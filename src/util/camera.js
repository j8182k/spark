// src/util/camera.js
import request from '@/util/request.js';

export const startCamera = (videoRef, mediaRecorderRef, recordingIntervalRef, handleDataAvailable) => {
  const constraints = { video: true };
  navigator.mediaDevices.getUserMedia(constraints)
    .then((stream) => {
      videoRef.srcObject = stream;
      startRecording(stream, mediaRecorderRef, recordingIntervalRef, handleDataAvailable);
    })
    .catch((error) => {
      console.error('无法访问摄像头', error);
    });
};

export const stopCamera = (videoRef, mediaRecorderRef, recordingIntervalRef) => {
  if (videoRef.srcObject) {
    videoRef.srcObject.getTracks().forEach(track => track.stop());
    videoRef.srcObject = null;
  }
  if (mediaRecorderRef.current) {
    mediaRecorderRef.current.stop();
  }
  if (recordingIntervalRef.current) {
    clearInterval(recordingIntervalRef.current);
  }
};

const startRecording = (stream, mediaRecorderRef, recordingIntervalRef, handleDataAvailable) => {
  mediaRecorderRef.current = new MediaRecorder(stream, { mimeType: 'video/webm' });
  mediaRecorderRef.current.ondataavailable = handleDataAvailable;
  recordingIntervalRef.current = setInterval(() => {
    if (mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
    mediaRecorderRef.current.start(3000); // 每3秒录制一次
  }, 3000);
};

export const handleDataAvailable = (event, uploadVideo) => {
  if (event.data.size > 0) {
    uploadVideo(event.data);
  }
};

export const uploadVideo = (blob, check_seqs) => {
  const formData = new FormData();
  formData.append('video', blob, 'video.mp4');

  request.post('http://localhost:8080/video', formData)
    .then(response => {
      console.log('视频上传成功', response.data);
      let data = response.data;
      if (data.alive && data.face) {
        check_seqs.push(true);
      } else {
        check_seqs.push(false);
      }
      if (check_seqs.length > 20) {
        check_seqs.pop();
      }
    })
    .catch(error => {
      console.error('视频上传失败', error);
    });
};

export const faceValidate = (check_seqs) => {
  // 当连续20个检测不通过时，判定人脸检测失败
  let isAllFalse = check_seqs.every(item => item === false);
  return !isAllFalse;
};
