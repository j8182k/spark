import {defineStore} from 'pinia'
import {ref} from 'vue'
import request from '@/util/request.js'
import {ElMessage} from 'element-plus'
export const useChatStore = defineStore('chat',()=>{
  
    const chat = async(content)=>{
        const params = new FormData();
        params.append('question',content)
        try{
            const response = await request.post('http://localhost:8080/chatBytext',params)
            
            return response.data
           
        }catch(error){
            console.error(error)
        }
    }

    const clear = ()=>{
        
    }

    

    return {chat}

},{persist:true})
