import {defineStore} from 'pinia'
import {ref} from 'vue'
import request from '@/util/request.js'
import {ElMessage} from 'element-plus'
import { useDateStore } from '@/util/date.js'
export const useQuestionStore = defineStore('question',()=>{

    const dateStore = useDateStore()
    const currentCourse = ref()
    //定义题目列表
    const questionList = ref([])
    //题目列表长度
    const q_len = ref(0)
    //本次测评的答题历史记录
    const q_history = ref({})
    //答题结果
    const result = ref({})

    //课程列表
    const courseList = ref({})
    
    // 获得课程列表
    const getCourse = async()=>{
        if(Object.keys(courseList.value).length == 0){
            const response = await request.get('http://localhost:8080/getCourse')
            courseList.value = response.data
        }
        return courseList.value
    }
    const initHistory = (questionList)=>{
        for(let i = 0; i < questionList.length; i++){
            let id = questionList[i].question_id
            q_history.value[id] = "-1"
        }
    }
    // 根据id获取题目详情
    const getQuestionByids = async(ids)=>{
        const params = new FormData();
        params.append('ids',ids)
        try{
            const response = await request.post('http://localhost:8080/getQuestions',params)
            // console.log("题目详情获取",response.data)
            return response.data
        }catch(error){
            console.error(error)
        }
    }
    //根据课程和用户名获取题目列表
    const getQuestionByCourse = async(courses,username,num)=>{
        const params = new FormData();
        params.append('course',courses)
        params.append('username',username)
        params.append('num',num)
        try{
            const response = await request.post('http://localhost:8080/getQuestions',params)
            let data = response.data
            let arr = []
            for(let q_id in data){
                let dic = {question_id:q_id}
                let line = data[q_id]
                // console.log('line',line)
                // line.create_time = dateStore.formatDate(line.create_time)
                let a = Object.assign(line,dic)
                // console.log('a',a)
                arr.push(a)
            }
            // arr.sort((a, b)=> {
            //     var date_a = new Date(a)
            //     var date_b = new Date(b)
            //     // console.log(date_a,date_b)
            //     return date_b - date_a;
            //   })
            console.log('arr',arr)
            return arr
      
        }catch(error){
            console.error(error)
        }
    }


    //答题历史保存
    const addRecord = (user_answer,q_id)=>{
      
        q_history.value[q_id] = user_answer
    }

    const genQuestion = async(question)=>{
        // 基于旧题目生成类似的新题目
        const params = new FormData();
        params.append('question',JSON.stringify(question))
        try{
            const response = await request.post('http://localhost:8080/genQuestion',params)
            
            return response
        }catch(error){
            console.error(error)
            return 1
        }
    }
    //提交答案,给后端处理
    const submit = async(username,course)=>{
        // console.log('history',q_history)
        for(let key in q_history.value){
            if(q_history.value[key]=='-1'){
                ElMessage.error('答题未完成')
                return 1
            }
        }
      
        const params = new FormData();
        const str = JSON.stringify(q_history.value);
        params.append('q_history',str)
        params.append('username',username)
        params.append('course',course)
        try{
            const response = await request.post('http://localhost:8080/submit',params)
            const rs_data = JSON.parse(response.data)
            for(let key in rs_data){
                result[rs_data[key].id] = rs_data[key].right
            }
            return result
        }catch(error){
            console.error(error)
            return 1
        }
        
    }
    // 获取学生的所有答题历史记录，用于绘制曲线图
    const getHistoryQ = async(username,course)=>{
        const params = new FormData();
        params.append('username',username)
        params.append('course',course)
        try{
            const response = await request.post('http://localhost:8080/getHistory',params)
            let rs_data = response.data
            let record = {}
            for(let i = 0 ; i<rs_data.length;i++){
                let time =new Date(rs_data[i].create_time)
                time = time.getTime()
                let history = rs_data[i].history
                record[time] = JSON.parse(history)
            }
            // console.log('record',record)
            return record
        }catch(error){
            console.error(error)
            return 1
        }
    }
    // 把以id为索引的题目字典转换成列表
    const questionDicTolist = (dic)=>{
        console.log('dic',dic)
        let arr = []
        for(let id in dic){
            arr.push(dic[id])
        }
        console.log('arr',arr)
        return arr
    }
   
    const clear = ()=>{
        //定义题目列表
        questionList.value = []
        //题目列表长度
        q_len.value = 0
        //答题历史记录
        q_history.value = {}
        //课程列表
        courseList.value = {}

        result.value = {}
    }

    

    return {currentCourse,getQuestionByids,getHistoryQ,getQuestionByCourse,
        courseList,q_len,addRecord,submit,q_history,clear,
        genQuestion,getCourse,initHistory}

},{persist:true})
