import {defineStore} from 'pinia'
import {ref} from 'vue'
import request from '@/util/request.js'
import {ElMessage} from 'element-plus'
import { useDateStore } from '@/util/date.js'
export const useTestPlanStore = defineStore('testPlan',()=>{
  
    const course = ref()
    const class_id = ref()
    const dateStore = useDateStore()
    
    const isRepeatTitle = async(title,class_id)=>{
        let planList = await getTestList(class_id)
        for(let i in planList){
            if(title==planList[i].TITLE){
                return true
            }
        }
        return false
    }
    const getTestList = async(class_id)=>{
       
        try{
            const response = await request.get('http://localhost:8080/test/getTestList?class_id='+class_id)
            
            let rs = []
            let data =  response.data
            // 降序排序
            data.sort((a, b) => b.CREATE_TIME - a.CREATE_TIME);
            for(let i in data){
                let plan = data[i]
                
                let new_plan = plan
                
                new_plan.START_TIME = dateStore.formatDateBytimestamp(new_plan.START_TIME)
                new_plan.END_TIME = dateStore.formatDateBytimestamp(new_plan.END_TIME)
                new_plan.CREATE_TIME = dateStore.formatDateBytimestamp(new_plan.CREATE_TIME)
                // console.log(new_plan.START_TIME,new_plan.END_TIME,new_plan.CREATE_TIME)
                rs.push(new_plan)
            }
            // console.log('rs',rs)
            return rs
        }catch(error){
            console.error(error)
        }
    }
    const updateTestPlan = async(test_plan)=>{
        
         const params = new FormData();
         test_plan.START_TIME = dateStore.formateToTimestep(test_plan.START_TIME)
         test_plan.END_TIME = dateStore.formateToTimestep(test_plan.END_TIME)
         test_plan.CREATE_TIME = dateStore.formateToTimestep(test_plan.CREATE_TIME)
        //  console.log("test_plan",test_plan)
         params.append('test_plan',JSON.stringify(test_plan))
         try{
             const response = await request.post('http://localhost:8080/test/updateTest',params)
             
             return response
         }catch(error){
             console.error(error)
             
         }
    }
    const deletePlan = async(plan_id)=>{
        const params = new FormData();
         params.append('plan_id',plan_id)
         try{
             const response = await request.post('http://localhost:8080/test/deletePlan',params)
             
             return response.data
         }catch(error){
             console.error(error)
             
         }
    }
    return {course,class_id,getTestList,updateTestPlan,deletePlan,isRepeatTitle}

},{persist:true})
