
<script setup>
import {
    Delete
} from '@element-plus/icons-vue'

import { ref,onMounted } from 'vue'

import {useDateStore} from '@/util/date.js'
import {usepageStore} from '@/util/page.js'

import { useEvaluationStore } from '@/stores/evaluation'
import { useUserStore } from '@/stores/userInfo'


const dateStore = useDateStore()

const evaluationStore = useEvaluationStore()
const pageStore = usepageStore()
const userStore = useUserStore()

onMounted(()=>{
   initData()
})

// 当前页要展示的数据
const tableData = ref([])
// pageData格式：{0:{},1:{},2:{},....}
const pageNum = ref(1)//当前页
const total = ref(0)//总条数
const pageSize = ref(3)//每页条数

const initData = async()=>{


    let plan_rs_list = await evaluationStore.get_plan_rs(userStore.info.username)

    console.log('plan_rs_list',plan_rs_list)

    // 设置表格数据
    tableData.value = pageStore.init(plan_rs_list,pageSize.value)
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


</script>
<template>

    <el-card class="page-container">
        
        <!-- 搜索表单 -->
        <el-form inline>
            <el-form-item>
                <h1>测评结果查看</h1>
            </el-form-item>
        </el-form>
        <!-- 测评结果显示 -->
        <el-table :data="tableData">
            
                <el-table-column  label="id" prop="id" editable>
                    
                </el-table-column>
                <el-table-column  label="标题" prop="TITLE" editable>
                    
                </el-table-column>
                <el-table-column  label="班级" prop="class_name">
                   
                </el-table-column>
                <el-table-column  label="科目" prop="course">
                    
                </el-table-column>
                <el-table-column  label="能力值变化" prop="mu_change">
                    <template #default="{ row }">
                        {{ (row.mu-row.pre_mu).toFixed(2) }}
                    </template>
                    
                </el-table-column>
                <el-table-column  label="薄弱知识点" prop="break_knowledge">
                    
                </el-table-column>
                <el-table-column  label="学习方案" prop="scheme">
                    
                </el-table-column>
                <el-table-column  label="完成时间" prop="CREATE_TIME"> 
                    <template #default="{ row }">
                        
                        <span>{{ dateStore.formatDateBytimestamp(row.CREATE_TIME) }}</span>
                        
                    </template>
                </el-table-column>
                
                <!-- <el-table-column  label="操作" width="100">
                    <template #default="{ row }">
                        
                        <el-button :icon="Delete" @click="" circle plain type="danger"></el-button>
                    </template>
                </el-table-column> -->
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
    
    box-sizing: border-box;

    .header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
}
.column{
    height:50px;
}

</style>




