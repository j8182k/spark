  
  <script setup>
  import { ref } from 'vue'
  
  const radio1 = ref('1')
  const dic = ref({
    Q:'',
    A:'',
    B:'',
    C:'',
    D:'',
    answer:''
})
const downLoadQ = async () => {
        const params = new FormData();
        params.append('img', selectedFile.value)
        alert(selectedFile.value.name)
        try {
            // 使用 axios 发送文件到服务器  response = requests.post(request_url, files=files, data=body, headers=headers)
            const response = await axios.post('http://localhost:8080/uploadImg', params, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            console.log("response.data.data");
            console.log(response.data.data);
            dic.value.Q = response.data.data.Q
            dic.value.A = response.data.data.A
            dic.value.B = response.data.data.B
            dic.value.C = response.data.data.C
            dic.value.D = response.data.data.D
            dic.value.answer = response.data.data.answer
            console.log("dic.value");
            console.log(dic.value);
            alert('图片识别成功，请按需修改');
        } catch (error) {
            console.error(error);
        }
   
}

  </script>
  
<template>
    <div class="mb-2 flex items-center text-sm">
      <el-radio-group v-model="radio1" class="ml-4">
        <el-radio value="1" size="large">Option 1</el-radio>
        <el-radio value="2" size="large">Option 2</el-radio>
      </el-radio-group>
    </div>
   
  </template>

<style scoped>

    

</style>
