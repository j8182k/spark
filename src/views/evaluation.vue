<script  setup>
import { ref,onMounted } from 'vue'
import request from '@/util/request.js'
import { useQuestionStore } from '@/stores/question.js'
import { useUserStore } from '@/stores/userInfo'
import { ElMessageBox,ElMessage} from 'element-plus'
import * as echarts from "echarts";

const userStore = useUserStore()
const questionStore = useQuestionStore()
// 首先选择课程，系统根据课程和用户能力查找题目
const courseList = ref({})
// 当前题目
const test_q = ref({
    id:'',
    Q:'',
    A:'',
    B:'',
    C:'',
    D:'',
    user_answer:'',
    answer:'',
    right:false
})
const isLoading = ref(false)
// 题目数量
const q_num = ref(5)
// 题目索引
let q_index = 0
// 题目列表 
const questionList = ref([])
// 课程选择
const selected = ref("机器学习")
// 组件展示
const courseisShow = ref(true)
const testisShow = ref(false)
const rsShow = ref(false)
const isDisabled = ref(false)
const  timestampToTime=(timestamp, format)=> {
  const date = new Date(timestamp);
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  const hour = date.getHours().toString().padStart(2, '0');
  const minute = date.getMinutes().toString().padStart(2, '0');
  const second = date.getSeconds().toString().padStart(2, '0');
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hour)
    .replace('mm', minute)
    .replace('ss', second);
}
onMounted(async()=>{
    questionStore.clear()
    rsShow.value = false 
    courseList.value = await questionStore.getCourse()
    
    charts(userStore.info.username,courseList.value[0])
    
    
})
const charts= async(username,course)=>{
        let record = await questionStore.getHistoryQ(username,course)
        // console.log(record)
        let times = []
        let accuracy = []
        for(let key in record){
            times.push(key)
        }
        times.sort()

        let points = []
        console.log('时间')
        console.log(times)
        for(let i in times){
            points.push(i)
            let right = 0
            let wrong = 0
            let record_line = record[times[i]]
            
            for(let j in record_line){
                
                if(record_line[j].right){
                    right++;
                }else{
                    wrong++;
                }
            }
            accuracy.push(right/(right+wrong))
        }
        var dom = document.getElementById("container");
        var myChart = echarts.init(dom, null, {
            renderer: "canvas",
            useDirtyRect: false,
        });
        var option;
        option = {
            title: {
            text: selected.value+"正确率曲线图："
            },
            xAxis: {
            type: "category",
            data: points,
            },
            yAxis: {
            type: "value",
            // data:['0%','5%','10%','15%','20%','25%','30%'],[150, 230, 224, 218, 135, 147, 260]
            },
            series: [
            {
                smooth: true,
                data: accuracy,
                type: "line",
            },
            ],
        };

        if (option && typeof option === "object") {
            myChart.setOption(option);
        }
}
const setTest_q = (data)=>{
    test_q.value.id = data.question_id
    test_q.value.Q = data.Q
    test_q.value.A = data.A
    test_q.value.B = data.B
    test_q.value.C = data.C
    test_q.value.D = data.D
    test_q.value.answer = data.answer
    // console.log('test_q.value',test_q.value)
}
const getQuestion = async()=>{
    if(Object.keys(selected.value).length === 0){
        ElMessage.error("请选择课程")
        return
    }
    //学生能力加载
    userStore.setSkill(selected.value)
    // 测评题目加载
    let rs = await questionStore.getQuestionByCourse(selected.value,userStore.info.username,q_num.value)
    //答题历史初始化
    questionStore.initHistory(rs)
    questionList.value = rs
    courseisShow.value = false
    // console.log('questionList',questionList)
    setTest_q(questionList.value[0])
    q_index = 0
    testisShow.value = true
    
}
const indexQuestion=(index)=>{
    // console.log("切换题目前的测试题信息");
    // console.log(test_q.value)
    //切换题目之前保存答案
    if(test_q.value['user_answer']!=''){
        questionStore.addRecord(test_q.value['user_answer'],test_q.value.id)
    }
    test_q.value['user_answer'] = ''
    // 取新题目
    let question =  questionList.value[index]
    setTest_q(question)
    test_q.value.user_answer = questionStore.q_history[test_q.value.id]
}
const nextQuestion=()=>{
    if(q_index == questionList.value.length-1){
        ElMessage.error("这是最后一题")
        return
    }
    q_index = q_index + 1
    indexQuestion(q_index)
    judge()
}
const priorQuestion=()=>{
    if(q_index == 0){
        ElMessage.error("这是第一题")
        return
    }
    q_index = q_index - 1
    indexQuestion(q_index)
    judge()
}
// 答案对比
const judge = ()=>{
    test_q.value.right = test_q.value.user_answer == test_q.value.answer
    return test_q.value.right
}

//答案提交
const submit= async()=>{
    questionStore.addRecord(test_q.value['user_answer'],test_q.value.id)
    let response =  await questionStore.submit(userStore.info.username,selected.value)
    if(response != 1){
        rsShow.value = true
        isDisabled.value = true
    }

}
const shiftCourse = ()=>{
    // console.log('selected',selected)
    charts(userStore.info.username,selected.value)
}
const stopTest = ()=>{
    location.reload();
}
</script>
<template>
    <div class="center"><h1>智化测评系统</h1></div>
    <!-- 选课程 -->
<div v-loading="isLoading">


  <div v-if="courseisShow">
        <h1>课程选择</h1>
        <el-radio-group  v-model="selected" size="large">
        <el-radio-button v-for="(value,key) in courseList" :key="key" v-bind:label="value" v-bind:value="value" @mouseout="shiftCourse" />
        </el-radio-group>
        <!-- 题目数量选择 -->
       
        <div class="slider-demo-block" >
            <span>题目数量</span>
            <el-slider style="width: 500px;" v-model="q_num" show-input />
        </div>
            <!-- <el-slider style="width: 500px;" v-model="q_num" :step="1" show-stops />
            <span class="demonstration">题目数量</span> -->
      
        <!-- 曲线图表 -->
        <div id="container" style="height: 300px"></div>
        <el-button  style="margin-left:45%;margin-top: 5%;display: grid;" type="primary" @click="getQuestion">开始测评</el-button>
  </div>
  <!-- 答题 -->
  <div v-if="testisShow">
  
        <!-- 开始答题后显示 -->
        <!-- <h1>总共{{questionStore.q_len}}道题，这是第{{ q_index+1 }}题 </h1>  -->
        <div style="margin-left:1200px">
            <el-button type="danger" @click="stopTest" plain>结束测评</el-button>
        </div>
          <!-- 答题进度条 -->
        <div class="demo-progress">
                <div>答题进度：</div><el-progress :text-inside="true" :stroke-width="26" :percentage="(((q_index+1)/questionList.length)*100).toFixed(0)" />
        </div>
       
        <div v-if="rsShow">
            <!-- 答案提交后显示 -->
            <h1 style="color:red">本题结果：{{ test_q.right?"正确":"错误" }}</h1>
            
            <el-button :type="primary" link>题目分析</el-button>
        </div>
        <!-- 题目 -->
        <h1>Id{{ test_q.id}}:{{test_q.Q }}</h1>
        <el-radio-group  v-model="test_q.user_answer" class="group" @mouseout="judge" :disabled="isDisabled">
        <el-radio class="select" label="A" value="A" size="large" border>A{{ test_q.A }}</el-radio>
        <el-radio class="select" label="B" value="B" size="large" border>B{{ test_q.B }}</el-radio>
        <el-radio class="select" label="C" value="C" size="large" border>C{{ test_q.C }}</el-radio>
        <el-radio class="select" label="D" value="D" size="large" border>D{{ test_q.D }}</el-radio>
        </el-radio-group>
        <div class="buttons">
            <!-- 底部功能按钮 -->
            <el-button @click="priorQuestion" type="primary">上一题</el-button>
            <el-button @click="submit" type="success" :disabled="isDisabled">提交答案</el-button>
            <el-button @click="nextQuestion" type="primary">下一题</el-button>
       
        </div>
    </div>
</div>
</template>

<style scoped>
.group{
   display: grid;
   
}
.select{
    margin-top: 10px;
    width: 80vw;
}
.buttons{
    margin-top: 10px;
    margin-left: 30%;
}

.center {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 0vh; /* 视口高度 */
}

.demo-progress .el-progress--line {
  margin-top: 20px;
  margin-bottom: 15px;
  max-width: 600px;
}

.slider-demo-block {
  margin-top: 10px;
  margin-bottom: 10px;
  max-width: 600px;
  display: flex;
  align-items: center;
}
.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}

</style>
