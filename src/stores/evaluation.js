import {defineStore} from 'pinia'
import {ref} from 'vue'
import request from '@/util/request.js'
import { useQuestionStore } from '@/stores/question.js'
import { useChatStore } from '@/util/chat'
export const useEvaluationStore = defineStore('evaluation',()=>{
    
    const questionStore = useQuestionStore()
    const chatStore = useChatStore()
    const current_plan_id = ref()

    const getPlanList = async(username)=>{
        // 根据用户名查找学生的测评计划列表
        try{
            const response = await request.get('http://localhost:8080/test/getStudentTestList?username='+username)
            // console.log("测评列表获取成功",response.data)
            return response.data
        }catch(error){
            console.error(error)
        }
    }

    const analysisQuestion = async(question)=>{
        chatStore.clear()
        let content = "问题："+question.Q+" A:"+question.A+" B:"+question.B+" C:"+question.C+" D:"+question.D
        content = content + "\n上述是学生做错的一道题目，请用概括这道题的知识点，不要多余的字，注意：你生成的知识点不要超过10个字"
        let rs = await chatStore.chat(content)
        return rs
    }
    const genScheme = async(all_knowledge)=>{
        chatStore.setPrompt("请针对下述知识点，生成一个学习方案（不超过200字）\n")
        let content = all_knowledge
        let rs = await chatStore.chat(content)
        // console.log('rs',rs)
        return rs
    }
    const save_plan_rs_form = async(rs_form)=>{
        // 基于旧题目生成类似的新题目
        const params = new FormData();
        params.append('rs_form',rs_form)
        try{
            const response = await request.post('http://localhost:8080/test/submitRs',params)
            return response.data
        }catch(error){
            console.error(error)
        }
    }

    const get_plan_rs = async(username)=>{
        try{
            const response = await request.get('http://localhost:8080/test/get_plan_rs?username='+username)
            return response.data
        }catch(error){
            console.error(error)
        }
    }


    return {current_plan_id,getPlanList,analysisQuestion,genScheme,save_plan_rs_form,get_plan_rs}

},{persist:true})
