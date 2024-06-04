<script  setup>
import { ref,onMounted } from 'vue'
import {useHistoryStore} from '@/stores/history.js'
import {useUserStore} from '@/stores/userInfo.js'
import {usepageStore} from '@/util/page.js'
import {useDateStore} from '@/util/date.js'
import { ElMessage, ElMessageBox } from 'element-plus'
const dateStore = useDateStore()
const historyStore = useHistoryStore()
const userStore = useUserStore()
const pageStore1 = usepageStore()//这个展示外部数据页
// const pageStore2 = usepageStore()//这个展示内部数据页
// const parentBorder = ref(false)
// const childBorder = ref(false)
const courseList = ref({
    // 格式 0:name
})
const selectCourseId = ref()
const tableData = ref([
    {
        time:'',
        accuracy:0,
        q_num:0,
        history:[{
        }]
    }
])
// 历史详情
// const history_list = ref([])
const pageNum = ref(1)//当前页
const total = ref(0)//总条数
const pageSize = ref(3)//每页条数
const setTableData = (data)=>{
    if(data==1){
        tableData.value = [{}]
        total.value = 0
        return
    }
    let formatData = []
    let times = Object.keys(data)
    // 时间降序排序
    times.sort((a, b) => b - a);
    // console.log('data',data)
    for(let t in times){
        let q_dic = data[times[t]]
        let acc = q_dic.accuracy
        let h_id = q_dic.h_id
        delete q_dic.h_id
        delete q_dic.accuracy
        let q_list = []
        for(let q_id in q_dic){
            // console.log('q_id',q_id)
            let q_info = historyStore.getQuestionInfoById(q_id)
            // console.log('q_info',q_info)
            // console.log('q_info.Q',q_info.Q)
            // 用户答案以及对应项
            let user_answer_value = q_dic[q_id].user_answer + q_info[q_dic[q_id].user_answer]
            q_list.push({
                id:q_id,
                Q:q_info.Q,
                answer:q_dic[q_id].answer,
                user_answer:user_answer_value,
                right:q_dic[q_id].right?'正确':'错误',
                info:q_info //题目内容和选项
            })
        }
        formatData.push({
            time:dateStore.formatDate(times[t]),  // dateStore.formatDate(times[t])
            accuracy:acc,
            h_id:h_id,
            length:q_list.length,
            questionList:q_list//题目列表,二级表
        })
    }
    tableData.value = pageStore1.init(formatData,3)
    total.value = pageStore1.total
}
onMounted(async()=>{
    courseList.value = await historyStore.getCourses()
    selectCourseId.value = courseList.value[0]
    await handleChange()
  })

//当每页条数发生了变化，调用此函数
const onSizeChange = (size) => {
     pageSize.value = size
     pageStore1.setPageSize(size)
     tableData.value = pageStore1.indexPageData(pageNum.value)
}
//当前页码发生变化，调用此函数
const onCurrentChange = (num) => {
    pageNum.value = num
    pageStore1.setCurrentPage(num)
    tableData.value = pageStore1.indexPageData(num)
}
//课程发生变化
const handleChange = async()=>{
    let course = null
    if (typeof selectCourseId.value === 'number'||/^\d+$/.test(selectCourseId.value) ) {
        course = courseList.value[selectCourseId.value]
    } else {
        course = selectCourseId.value
    }
    // console.log(course)
    let data = await historyStore.getHistory(userStore.info.username,course)
    // console.log('data',data)

    setTableData(data)
}
const isLoading = ref(false)
import {useChatStore} from '@/util/chat.js'
const chatStore = useChatStore()
const analysis = async(id)=>{
    // console.log('id',id)
    let q = historyStore.getQuestionInfoById(id)
    let question = q
    q = JSON.stringify(q)+'\n请分析上述题目'
    // console.log("q",q)
    isLoading.value = true
    let content = await chatStore.chat(q)
    isLoading.value = false
    content = "问题："+question.Q+"<br/>A"+question.A+"<br/>B"+question.B+"<br/>C"+question.C+"<br/>D"+question.D+"<br/>"+content
    ElMessageBox.alert(
    content,
    '分析',
    {
      dangerouslyUseHTMLString: true,
    }
  )

}
import {useErrorQuestionStore} from '@/stores/errorQ.js'
const errorQuestionStore = useErrorQuestionStore()
const upLoading = ref(false)
const addError = (q_id)=>{
    let username = userStore.info.username
    errorQuestionStore.addErrorQuestions(username,q_id)
}
  </script>
<template>
   <div class="center"><h1>答题记录</h1></div>

   <div style="margin-top:5%" v-loading="isLoading">
    <el-form-item label="课程：">
                <el-select  v-model="selectCourseId" placeholder='请选择' style="width: 240px" @change="handleChange">
                    <el-option 
                        v-for="key,value in courseList" 
                        :key="key" 
                        :label="key"
                        :value="value"
                    >
                    </el-option>
                </el-select>
    </el-form-item>
    <el-table :data="tableData"  style="width: 100%">
        <el-table-column type="expand">
            <template #default="props">
            <div m="4">
                <p m="t-0 b-2">正确率:{{ props.row.accuracy*100 }}% </p>
                <p m="t-0 b-2">题目数量:{{ props.row.length }} </p>
                <h3>测评题目</h3>
                <el-table :data="props.row.questionList">
                    <el-table-column label="id" prop="id" />
                    <el-table-column label="问题" prop="Q" />
                    <!-- <el-table-column label="答案" prop="answer" /> -->
                    <el-table-column label="你的答案" prop="user_answer" />
                    <el-table-column label="正误" prop="right" />
                    <el-table-column label="操作">
                    <template #default="propss">
                        <el-button @click="addError(propss.row.id)" type="success" v-loading="upLoading">添加到错题集</el-button>
                        <el-button @click="analysis(propss.row.id)">星火分析</el-button>
                    </template>
                    </el-table-column>
                </el-table>
            </div>
            </template>
        </el-table-column>
        <el-table-column label="答题时间" prop="time" >
        </el-table-column>
    </el-table>
    <el-pagination v-model:current-page="pageNum" v-model:page-size="pageSize" :page-sizes="[3, 5 ,10, 15]"
            layout="jumper, total, sizes, prev, pager, next" background :total="total" @size-change="onSizeChange"
            @current-change="onCurrentChange" style="margin-top: 20px; justify-content: flex-end" />

</div>

</template>

<style>

.center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 0vh; /* 视口高度 */
}
  
  </style>
  
  









