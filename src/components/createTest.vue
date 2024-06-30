<!-- 测评计划创建 -->
<script setup>
import { ref,onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { defineProps } from 'vue';
// import DatePicker from 'vue-date-picker';

// 定义接收的属性

const props = defineProps({

  formData: {
    type: Object, // 或者 String, Number 等，根据你的数据类型来定
    // required默认为false，这里可以省略，若需要必填可明确指定required: true
  }

});
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
    class_id:props.formData,
    start_time:'',
    end_time:'',
    state: 0,
    remark:'',
    questionList:[]
})

const submitTest_plan = async()=>{
    if(test_plan.value.title==''){
        ElMessage.error('请输入标题')
        return
    }
    test_plan.value.start_time = combineDateAndTime(date.value,value2.value[0])
    test_plan.value.end_time = combineDateAndTime(date.value,value2.value[1])
    // console.log('date',date)
    console.log('test_plan',test_plan)
    const params = new FormData();
    params.append('title',test_plan.value.title)
    params.append('start_time',test_plan.value.start_time)
    params.append('end_time',test_plan.value.end_time)
    params.append('state',test_plan.value.state)
    params.append('remark',test_plan.value.remark)
    params.append('class_id',test_plan.value.class_id)
    try{
        const response = await request.post('http://localhost:8080/test/createTest',params)
        
        console.log('desc',response.desc)
           
    }catch(error){
        console.error(error)
    }
    
}




</script>

<template>

<el-form v-model="test_plan">
    <el-form-item label="标题">
        <el-input name="title" placeholder="请输入标题" v-model="test_plan.title"></el-input>
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
        <el-button type="primary" @click="submitTest_plan">
            发布
        </el-button>
    </el-form-item>
</el-form>


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

</style>



















