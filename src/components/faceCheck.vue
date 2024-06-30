<template>
  <div>
    <video ref="video" autoplay></video>
    
    <!-- <el-button @click="startCamera">启动摄像头</el-button>
    <el-button @click="stopCamera">关闭摄像头</el-button> -->
  </div>
</template>

<script>
import request from '@/util/request.js';
import { ElMessage } from 'element-plus';
import { useIllegalOperationStore } from '@/stores/illegalOperation';
export default {
  data() {
    return {
      mediaRecorder: null,
      recordingInterval: null,
      check_seqs:[],
      illegalOperation:useIllegalOperationStore()
    };
  },
  mounted() {
    // this.startCamera();
  },
  methods: {
    startCamera() {
      const constraints = { video: true };
      navigator.mediaDevices.getUserMedia(constraints)
        .then((stream) => {
          this.$refs.video.srcObject = stream;
          this.startRecording(stream);
        })
        .catch((error) => {
          console.error('无法访问摄像头', error);
        });
    },
    stopCamera() {
      if (this.$refs.video.srcObject) {
        this.$refs.video.srcObject.getTracks().forEach(track => track.stop());
        this.$refs.video.srcObject = null;
      }
      if (this.mediaRecorder) {
        this.mediaRecorder.stop();
      }
      if (this.recordingInterval) {
        clearInterval(this.recordingInterval);
      }
    },
    startRecording(stream) {
      this.mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
      this.mediaRecorder.ondataavailable = this.handleDataAvailable;
      this.recordingInterval = setInterval(() => {
        if (this.mediaRecorder.state === 'recording') {
          this.mediaRecorder.stop();
        }
        this.mediaRecorder.start(4000); // 每4秒录制一次
      }, 4000);
    },
    handleDataAvailable(event) {
      if (event.data.size > 0) {
        this.uploadVideo(event.data);
      }
    },
    uploadVideo(blob) {
      const formData = new FormData();
      formData.append('video', blob, 'video.mp4');

      request.post('http://localhost:8080/video', formData)
        .then(response => {
          // console.log('视频上传成功', response.data);
          let data = response.data
          if(data.alive&&data.face){
            this.check_seqs.push(true)
          }else{
            this.check_seqs.push(false)
          }
          if(this.check_seqs.length > 3){
              this.check_seqs.shift()
            }
          let isValidate = this.faceValidate()
          if(!isValidate){
              ElMessage.error('人脸验证失败')
              // 人脸验证失败,设置违规状态
              this.illegalOperation.state = true
          }else{
            ElMessage({
              type:'success',
              message:'人脸验证成功'
            })
          }
        })
        .catch(error => {
          console.error('视频上传失败', error);
        });
    },
    faceValidate(){
      // 当连续多个检测不通过时，判定人脸检测失败
      console.log('check_seqs',this.check_seqs)
      let isAllFalse = this.check_seqs.every(item => item === false);
      return !isAllFalse
    },
  },
};
</script>


