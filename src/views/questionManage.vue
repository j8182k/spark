
<script setup>
import {
    Delete
} from '@element-plus/icons-vue'

import { ref,onMounted } from 'vue'
import {useQuestionStore} from '@/stores/question.js'
import {useDateStore} from '@/util/date.js'
import {usepageStore} from '@/util/page.js'
const questionStore = useQuestionStore()
const dateStore = useDateStore()
const pageStore = usepageStore()
//分类数据模型
const categorys = ref({})

//用户搜索时选中的分类id
const categoryId=ref('')

const keyword = ref('')
onMounted(()=>{
   initData()
})

// 当前页要展示的数据
const tableData = ref([])
// pageData格式：{0:{},1:{},2:{},....}
const pageNum = ref(1)//当前页
const total = ref(0)//总条数
const pageSize = ref(3)//每页条数
// 点击题目搜索时触发
const getQuestions = async(course,keyword)=>{
    let questionList =  await questionStore.querryQuestion(course,keyword)
    
    for(let i in questionList){
        let time = questionList[i].create_time
        
        time = dateStore.formatDateBytimestamp(time)
        
        questionList[i].create_time = time
    }
    tableData.value = pageStore.init(questionList,pageSize.value)
    total.value = pageStore.total
    
}
const initData = async()=>{
    categorys.value = await questionStore.getCourse()
    categoryId.value = categorys.value[0]
    getQuestions(categoryId.value)
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
    pageNum.value = 1//当前页
    total.value = 0//总条数
    pageSize.value = 3//每页条数

}

const valueInput = (row, column)=>{
    questionStore.updateQuestion(JSON.stringify(row))
}
const deleteQ = async(row)=>{
    await questionStore.deleteQuestion(JSON.stringify(row))
    initData()
}
let tableRowEditId = ref(null) // 控制可编辑的每一行
let tableColumnEditIndex = ref(null) //控制可编辑的每一列

const showUnitInput = (row, column) => {
  //赋值给定义的变量
  tableRowEditId.value = row.id //确定点击的单元格在哪行 如果数据中有ID可以用ID判断，没有可以使用其他值判断，只要能确定是哪一行即可
  tableColumnEditIndex.value = column.id //确定点击的单元格在哪列 
}
</script>
<template>

    <el-card class="page-container">
        
        <!-- 搜索表单 -->
        <el-form inline>
            <el-form-item label="课程：">
                <el-select  v-model="categoryId" placeholder="请选择" style="width: 240px" @change="getQuestions(categoryId,keyword)">
                    <el-option 
                        v-for="key,value in categorys" 
                        :key="key" 
                        :label="key"
                        :value="key">
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-input v-model="keyword" placeholder="请输入关键字"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="getQuestions(categoryId,keyword)">搜索</el-button>
                <el-button @click="reload()">重置</el-button>
                <!-- <el-button @click="upLoadQ" type="success" >上传题目</el-button> -->
            </el-form-item>
        </el-form>
        <!-- 题目列表 -->
        <el-table :data="tableData" :edit="true" style="width: 100%;"  @cell-click="showUnitInput">
            
                <el-table-column  label="题目id" prop="id" editable>
                    
                </el-table-column>
                <el-table-column  label="难度" prop="mu" editable>
                    
                </el-table-column>
                <el-table-column  label="问题" prop="Q">
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            v-model="row.Q"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                            @input="valueInput(row, column)"
                        />
                        <span v-else>{{ row.Q }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="知识点" prop="knowledge">
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            v-model="row.knowledge"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                            @input="valueInput(row, column)"
                        />
                        <span v-else>{{ row.knowledge }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="选项A" prop="A"> 
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            @input="valueInput(row, column)"
                            v-model="row.A"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                        />
                        <span v-else>{{ row.A }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="选项B" prop="B">
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            @input="valueInput(row, column)"
                            v-model="row.B"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                        />
                        <span v-else>{{ row.B }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="选项C" prop="C">
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            @input="valueInput(row, column)"
                            v-model="row.C"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                        />
                        <span v-else>{{ row.C }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="选项D" prop="D"> 
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            @input="valueInput(row, column)"
                            v-model="row.D"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                        />
                        <span v-else>{{ row.D }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="答案" prop="answer">
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            @input="valueInput(row, column)"
                            v-model="row.answer"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                        />
                        <span v-else>{{ row.answer }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="创建时间" prop="create_time"> 
                    
                </el-table-column>
                <el-table-column  label="操作" width="100">
                    <template #default="{ row }">
                        <!-- <el-button :icon="Edit" circle plain type="primary"></el-button> -->
                        <el-button :icon="Delete" @click="deleteQ(row)" circle plain type="danger"></el-button>
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




