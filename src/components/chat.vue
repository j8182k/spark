<!-- <script setup>
import axios from 'axios';
import { ref } from 'vue';

import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'


const data = ref({
    inputData: '',
    outputData: ''
});

const submit = async()=> {
         const params = new FormData();
         if(!data.value.inputData){
            alert('请输入问题')
            return
         }
        alert(data.value.inputData)
         params.append('question', data.value.inputData)
    try {
        // 使用 axios 发送文件到服务器  response = requests.post(request_url, files=files, data=body, headers=headers)
        const response = await axios.post('http://localhost:8080/chatBytext',params)
        console.log(response.data);
        data.value.outputData = response.data.data
        alert('上传成功');
      } catch (error) {
        console.error(error);
      }
    }
</script>

<template>
<div class="body">
   
    <div>星火回答：</div>
    <br>
    <br>
    <br>
    <div>
      <el-text class="answer" type="success">{{data.outputData}}</el-text>
    </div>
    <br>
    <br>
    <div class="q">
      <div><input  v-model="data.inputData" style="width: 240px" autosize type="textarea"/></div>
      <div style="padding-left:10%"><el-button @click="submit" type="primary">提问</el-button></div>
    </div>
</div>
</template>

<style scoped>
/* .body{
  background-color:ivory;

} */
  .q{
    display:flex;
  }
  .answer{
    border-radius:10%;
    width:240px;
    height:240px;

  }
  input {
    border: 1px solid #ccc;
    width: 300px;
    height: 30px;
  }
</style> -->
<template>
  <div>
    <h1>我的聊天应用</h1>
    <ChatWindow />
  </div>
</template>

<script>
import ChatWindow from '@/components/ChatWindow.vue';

export default {
  components: {
    ChatWindow,
  },
};
</script>
