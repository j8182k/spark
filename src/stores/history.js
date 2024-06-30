import {defineStore} from 'pinia'
import {ref} from 'vue'
import request from '@/util/request.js'
import {useQuestionStore} from '@/stores/question.js'
// import {ElMessage} from 'element-plus'
// import { da } from 'element-plus/es/locale'
export const useHistoryStore = defineStore('history',()=>{
    
    const historyDic = ref({
        //格式：{ 1716518977: {…}, 1716534732: {…}, 1716534757: {…}, … }
        // 1716518977: { 1: {…}, 4: {…}, 12: {…}, … }
        // 1:  { answer: "B", right: false, user_answer: "C" }
    
    })
    // 对应于上述历史字典的题目详情，以题目id为索引方便查找
    const questionInfo = ref({
        // 格式：{ 1: {…}, 4: {…}, 12: {…}, … }
    })
    const questionStore = useQuestionStore()
      //课程列表
    const courseList = ref({})
    
      // 获得课程列表
    const getCourses = async()=>{
        if(Object.keys(courseList.value).length == 0){
              const response = await request.get('http://localhost:8080/getCourse')
              courseList.value = response.data
        }
          return courseList.value
    }
    const getHistory = async(username,courses)=>{
        clear()
        const params = new FormData();
        params.append('course',courses)
        params.append('username',username)
        try{
            const response = await request.post('http://localhost:8080/getHistory',params)
            let data = response.data
            // console.log('data',data)
            if(data == '1'||data == 1 ){
                return 1
            }
            let idSet = new Set()
            for(let i = 0;i<data.length;i++){
                // console.log('data[i]',data[i])
                let time = data[i].create_time
                // console.log('time',time)
                // time = new Date(time)
                let history = JSON.parse(data[i].history)
                // 存储题目id列表，生成id字典，方便查找题目
                let list_id = Object.keys(history)
                let new_set = new Set(list_id)
                idSet = new Set([...new_set,...idSet])
                // 把正确率放入history中
                history.accuracy = data[i].accuracy
                // 把历史记录的id放入history中
                history.h_id = data[i].h_id

                // console.log('history',history)
                // 保存成以时间为索引的字典
                historyDic.value[time] = history
            }
            let ids = Array.from(idSet)
            // console.log(ids)
            questionInfo.value = await questionStore.getQuestionByids(ids)
            // console.log('questionInfo',questionInfo)
            let info_dic = {}
            for(let index in questionInfo.value){
                let id = questionInfo.value[index].id
                info_dic[id] = questionInfo.value[index]
            }
            // console.log('info_dic',info_dic)
            questionInfo.value = info_dic



            // console.log('historyDic',historyDic)
            return historyDic.value
        }catch(error){
            console.error(error)
        }
    }
    const getQuestionInfoById = (id)=>{
        return questionInfo.value[id]
    }
    const clear = ()=>{
        historyDic.value = {}
        questionInfo.value = {}
    }


    return {getHistory,clear,getCourses,getQuestionInfoById}

},{persist:true})
