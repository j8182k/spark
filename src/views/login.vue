<script setup>
import { User, Lock } from '@element-plus/icons-vue'
import { ref } from 'vue'
// import axios from 'axios'
import request from '../util/request.js'

// const value1 = ref(true)
//定义数据模型
const registerData = ref({
    username: '',
    password: '',
    type: 'student'

})

//定义表单校验规则
const rules = {
    username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 5, max: 16, message: '长度为5~16位非空字符', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 5, max: 16, message: '长度为5~16位非空字符', trigger: 'blur' }
    ]
   
}


//表单数据校验
//登录函数
//路由定义
import {useRouter} from 'vue-router'
const router = useRouter()
//token获取之后存储到pinia
import {useTokenStore} from '../stores/token.js'
import {useUserStore} from '../stores/userInfo.js'
import { ElMessage, ElMessageBox } from 'element-plus'
const tokenStore = useTokenStore() 
const userStore = useUserStore()
const login =async ()=>{
    //调用接口,完成登录
    const params = new FormData();
    if(registerData.value.username===''){
   
        ElMessage('请输入用户名')
        return 
    }
    if(registerData.value.password===''){
       
        ElMessage('请输入密码')
        return
    }
    params.append('username', registerData.value.username)
    params.append('password', registerData.value.password)
    params.append('type', registerData.value.type)
   try {
        // 使用 axios 发送文件到服务器  response = requests.post(request_url, files=files, data=body, headers=headers)
        const response = await request.post('http://localhost:8080/login',params)

        const code = response.code
        if (code === "0"){
            ElMessage({
                message:'登录成功',
                type:'success'
            })
            //存储token及用户信息
            tokenStore.setToken(response.data)
            userStore.setInfo(registerData.value.username,registerData.value.type)
            router.push('/')
        }else{
            ElMessage(response.desc)
        }
      } catch (error) {
        console.error(error);
      }

}



const options = [
  {
    value: 'student',
    label: '学生',
  },
  {
    value: 'teacher',
    label: '教师',
  }
]

const register = ()=>{




    
}





</script>

<template>
    <el-row class="login-page">
        <el-col :span="12" class="bg"></el-col>
        <el-col :span="6" :offset="3" class="form">
           
            <!-- 登录表单 -->
            <el-form ref="form" size="large" autocomplete="off" :model="registerData" :rules="rules">
                <el-form-item>
                    <h1 style="color:black">登录</h1>    
                </el-form-item>
                <el-form-item>
                    <el-select
                    v-model="registerData.type"
                    placeholder="学生"
                    :value="student"
                    style="width: 240px"
                    >
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                    />
                    </el-select>
                </el-form-item>
                <el-form-item prop="username">
                    <el-input :prefix-icon="User" placeholder="请输入用户名" v-model="registerData.username"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input name="password" :prefix-icon="Lock" type="password" placeholder="请输入密码" v-model="registerData.password"></el-input>
                </el-form-item>
                <el-form-item class="flex">
                    <div class="flex">
                        <el-checkbox>记住我</el-checkbox>
                        <el-link type="primary" :underline="false">忘记密码？</el-link>
                    </div>
                </el-form-item>
                <!-- 登录按钮 -->
                <el-form-item>
                    <el-button class="button" type="primary" auto-insert-space @click="login">登录</el-button>
                </el-form-item>
            </el-form>
            <!-- 注册表单 -->
            <!-- <el-form ref="form" size="large" autocomplete="off" :model="registerData" :rules="rules">
                <el-form-item>
                    <h1 style="color:black">注册</h1>    
                </el-form-item>
                <el-form-item>
                    <el-select
                    v-model="registerData.type"
                    placeholder="学生"
                    :value="student"
                    style="width: 240px"
                    >
                    <el-option
                    v-for="item in options"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                    />
                    </el-select>
                </el-form-item>
                <el-form-item prop="username">
                    <el-input :prefix-icon="User" placeholder="请输入用户名" v-model="registerData.username"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input name="password" :prefix-icon="Lock" type="password" placeholder="请输入密码" v-model="registerData.password"></el-input>
                </el-form-item>
                <el-form-item class="flex">
                    <div class="flex">
                        <el-checkbox>记住我</el-checkbox>
                        <el-link type="primary" :underline="false">忘记密码？</el-link>
                    </div>
                </el-form-item>
               
                <el-form-item>
                    <el-button class="button" type="primary" auto-insert-space @click="register">注册</el-button>
                </el-form-item>
            </el-form> -->








        </el-col>
    </el-row>
</template>

<style lang="scss" scoped>
/* 样式 */
.login-page {
    width: 100%;
    height: 100vh;
    background-color: #fff;
    position: absolute;
    left: 0%;
    top:0%;
    .bg {
        background: 
            url('@/assets/login.png') no-repeat center / cover;
        border-radius: 0 20px 20px 0;
    }

    .form {
        display: flex;
        flex-direction: column;
        justify-content: center;
        user-select: none;

        .title {
            margin: 0 auto;
        }

        .button {
            width: 100%;
        }

        .flex {
            width: 100%;
            display: flex;
            justify-content: space-between;
        }
    }
}
</style>