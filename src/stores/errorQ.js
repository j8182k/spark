import {defineStore} from 'pinia'
import {ref} from 'vue'
import request from '@/util/request.js'
import {ElMessage} from 'element-plus'
export const useErrorQuestionStore = defineStore('errorQ',()=>{
  
    const errorQ = ref({
        create_time:'',//日期
        info:'',//具体问题和答案
        analysis:'',//分析
        knowledge:''//知识点
      })
    const errorQuestionList = ref({})
    const getErrorQuestions = async(username,courses)=>{
        const params = new FormData();
        params.append('course',courses)
        params.append('username',username)
        try{
            const response = await request.post('http://localhost:8080/getErrorQuestion',params)
            let data = response.data
            // console.log('data',data)
            for(let i = 0; i < data.length; i++ ){
                data[i].info = JSON.parse(data[i].info)
            }
            
            errorQuestionList.value = data
            
            return errorQuestionList.value
        }catch(error){
            console.error(error)
        }
    }
    const addErrorQuestions = async(username,q_id)=>{
        const params = new FormData();
        params.append('username',username)
        params.append('q_id',q_id)
        try{
            const response = await request.post('http://localhost:8080/addErrorQuestion',params)
            ElMessage({
                message:response.desc,
                type:'success'
            })
        }catch(error){
            console.error(error)
        }
    }
    

    const clear = ()=>{
        
    }

    

    return {getErrorQuestions,addErrorQuestions}

},{persist:true})
