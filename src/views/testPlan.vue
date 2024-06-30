<!-- 测评计划创建 -->
<script setup>

import { ref,onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useSemesterStore } from '@/stores/semester';
import { useUserStore } from '@/stores/userInfo';
import request from '@/util/request.js'
const semesterStore = useSemesterStore()
const userStore = useUserStore()
const combineDateAndTime=(datePart, timePart)=>{
// 分别从datePart提取年月日

let yearMonthDay = new Date(datePart.getFullYear(), datePart.getMonth(), datePart.getDate());

// 从timePart提取时分秒毫秒

let hours = timePart.getHours();

let minutes = timePart.getMinutes();

let seconds = timePart.getSeconds();

let milliseconds = timePart.getMilliseconds();


// 将时分秒毫秒设置到年月日上

yearMonthDay.setHours(hours);

yearMonthDay.setMinutes(minutes);

yearMonthDay.setSeconds(seconds);

yearMonthDay.setMilliseconds(milliseconds);

// 使用 getTime() 方法获取毫秒级别的时间戳

milliseconds = yearMonthDay.getTime();

// 将毫秒转换为秒
// console.log('yearMonthDay',yearMonthDay)
seconds = Math.floor(milliseconds / 1000);
// console.log('milliseconds',milliseconds)
return seconds;
}

const value2 = ref([
  new Date(2016, 9, 10, 8, 40),
  new Date(2016, 9, 10, 9, 40),
])
const date = ref(new Date())
const test_plan = ref({
    title:'',
    class_id:'',
    start_time:'',
    end_time:'',
    state: 0,
    remark:'',
    questionList:[]
})
onMounted(()=>{
    initData()
})
//分类数据模型，班级列表
const categorys = ref({
    // id:字符串
})

//用户搜索时选中的分类id,班级id
const categoryId=ref('')
const initData = async()=>{
    categorys.value = {}
    // 获取该老师创建的所有班级数据
    let data = await semesterStore.getSemester(userStore.info.username)
    // console.log('data',data)
    for(let i in data){
        // 设置班级学科映射
        semesterStore.classID_course[data[i].id] = data[i].course
        // 填写分类数据模型
        categorys.value[data[i].id]=data[i].name+'('+data[i].course+')'
    }

}
// 提交测评计划
const submitTest_plan = async()=>{
    if(test_plan.value.title==''){
        ElMessage.error('请输入标题')
        return
    }
    if(test_plan.value.questionList.length==0){
        ElMessage.error('请添加题目')
        return
    }
    test_plan.value.start_time = combineDateAndTime(date.value,value2.value[0])
    test_plan.value.end_time = combineDateAndTime(date.value,value2.value[1])
    console.log('test_plan',test_plan)
    const params = new FormData();
    params.append('title',test_plan.value.title)
    params.append('start_time',test_plan.value.start_time)
    params.append('end_time',test_plan.value.end_time)
    params.append('state',test_plan.value.state)
    params.append('remark',test_plan.value.remark)
    params.append('class_id',categoryId.value)
    params.append('questionList','['+test_plan.value.questionList.toString()+']')
    try{
        await request.post('http://localhost:8080/test/createTest',params)
        
        resultShow.value = true;
        selectQuestion.value=false;
    }catch(error){
        ElMessage.error('测评计划标题重复，请重置')
        // console.error(error)
    }
    
    
}


const baseInfo = ref(true)
const selectQuestion = ref(false)
const resultShow = ref(false)

// .............................................................................
// 题目列表处理。。。。。。
import {useQuestionStore} from '@/stores/question.js'
import {useDateStore} from '@/util/date.js'
import {usepageStore} from '@/util/page.js'
import {useTestPlanStore} from '@/stores/testPlan.js'
const testPlanStore = useTestPlanStore()
const questionStore = useQuestionStore()
const dateStore = useDateStore()
const pageStore = usepageStore()
// 当前页要展示的数据
const tableData = ref([])
// pageData格式：{0:{},1:{},2:{},....}
const pageNum = ref(1)//当前页
const total = ref(0)//总条数
const pageSize = ref(3)//每页条数
// 点击题目搜索时触发
const getQuestions = async(course,keyword)=>{
    if(test_plan.value.class_id==''){
        ElMessage.error("请选择班级")
        return
    }
    if(test_plan.value.title==''){
        ElMessage.error("请输入标题")
        return
    }
    let right = await testPlanStore.isRepeatTitle(test_plan.value.title,test_plan.value.class_id)
    if(right){
        ElMessage.error("标题已存在，请重新填写")
        return
    }

    // console.log(course)

    let questionList =  await questionStore.querryQuestion(course,keyword)
    
    for(let i in questionList){
        let time = questionList[i].create_time
        
        time = dateStore.formatDateBytimestamp(time)
        
        questionList[i].create_time = time
        questionList[i].added = false
    }
    tableData.value = pageStore.init(questionList,pageSize.value)
    total.value = pageStore.total
    baseInfo.value=false;
    selectQuestion.value=true;
}
//当每页条数发生了变化，调用此函数
const onSizeChange = (size) => {
    pageSize.value = size
    pageStore.setPageSize(size)
    pageNum.value = 1
    tableData.value = pageStore.indexPageData(pageNum.value)
}
//当前页码发生变化，调用此函数
const onCurrentChange = (num) => {
    pageNum.value = num
    tableData.value = pageStore.indexPageData(num)
}

const addToPlan = (row)=>{
    // console.log('row',row.id)
    test_plan.value.questionList.push(row.id)
    row.added = true
    // console.log('questionList',test_plan.value.questionList)
}
const deleteFromPlan = (row)=>{
    test_plan.value.questionList=test_plan.value.questionList.filter(item => item !== row.id);
    row.added = false
    console.log('questionList',test_plan.value.questionList)
}
// 智能组卷
const autoAddToPlan=()=>{
    // 根据班级内的学生学科能力，让大模型去选择题目
}




const checkTitle = ()=>{
    return test_plan.value.title!=''
}
//定义表单校验规则
const rules = {
    title: [
        { validator:checkTitle, message: '请输入标题', trigger: 'blur' }
    
    ],
    class_id: [
        { required: true, message: '选择班级', trigger: 'blur' }
    ]
}

</script>

<template>

<!-- 测评计划信息填写 -->
<el-form v-model="test_plan" v-if="baseInfo"  :rules="rules">
    <el-form-item label="标题" prop="title">
        <el-input  placeholder="请输入标题" v-model="test_plan.title"></el-input>
    </el-form-item>
    <el-form-item label="发布班级" prop="class_id">
                <el-select  v-model="categoryId" style="width: 240px" @change="test_plan.class_id=categoryId">
                    <el-option 
                        v-for="key,value in categorys" 
                        :key="key" 
                        :label="key"
                        :value="value">
                    </el-option>
                </el-select>
    </el-form-item>
    <el-form-item label="日期" >
        <el-date-picker
          v-model="date"
          type="date"
          placeholder="请选择日期"
        />
    </el-form-item>
    <el-form-item label="时间选择">
        <el-time-picker
            v-model="value2"
            is-range
            arrow-control
            range-separator="To"
            start-placeholder="Start time"
            end-placeholder="End time"
        />
    </el-form-item>
    
    <el-form-item label="备注">
        <el-input name="remark" placeholder="请输入备注" v-model="test_plan.remark"></el-input>
    </el-form-item>
    <br>
    <el-form-item>
        <el-button type="primary" @click="getQuestions(semesterStore.classID_course[categoryId])">
            下一步，选择题目
        </el-button>
    </el-form-item>
</el-form>

<!-- 挑选题目 -->
<el-card class="page-container" v-if="selectQuestion">
        
        <!-- 搜索表单 -->
        <el-form inline>
            <el-form-item>
                <el-input v-model="keyword" placeholder="请输入关键字"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="getQuestions(categoryId,keyword)">搜索</el-button>
                <el-button @click="keyword=''">重置</el-button>
                <el-button @click="baseInfo=true;selectQuestion=false">上一步</el-button>
                <el-button type="primary" plain @click="">智能一键组卷</el-button>
                <el-button type="success" @click="submitTest_plan()">提交测评计划</el-button>
            </el-form-item>
        </el-form>
        <!-- 题目列表 -->
        <el-table :data="tableData" style="width: 100%;" >
            
                <el-table-column  label="题目id" prop="id" editable>
                    
                </el-table-column>
                <el-table-column  label="难度" prop="mu" editable>
                    <template #default="{ row }">
                        <span
                  class="demonstration"
                >{{ (row.mu >= 20 && row.mu < 30 )? 
                '正常':row.mu >= 0 && row.mu <20 ? 
                '简单':row.mu >= 30 && row.mu < 50 ?
                 '较难': row.mu >= 50 && row.mu < 70 ?
                  '困难':'难出天际'}}</span>
                    </template>
                    
                </el-table-column>
                <el-table-column  label="问题" prop="Q">
                   
                </el-table-column>
            
                <el-table-column  label="选项A" prop="A"> 
                    
                </el-table-column>
                <el-table-column  label="选项B" prop="B">
                    
                </el-table-column>
                <el-table-column  label="选项C" prop="C">
                   
                </el-table-column>
                <el-table-column  label="选项D" prop="D"> 
                    
                </el-table-column>
                <el-table-column  label="答案" prop="answer">
                    
                </el-table-column>
                <el-table-column  label="创建时间" prop="create_time"> 
                    
                </el-table-column>
                <el-table-column  label="操作" width="100">
                    <template #default="{ row }">
                        <el-button  type="primary" @click="addToPlan(row)" v-if="!row.added">添加</el-button>
                        <el-button  type="danger" @click="deleteFromPlan(row)" v-if="row.added">删除</el-button>
                    </template>
                </el-table-column>
                <template #empty>
                    <el-empty description="没有数据"/>
                </template>
           
        </el-table>
        <!-- 分页条 -->
        <el-pagination v-model:current-page="pageNum" v-model:page-size="pageSize" :page-sizes="[3, 5 ,10, 15]"
            layout="jumper, total, sizes, prev, pager, next" background :total="total" @size-change="onSizeChange"
            @current-change="onCurrentChange" style="margin-top: 20px; justify-content: flex-end" />
    </el-card>
    <el-result
        icon="success"
        title="提交成功"
        v-if="resultShow"
      >
        <template #extra>
          <el-button type="primary" @click="baseInfo=true;resultShow=false">返回</el-button>
        </template>
      </el-result>

</template>

<style scoped>

.is-selected {
  color: #1989fa;
}

.demo-range .el-date-editor {
  margin: 8px;
}

.demo-range .el-range-separator {
  box-sizing: content-box;
}
.page-container {
    min-height: 100%;
    box-sizing: border-box;

    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
}
.column{
    height:100px;
}

</style>



















