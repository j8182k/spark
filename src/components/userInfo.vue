<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {useUserStore} from '@/stores/userInfo.js'
const userInfo = useUserStore()
const info = ref({
    username:'',
    password:'',
    nickname:'',
    type:'',
    gender:'',
    age:0,
    class:'',
    phone:0,
    avatar:'@/assets/avatar.jpg'
})
onMounted(()=>{
  info.value = userInfo.info
})
const nicknameRule = ()=>{
  return info.value.nickname != ''
}
const ageRule = ()=>{
  let value = info.value.age
  if(/^\d+$/.test(value) && value >= 1 && value <= 100 ){
    return true
  }else{
    return false
  }
}
const rules= {
        nickname: [
          { validator: nicknameRule, message: "昵称不能为空", trigger: "blur" },
        ],
        class: [
          { validator: info.value.class != '', message: "班级不能为空", trigger: "blur" },
        ],
        age: [
          { validator: ageRule, message: "必须是1~100的数字", trigger: "blur" },
        ],
}
const submit = ()=>{
  userInfo.updateInfo(JSON.stringify(info.value))
}
// 用户信息展示
// 账户，姓名，身份，性别，年龄，班级，电话
</script>
<template>
  <h1>基本资料</h1>
  <el-form
    style="max-width: 600px"
    :v-model="info"
    :rules="rules"
    label-width="auto"
    class="demo-ruleForm"
    status-icon
  >
    <el-form-item label="用户名" prop="username">
      <el-input v-model="info.username"  disabled/>
    </el-form-item>
    <el-form-item label="身份" prop="type">
      <el-select v-model="info.type" placeholder="未知">
        <el-option label="学生" value="student" />
        <el-option label="老师" value="teacher" />
      </el-select>
    </el-form-item>
    <el-form-item label="昵称" prop="nickname">
      <el-input v-model="info.nickname" />
    </el-form-item>
    <el-form-item label="性别" prop="gender">
      <el-select v-model="info.gender" placeholder="未知">
        <el-option label="男" value="男" />
        <el-option label="女" value="女" />
      </el-select>
    </el-form-item>
    <el-form-item label="年龄" prop="age">
      <el-input v-model="info.age" />
    </el-form-item>
    <el-form-item label="班级" prop="class">
      <el-input v-model="info.class" />
    </el-form-item>
    <el-form-item label="电话" prop="phone" v-if="info.type == 'teacher'">
      <el-input v-model="info.phone" />
    </el-form-item>
    <el-form-item>
      <el-button style="margin-left:90%" type="primary" @click="submit" >
        确认
      </el-button>
      
    </el-form-item>
  </el-form>
</template>



