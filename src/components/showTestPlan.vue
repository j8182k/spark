
<script setup>
import {
    Delete
} from '@element-plus/icons-vue'

import { ref,onMounted } from 'vue'
import {useQuestionStore} from '@/stores/question.js'
import {useDateStore} from '@/util/date.js'
import {usepageStore} from '@/util/page.js'
import { useTestPlanStore } from '@/stores/testPlan'
const questionStore = useQuestionStore()
const dateStore = useDateStore()
const testPlanStore = useTestPlanStore()
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
const getTestList = async(class_id)=>{
    
    let testList = await testPlanStore.getTestList(class_id)
    tableData.value = pageStore.init(testList,pageSize.value)
    total.value = pageStore.total
    
}
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



const valueInput = (row, column)=>{
    // questionStore.updateQuestion(JSON.stringify(row))   更新

}
const deleteQ = async(row)=>{
    
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
            <el-form-item label="班级">
                <el-select  v-model="categoryId" placeholder="请选择" style="width: 240px" @change="getTestList(categoryId)">
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
                <el-button type="primary" @click="">搜索</el-button>
                <el-button @click="keyword=''">重置</el-button>
            </el-form-item>
        </el-form>
        <!-- 测评计划显示 -->
        <el-table :data="tableData" :edit="true" style="width: 100%;"  @cell-click="showUnitInput">
            
                <el-table-column  label="id" prop="id" editable>
                    
                </el-table-column>
                <el-table-column  label="标题" prop="title" editable>
                    
                </el-table-column>
                <el-table-column  label="开始时间" prop="start_time">
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            v-model="row.start_time"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                            @input="valueInput(row, column)"
                        />
                        <span v-else>{{ row.start_time }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="结束时间" prop="end_time">
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            v-model="row.end_time"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                            @input="valueInput(row, column)"
                        />
                        <span v-else>{{ row.end_time }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="创建时间" prop="create_time"> 
                    
                </el-table-column>
                <el-table-column  label="状态" prop="state">
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            v-model="row.state"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                            @input="valueInput(row, column)"
                        />
                        <span v-else>{{ row.state==0?'未发布':'已发布' }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="备注" prop="remark">
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            v-model="row.remark"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                            @input="valueInput(row, column)"
                        />
                        <span v-else>{{ row.remark }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="操作" width="100">
                    <template #default="{ row }">
                        <!-- <el-button :icon="Edit" circle plain type="primary"></el-button> -->
                        <el-button :icon="Delete" @click="" circle plain type="danger"></el-button>
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




