<script setup>
import { ElMessage } from 'element-plus'
import { ref,onMounted } from 'vue';
import request from '../util/request.js';


const data = ref({
    inputData: '',
    fileNames: {},
    selectedFile:'请选择知识文本',
    outputData: ''
});
onMounted( async()=>{
    const response = await request.get("http://localhost:8080/getFileNames")
    data.value.fileNames = response.data
    console.log(data.value.fileNames)
})
const showFile = (value)=>{
    data.value.selectedFile = value
}

const submit = async()=> {
         const params = new FormData();
         if(!data.value.inputData){
            ElMessage('请输入问题')
            return
         }
         if(data.value.selectedFile==='未选'){
            ElMessage('请选择文本')
            return
         }
        ElMessage(data.value.inputData)
         params.append('question', data.value.inputData)
         params.append('fileName',data.value.selectedFile)
    try {
        // 使用 axios 发送文件到服务器  response = requests.post(request_url, files=files, data=body, headers=headers)
        const response = await request.post('http://localhost:8080/chatOnfiles',params)
        // console.log(response.data);
        data.value.outputData = response.data
        ElMessage('已发送请求');
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
      <div><input  v-model="data.inputData" autosize type="textarea"/></div>
      
      <div style="padding-left:10%;padding-right:10%"><el-button @click="submit" type="primary">提问</el-button></div>
      <div class="flex flex-wrap items-center">
        <el-dropdown >
        <el-button type="primary">
            {{ data.selectedFile }}<el-icon class="el-icon--right"><arrow-down /></el-icon>
        </el-button>
        <template #dropdown>
            <el-dropdown-menu>
                <el-dropdown-item v-for="(value, key) in data.fileNames" :key="key" @click = "showFile(key)">{{ key }}</el-dropdown-item>
            </el-dropdown-menu>
        </template>
        </el-dropdown>
    </div>
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
</style>
