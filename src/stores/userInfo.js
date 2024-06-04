import {defineStore} from 'pinia'
import {ref} from 'vue'
import request from '@/util/request.js'
import { ElMessage, ElMessageBox } from 'element-plus'
import {useTokenStore} from '../stores/token.js'

export const useUserStore = defineStore('userInfo',()=>{
    const tokenStore = useTokenStore() 
    //定义状态相关的内容
    const info = ref({
        username:'',
        password:'',
        nickname:'',
        type:'',
        gender:'',
        age:0,
        class:'',
        phone:0
    })
    //定义技能信息
    const skill = ref({
        course:'',
        mu:25.0,
        sigma:8.334
    })
    const login = async(username,password,type)=>{
        //调用接口,完成登录
        const params = new FormData();
        if(username===''){
            ElMessage('请输入用户名')
            return false
        }
        if(password===''){
            ElMessage('请输入密码')
            return false
        }
        params.append('username', username)
        params.append('password', password)
        params.append('type', type)
       try {
            // 使用 axios 发送文件到服务器  response = requests.post(request_url, files=files, data=body, headers=headers)
            const response = await request.post('http://localhost:8080/login',params)
            const code = response.code
            if (code === "0"){
                //存储token及用户信息
                tokenStore.setToken(response.data)
                setInfo(username,type)
                // console.log('用户信息已经存储',info.value)
                
                return true
            }else{
                ElMessage(response.desc)
                return false

            }
          } catch (error) {
            console.error(error);
            return false
          }
    
    }
    const setInfo = async(names,type)=>{
        info.value.username = names
        info.value.type = type
        const params = new FormData();
        params.append('username',names)
        params.append('type',type)
        try{
            const response = await request.post('http://localhost:8080/getUserinfo',params)
            info.value = response.data
            info.value.type = type
            // console.log('用户信息已存储')
            // console.log(info.value)
        }catch(error){
            console.error(error)
        }
    }
    const setSkill = async(course)=>{
        const params = new FormData();
        params.append('username',info.value.username)
        params.append('course',course)
        try{
            const response = await request.post('http://localhost:8080/getUserSkill',params)
            skill.value.course = course
            skill.value.mu = response.data.mu
            skill.value.sigma = response.data.sigma
        }catch(error){
            console.error(error)
        }
    }

    const updateInfo = async(info)=>{
        const params = new FormData();
        params.append('userInfo',info)
        try{
            const response = await request.post('http://localhost:8080/updateInfo',params)
            
            ElMessage({
                message:'修改成功',
                type:'success'
            })

        }catch(error){
            console.error(error)
        }
    }

    const modifyPassword = async(info,new_password)=>{
        const params = new FormData();
        params.append('userInfo',info);
        params.append('new_password',new_password);
        try{
            const response = await request.post('http://localhost:8080/updateInfo',params)
        }catch(error){
            console.error(error)
        }
    }

    const removeInfo = ()=>{
        info.value = {
            name:'',
            password:'',
            nickname:'',
            type:'',
            gender:'',
            age:0,
            class:'',
            phone:0
        }
    }

    return {info,setInfo,setSkill,removeInfo,updateInfo,modifyPassword,login}

},{persist:true})
