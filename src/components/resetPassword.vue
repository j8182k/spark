<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {useUserStore} from '@/stores/userInfo.js'
import {useRouter} from 'vue-router'
const router = useRouter()
const userInfo = useUserStore()
const data = ref({
    old_password:'',
    new_password:'',
    user_password:''
})
const isdisabled = ref(false)
const check = ref([false,false,false])
const oldCheck= async()=>{
    if(data.value.old_password==''){
        check.value[0] = false
        return false
    }
    let isright = await userInfo.login(userInfo.info.username,data.value.old_password,userInfo.info.type)
    // console.log('right',isright)
    if(isright){
        check.value[0] = true
    }else{
        check.value[0] = false
    }
    return isright
}

const new_passwordCheck = ()=>{
    if(data.value.new_password==''){
        check.value[1] = false
        return false
    }
    if(data.value.new_password == data.value.old_password){
        ElMessage.error('新密码不能与原密码重复！')
        check.value[1] = false
        return false
    }
    var pattern = /^\S{5,16}$/;
    let right = pattern.test(data.value.new_password);
    if(right){
        check.value[1] = true
    }else{
        check.value[1] = false
    }
    return right
}
const user_passwordCheck = ()=>{
    if(data.value.user_password == ''){
        check.value[2] = false
        return false
    }
    let right = data.value.user_password == data.value.new_password
    if(right){
        check.value[2] = true
    }else{
        check.value[2] = false
    }
    return right
}
const rules= {
    old_password: [
          { validator: oldCheck, message: "原密码输入不正确", trigger: "blur" },
        ],
    new_password: [
          { validator: new_passwordCheck, message: "新密码长度必须为5~16位非空字符", trigger: "blur" },
        ],
    user_password: [
          { validator: user_passwordCheck, message: "与新密码不一致，请再次输入", trigger: "blur" },
        ]
}
const submit = ()=>{
  for(let i = 0;i < 3;i++){
    if(!check.value[i]){
        ElMessage.error('请填写正确信息')
        return
    }
  }
  userInfo.modifyPassword(JSON.stringify(userInfo.info),data.value.new_password)
  ElMessage({
    message:'密码修改成功，请重新登录',
    type:'success'
  })
  router.push('/login')
}

</script>
<template>
  <h1>重置密码</h1>
  <el-form
    style="max-width: 600px;"
    :v-model="data"
    :rules="rules"
    label-width="auto"
    class="demo-ruleForm"
    status-icon
   >
            <el-form-item label="原密码" prop="old_password">
                <el-input type="password" v-model="data.old_password"/>
            </el-form-item>
            <el-form-item label="新密码" prop="new_password">
                <el-input type="password" v-model="data.new_password"/>
            </el-form-item>
            <el-form-item label="再次输入新密码" prop="user_password">
                <el-input type="password" v-model="data.user_password" />
            </el-form-item>
            
            <el-form-item>
                <el-button style="margin-left:90%;" type="primary" @click="submit" :disabled="isdisabled" >
                    提交
                </el-button>
            </el-form-item>
  </el-form>
</template>



