
<script setup>
import {
    Delete,
    Check
} from '@element-plus/icons-vue'

import { ref,onMounted } from 'vue'
import { usepageStore } from '@/util/page.js'
import { useTestPlanStore } from '@/stores/testPlan'
import { useSemesterStore } from '@/stores/semester';
import { useUserStore } from '@/stores/userInfo';
import { useDateStore } from '@/util/date.js'
import { ElMessage,ElMessageBox } from 'element-plus';
const dateStore = useDateStore()
const semesterStore = useSemesterStore()
const userStore = useUserStore()

const testPlanStore = useTestPlanStore()
const pageStore = usepageStore()
//分类数据模型
const categorys = ref({

})

//用户搜索时选中的分类id
const categoryId=ref('')

const keyword = ref('')
onMounted(()=>{
   initData()
})
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
    categoryId.value = data[0].id.toString()
    getTestList(data[0].id)

}
// 当前页要展示的数据
const tableData = ref([])
// pageData格式：{0:{},1:{},2:{},....}
const pageNum = ref(1)//当前页
const total = ref(0)//总条数
const pageSize = ref(10)//每页条数
// 点击题目搜索时触发
const getTestList = async(class_id)=>{
    // console.log(class_id)
    let testList = await testPlanStore.getTestList(class_id)
    tableData.value = pageStore.init(testList,pageSize.value)
    total.value = pageStore.total
    
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
// 数据发生变化时更新展示
const reload = ()=>{
    let current_page = pageNum.value

    getTestList(categoryId.value)
    onCurrentChange(current_page)
}
const isLoading = ref(false);
const valueInput = async(row)=>{
    // questionStore.updateQuestion(JSON.stringify(row))   更新
    let new_plan = row

    // console.log("new_plan",new_plan)
    let start = dateStore.formateToTimestep(new_plan.START_TIME)
    let end = dateStore.formateToTimestep(new_plan.END_TIME)
    if(end-start<=0){
        ElMessage.error("开始时间晚于结束时间，请重置")
        initData()
        return
    }
    await testPlanStore.updateTestPlan(new_plan)
    reload()
   
}
const release = async(row)=>{
    row.STATE = 1
    await testPlanStore.updateTestPlan(row)
    reload()
}
const deletePlan = async(row)=>{
    //退出登录
    ElMessageBox.confirm(
        '您确认要删除该计划吗?',
        '温馨提示',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then( async() => {
            await testPlanStore.deletePlan(row.id)
            reload()
            ElMessage({
                type: 'success',
                message: '删除成功',
            })
            
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '用户取消了删除',
            })
        })
    
}
let tableRowEditId = ref(null) // 控制可编辑的每一行
let tableColumnEditIndex = ref(null) //控制可编辑的每一列

const showUnitInput = (row, column) => {
  //赋值给定义的变量
  tableRowEditId.value = row.id //确定点击的单元格在哪行 如果数据中有ID可以用ID判断，没有可以使用其他值判断，只要能确定是哪一行即可
  tableColumnEditIndex.value = column.id //确定点击的单元格在哪列 
}
const filterState = (value, row, column)=> {
      return row.STATE === value;
}
</script>
<template>

    <el-card class="page-container" v-loading="isLoading">
        
        <!-- 搜索表单 -->
        <el-form inline>
            <el-form-item label="班级">
                <el-select  v-model="categoryId" placeholder="请选择" style="width: 240px" @change="getTestList(categoryId)">
                    <el-option 
                        v-for="key,value in categorys" 
                        :key="key" 
                        :label="key"
                        :value="value">
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
            
                <el-table-column  label="id" prop="id">
                    
                </el-table-column>
                <el-table-column  label="标题" prop="TITLE">
                    
                </el-table-column>
                <el-table-column  label="开始时间" prop="START_TIME">
                    <template #default="{ row, column }">
                        <el-date-picker
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id && row.STATE==0"
                            v-model="row.START_TIME"
                            format="YYYY年MM月DD日 HH时mm分ss秒"
                            value-format="YYYY年MM月DD日 HH时mm分ss秒"
                            type="datetime"
                            :default-value="new Date()"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                        />
                        
                    </template>
                </el-table-column>
                <el-table-column  label="结束时间" prop="END_TIME">
                    <template #default="{ row, column }">
                        <el-date-picker
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id&& row.STATE==0"
                            v-model="row.END_TIME"
                            format="YYYY年MM月DD日 HH时mm分ss秒"
                            value-format="YYYY年MM月DD日 HH时mm分ss秒"
                            type="datetime"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                            
                        />
                        
                    </template>
                </el-table-column>
                <el-table-column  label="创建时间" prop="CREATE_TIME"> 
                    
                </el-table-column>
                <el-table-column  
                label="状态" 
                prop="STATE"
                :filters="[{ text: '未发布', value: 0 }, { text: '已发布', value: 1 }]"
                :filter-method="filterState"
                filter-placement="bottom-end"
                >
                    <template #default="{ row, column }">
                        <span >{{ row.STATE==0?'未发布':'已发布' }}</span>
                    </template>
                    
                </el-table-column>
                <el-table-column  label="备注" prop="REMARK">
                    <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id&& row.STATE==0"
                            v-model="row.REMARK"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                            
                        />
                        <span v-else>{{ row.REMARK }}</span>
                    </template>
                </el-table-column>
                <el-table-column  label="操作" width="200">
                    <template #default="{ row }">
                        <el-button size="small" @click="valueInput(row)" v-if="row.STATE==0">保存</el-button>
                        <el-button size="small" @click="release(row)" type="success" v-if="row.STATE==0">发布</el-button>
                        <el-button :icon="Delete" @click="deletePlan(row)" circle plain type="danger" ></el-button>

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




