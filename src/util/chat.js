import {defineStore} from 'pinia'
import {ref} from 'vue'
import request from '@/util/request.js'
import {ElMessage} from 'element-plus'
export const useChatStore = defineStore('chat',()=>{
  
    const prompt = ref("")
    const preQuestion = ref("") //当前答疑问题
 
    const chat = async(content)=>{
        
        const params = new FormData();
        params.append('question',prompt.value+content)
        try{
            const response = await request.post('http://localhost:8080/chat',params)
            
            return response.data
           
        }catch(error){
            console.error(error)
        }
    }
    const setPrompt = (str)=>{
        prompt.value = str
    }
    const getPrompt = ()=>{
        return prompt.value
    }
    const setPreQuestion = (str)=>{

        preQuestion.value = str
        console.log('设置preQuestion',preQuestion.value)
    }
    const getPreQuestion = ()=>{
        return preQuestion.value
    }
    
  
    const clear = ()=>{
        setPrompt("")
        setPreQuestion("")
    }

    

    return {chat,setPrompt,getPrompt,setPreQuestion,getPreQuestion,clear}

},{persist:true})
