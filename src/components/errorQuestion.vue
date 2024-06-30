
<script setup>
import {
    Edit,
    Delete
} from '@element-plus/icons-vue'

import { ref,onMounted } from 'vue'
import {useQuestionStore} from '@/stores/question.js'
import {useErrorQuestionStore} from '@/stores/errorQ.js'
// import {useDateStore} from '@/util/date.js'
import {usepageStore} from '@/util/page.js'
import {useUserStore} from '@/stores/userInfo.js'
const userStore = useUserStore()
const questionStore = useQuestionStore()
const errorQuestionStore = useErrorQuestionStore()
const pageStore = usepageStore()
//分类数据模型
const categorys = ref({})

//用户搜索时选中的分类id
const categoryId=ref('')

//搜索关键字
const keyword = ref()
onMounted(()=>{
    initData()
})
const initData = async()=>{
    // 课程名称获取
    categorys.value = await questionStore.getCourse()
    categoryId.value = categorys.value[0]
    getQuestions(categoryId.value)

}
// 当前页要展示的数据
const tableData = ref([])
// pageData格式：{0:{},1:{},2:{},....}
const pageNum = ref(1)//当前页
const total = ref(0)//总条数
const pageSize = ref(3)//每页条数
// 点击题目搜索时触发
const getQuestions = async(course,keyword)=>{
    let username = userStore.info.username
    let errorQuestionList =  await errorQuestionStore.getErrorQuestions(username,course,keyword)
    // console.log('errorQuestionList',errorQuestionList)
    // 列表形式初始化页数据
    tableData.value = pageStore.init(errorQuestionList,pageSize.value)
    total.value = pageStore.total
    // console.log('tableData',tableData)
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

const reload = ()=>{
    location.reload();
}
const clear =()=>{
//根据课程查询到的所有题目
    // questions.value = {}
    pageNum.value = 1//当前页
    total.value = 0//总条数
    pageSize.value = 3//每页条数

}

const deleteRow = async(row)=>{
    let q_id = row.q_id
    await errorQuestionStore.deleteErrorQ(userStore.info.username,q_id)
    initData()
}

</script>
<template>

    <el-card class="page-container">
        
        <!-- 搜索表单 -->
        <el-form inline>
            <el-form-item label="课程：">
                <el-select  v-model="categoryId" placeholder="请选择" style="width: 240px">
                    <el-option 
                        v-for="key,value in categorys" 
                        :key="key" 
                        :label="key"
                        :value="key">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-input v-model="keyword" placeholder="请输入题目id"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="getQuestions(categoryId,keyword)">搜索</el-button>
                <el-button @click="reload()">重置</el-button>
                <!-- <el-button @click="upLoadQ" type="success" >上传题目</el-button> -->
            </el-form-item>
        </el-form>
        <!-- 题目列表 -->
        <el-table :data="tableData" style="width: 100%;">
            <el-table-column  label="题目id" prop="q_id">
                
            </el-table-column>
      
            <el-table-column  label="问题" prop="info.Q">

            </el-table-column>
            <el-table-column  label="选项A" prop="info.A"> 

            </el-table-column>
            <el-table-column  label="选项B" prop="info.B">

            </el-table-column>
            <el-table-column  label="选项C" prop="info.C">
                 
            </el-table-column>
            <el-table-column  label="选项D" prop="info.D"> 

            </el-table-column>
            <!-- <el-table-column  label="分析" prop="analysis"> 

            </el-table-column>
            <el-table-column  label="知识点" prop="knowledge"> 

            </el-table-column> -->
            <el-table-column  label="创建时间" prop="create_time"> 
                
            </el-table-column>
            <el-table-column  label="操作" width="100">
                <template #default="{ row }">
                    <!-- <el-button :icon="Edit" circle plain type="primary"></el-button> -->
                    <el-button :icon="Delete" circle plain type="danger" @click="deleteRow(row)"></el-button>
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
</template>
<style>
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




