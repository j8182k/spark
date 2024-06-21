<template>
    <div>
      <video ref="video" autoplay></video>
      <el-button @click="startCamera">启动摄像头</el-button>
    </div>
  </template>
  
  <script>
  export default {
    methods: {
      startCamera() {
        const constraints = { video: true };
        navigator.mediaDevices.getUserMedia(constraints)
          .then((stream) => {
            this.$refs.video.srcObject = stream;
          })
          .catch((error) => {
            console.error('无法访问摄像头', error);
          });
      }
    }
  }
  </script>
  








