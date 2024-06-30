<script  setup>
import { ref, onMounted } from 'vue';
import { useQuestionStore } from '@/stores/question.js';
import { useUserStore } from '@/stores/userInfo';
import { ElMessage } from 'element-plus';
import {useEvaluationStore} from '@/stores/evaluation.js'
import { useDateStore } from '@/util/date';
import faceCheck from '@/components/faceCheck.vue'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
const userStore = useUserStore();
const questionStore = useQuestionStore();
const evaluationStore = useEvaluationStore();
const dateStore = useDateStore();
const questionList = ref()
const isLoading = ref(false)
const test_q = ref({
    id: '',
    Q: '',
    A: '',
    B: '',
    C: '',
    D: '',
    user_answer: '',
    answer: '',
    right: false
});
// 当前展示题目的索引
let q_index = 0
// 当前进行测评的计划
const current_plan = ref() 



// 测评计划结果表
const plan_rs_form = ref({
  plan_id:'',
  student:userStore.info.username,
  pre_mu:'',
  mu:'',
  pre_sigma:'',
  sigma:'',
  break_knowledge:'',//薄弱知识点
  scheme:'',//推荐学习方案
  isValid:0//若人脸验证不通过，记录下来
})
const courseisShow = ref(true)
const rsShow = ref(false);
const isDisabled = ref(false);
const testisShow = ref(false)
const plan_rs_show = ref(false)
const lineData = ref([
// {CLASS_ID
// CREATE_TIME
// END_TIME
// REMARK
// START_TIME
// STATE
// TITLE
// id
// class_name
// course
// stu_state} 
])
onMounted(()=>{
    initData()
})
const initData = async()=>{
    // 获取测评计划列表
    let plan_list = await evaluationStore.getPlanList(userStore.info.username)
    // console.log('plan_list',plan_list)
    lineData.value = plan_list

}
const setTest_q = (data) => {
    test_q.value.id = data.id;
    test_q.value.Q = data.Q;
    test_q.value.A = data.A;
    test_q.value.B = data.B;
    test_q.value.C = data.C;
    test_q.value.D = data.D;
    test_q.value.answer = data.answer;
};

const indexQuestion = (index) => {
    if (test_q.value.user_answer != '') {
        questionStore.addRecord(test_q.value.user_answer, test_q.value.id);
    }
    test_q.value.user_answer = '';
    let question = questionList.value[index];
    setTest_q(question);
    // console.log("test_q",test_q.value)
    test_q.value.user_answer = questionStore.q_history[test_q.value.id];
};

const nextQuestion = () => {
    if (q_index == questionList.value.length - 1) {
        ElMessage.error("这是最后一题");
        return;
    }
    q_index = q_index + 1;
    indexQuestion(q_index);
    judge();
};

const priorQuestion = () => {
    if (q_index == 0) {
        ElMessage.error("这是第一题");
        return;
    }
    q_index = q_index - 1;
    indexQuestion(q_index);
    judge();
};
const judge = () => {
    test_q.value.right = test_q.value.user_answer == test_q.value.answer;
    return test_q.value.right;
};
// 答案提交
const submit = async () => {
    // 获取学生测评后的学科能力 
    userStore.setSkill(current_plan.value.course)
    plan_rs_form.value.mu = userStore.skill.mu
    plan_rs_form.value.sigma = userStore.skill.sigma
    // 保存最后一条答题记录
    questionStore.addRecord(test_q.value.user_answer, test_q.value.id);
    // 将答题结果上传到数据库
    let response = await questionStore.submit(userStore.info.username, current_plan.value.course);
    rsShow.value = true;
    isDisabled.value = true;
   
    // 提取答题结果记录
    let rs = response
    // console.log('答题结果rs',rs)
    // 整理错题
    let error_question_list = []
    for(let index in questionList.value){
        let  question = questionList.value[index]
        // console.log(question)
        let id = question.id
        if(!rs[id]){
          error_question_list.push(question)
        }
    }
    // console.log(error_question_list)
//     // 大模型分析错题，一个一个分析，提取学生薄弱知识点，知识点融合，生成推荐学习方案
//      // 生成测评报告，其中包括学科能力变化情况、正确率、综合薄弱知识点、综合学习方案、人脸验证是否通过
    let knowledge_all = ''
    let len=error_question_list.length
    NProgress.start()
    isLoading.value = true
    for(let q in error_question_list){
      console.log(error_question_list[q])
      let knowledge = await evaluationStore.analysisQuestion(error_question_list[q])
      knowledge_all =  knowledge_all+' '+knowledge
      let progress = (parseInt(q) + 1) / len
      NProgress.set(progress)
    }
    
  
    // console.log('薄弱知识总结knowledge_all',knowledge_all)

    
    plan_rs_form.value.break_knowledge = knowledge_all

    let scheme = await evaluationStore.genScheme(knowledge_all)

    console.log('推荐学习方案scheme',scheme)

    plan_rs_form.value.scheme = scheme
    plan_rs_show.value = true
    isLoading.value=false
    NProgress.done()
//     // 上传到后端，存入数据库
    await evaluationStore.save_plan_rs_form(JSON.stringify(plan_rs_form.value))

    ElMessage({
      type:'success',
      message:'测评结果生成'
    })
    

};


const startTest = async(index) => {
    questionStore.clear()
    // console.log(index)
    current_plan.value = lineData.value[index]
    // 获取学生测评前的学科能力 
    userStore.setSkill(current_plan.value.course)
    plan_rs_form.value.plan_id = current_plan.value.id
    plan_rs_form.value.course = current_plan.value.course
    plan_rs_form.value.class_name = current_plan.value.class_name
    plan_rs_form.value.pre_mu = userStore.skill.mu
    plan_rs_form.value.pre_sigma = userStore.skill.sigma
    let q_id_list = lineData.value[index].questionList
    // console.log(q_id_list)
    let rs = await questionStore.getQuestionByids(q_id_list);
    for(let i in rs){
      rs[i].question_id = rs[i].id
    }
    // console.log(rs)
    // 答题记录初始化
    questionStore.initHistory(rs);
    questionList.value = rs;
    courseisShow.value = false;
    setTest_q(questionList.value[0]);
    q_index = 0;
    testisShow.value = true;
    courseisShow.value = false;
    // startCamera();
};



const stopTest = () => {
    // stopCamera();
    location.reload();
};
// import { useIllegalOperationStore } from '@/stores/illegalOperation';
// const illegalOperation = useIllegalOperationStore()
// const illegalDialog = ref(false)
// setInterval(()=>{
//     let state = illegalOperation.state
//     if(state){
//         // 出现违规操作
//         illegalOperation.state = false
//         state = false
//         // illegalDialog.value = true
//     }
// },3000)



</script>
<template>
    <!-- 
        流程：
        1、查看测评计划
        2、选择测评计划
        3、开始测评
        4、答题
        5、提交答案
        6、展示测评结果
     -->
    <div class="center"><h1>数智化测评系统</h1></div>

<div v-loading="isLoading">

          <!-- 答题前显示 -->
        <div v-if="courseisShow">
          <!-- // {CLASS_ID
      // CREATE_TIME
      // END_TIME
      // REMARK
      // START_TIME
      // STATE
      // TITLE
      // id
      // class_name
      // course
      // stu_state} -->
        <!-- 展示测评计划轴 -->
          <el-timeline style="max-width: 600px" v-model="lineData">
              <el-timeline-item
              v-for="(item, index) in lineData"
              :key="index"
              :timestamp="'开始时间：'+dateStore.formatDate(item.START_TIME)"
              placement="top"
            >
              <el-card>
                <h4>标题：{{ item.TITLE }}</h4>
                <p>截止时间:{{ dateStore.formatDate(item.END_TIME) }}<el-text v-if="dateStore.getCurrentTimestep()>item.END_TIME" type="danger">已截止</el-text></p>
                
                <p>班级：{{ item.class_name }}</p>
                <p>课程：{{ item.course }}</p>
                <p>备注：{{item.REMARK}}</p>
                <el-text v-if="item.stu_state==0" type="danger">未完成 </el-text>
                <el-text v-if="item.stu_state!=0" type="success">已完成 </el-text>
    
                <el-button  
                  style="margin-left:45%;
                  margin-top: 5%;
                  display: grid;" type="primary" 
                  @click="startTest(index)" 
                  v-if="item.stu_state==0&&dateStore.getCurrentTimestep()<item.END_TIME"
                >
                开始测评
              </el-button>
              </el-card>
            </el-timeline-item>
          </el-timeline>
      
              
            
            
      
    
      <!-- <el-button  style="margin-left:45%;margin-top: 5%;display: grid;" type="primary" @click="startTest">开始训练</el-button> -->
    </div>
    <!-- 答题 -->
    <div v-if="testisShow">
        <!-- 摄像监控 -->
            <!-- <div>
                <faceCheck></faceCheck>
            </div> -->
            <!-- 开始答题后显示 -->
            <h1>总共{{questionList.length}}道题，这是第{{ q_index+1 }}题 </h1> 
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
                <!-- 薄弱知识点提取中：<el-progress :percentage="knowledge_progress" /> -->
                <!-- <el-button :type="primary" link>题目分析:</el-button> -->
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


    <!-- const plan_rs_form = ref({
  plan_id:'',
  student:userStore.info.username,
  pre_mu:'',
  mu:'',
  pre_sigma:'',
  sigma:'',
  break_knowledge:'',//薄弱知识点
  scheme:'',//推荐学习方案
  isValid:true//若人脸验证不通过，记录下来
}) -->
        <el-dialog v-model="plan_rs_show">
          <el-descriptions
              title="测评结果"
              :column="4"
              :size="size"
              direction="vertical"
              :style="blockMargin"
            >
            <el-descriptions-item label="学生">{{ userStore.info.nickname }}</el-descriptions-item>
            <el-descriptions-item label="班级">{{ plan_rs_form.class_name }}</el-descriptions-item>
            <el-descriptions-item label="学科" >{{ plan_rs_form.course }}</el-descriptions-item>
            <el-descriptions-item label="之前能力值">
                {{ plan_rs_form.pre_mu.toFixed(1) }}
            </el-descriptions-item>
            <el-descriptions-item label="本次测评能力值">
              {{ plan_rs_form.mu.toFixed(1) }}
            </el-descriptions-item>
            <el-descriptions-item label="能力值变化">
              {{ (plan_rs_form.mu-plan_rs_form.pre_mu).toFixed(2) }}
            </el-descriptions-item>
            <el-descriptions-item label="薄弱知识点">
              {{ plan_rs_form.break_knowledge }}
            </el-descriptions-item>
            <el-descriptions-item label="智能推荐学习方案">
              {{ plan_rs_form.scheme }}
            </el-descriptions-item>
        </el-descriptions>
        
        </el-dialog>
</div>





<!-- <el-dialog v-model="illegalDialog" :show-close="false" width="500">
    <template #header="{ close, titleId, titleClass }">
      <div class="my-header">
        <h4 :id="titleId" :class="titleClass">违规事件</h4>
        <el-button type="danger" @click="close">
          <el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>
        关闭
        </el-button>
      </div>
    </template>
    人脸验证失败，请重新开始测评
  </el-dialog> -->
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
