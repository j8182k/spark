<script setup>
import {ref} from 'vue'

import request from '@/util/request.js'
import { UploadFilled } from '@element-plus/icons-vue'

// 选择要上传的文件
const selectedFile = ref()
const handleFileUpload = async(file)=>{
    // 获取文件类型
    const fileType = file.type;

    // 定义允许的文件类型
    const allowedTypes = ["text/plain", "application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];

    // 检查文件类型是否在允许的类型列表中
    if (!allowedTypes.includes(fileType)) {
      // 如果文件类型不在允许的类型列表中，提示用户重新输入
      alert("请上传 text/pdf/doc/docx 格式的文件");
      return;
    }
    selectedFile.value = await file.file
    console.log("selectedFile.value")
    console.log(selectedFile.value)
    
}
// 将要上传的文件转发到后台，再由后台转发到线上知识库
const submitForm = async()=>{
  if(selectedFile.value){
    const params = new FormData();
    params.append('files',selectedFile.value)
    alert(selectedFile.value.name)
    try {
        // 使用 axios 发送文件到服务器  response = requests.post(request_url, files=files, data=body, headers=headers)
        const response = await request.post('http://localhost:8080/upload',params,{
                   headers: {
                    'Content-Type': 'multipart/form-data'
                  }
             })
        console.log(response.data);
        alert('上传成功');
      } catch (error) {
        console.error(error);
      }
  }else{
    alert('请选择一个文件上传');
  }
}
</script>
<template>

 <!-- <div>

    <input type="file" @change="handleFileUpload($event)"/>
    <button @click="submitForm">上传文件</button>
  </div> -->
  <el-upload
    class="upload-demo"
    drag
    action="#"
    multiple
    :limit="1"
    :file-list="fileList"
    :http-request="handleFileUpload"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
    <template #tip>
      <div class="el-upload__tip">
        text/pdf/doc/docx files with a size less than 20Mb
      </div>
    </template>
  </el-upload>
  <el-button @click="submitForm" type="success">上传文件</el-button>



</template>

<style scoped>

</style>
