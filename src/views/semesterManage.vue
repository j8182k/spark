<script setup>
import {
    Delete
} from '@element-plus/icons-vue'

import { ref,onMounted } from 'vue'

import {usepageStore} from '@/util/page.js'
import { useUserStore } from '@/stores/userInfo'
import { useSemesterStore } from '@/stores/semester';
const semesterStore =  useSemesterStore()
const userStore = useUserStore()
const pageStore = usepageStore()
//分类数据模型
const categorys = ref({
    // id:字符串
})

//用户搜索时选中的分类id
const categoryId=ref('')
// const categoryValue=ref('')
const keyword = ref('')
onMounted(()=>{
   initData()
})

// 当前页要展示的数据
const tableData = ref([])
// pageData格式：{0:{},1:{},2:{},....}
const pageNum = ref(1)//当前页
const total = ref(0)//总条数
const pageSize = ref(10)//每页条数

// 获取列表数据----》班里的学生
const getTableData = async()=>{
    // console.log('categoryId',categoryId)
    let semesterId = categoryId.value
    let students = await semesterStore.getSutdents(semesterId)
    // console.log('students',students)
    tableData.value = pageStore.init(students,pageSize.value)
    total.value = pageStore.total
    
}

const setTableData = async(data)=>{
    tableData.value = pageStore.init(data,pageSize.value)
    total.value = pageStore.total
}



const initData = async()=>{
    
    let data = await semesterStore.getSemester(userStore.info.username)
    categorys.value = {}
    for(let i in data){
        semesterStore.classID_course[data[i].id] = data[i].course
        categorys.value[data[i].id]=data[i].name+'('+data[i].course+')'
        
    }
    // console.log('classID_course',semesterStore.classID_course)
    categoryId.value = data[0].id.toString()
    getTableData()

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



const deleteRow = async(row)=>{
    await semesterStore.deleteStudent(row.username,categoryId.value)
    initData()
}
let tableRowEditId = ref(null) // 控制可编辑的每一行
let tableColumnEditIndex = ref(null) //控制可编辑的每一列

const showUnitInput = (row, column) => {
  //赋值给定义的变量
  tableRowEditId.value = row.id //确定点击的单元格在哪行 如果数据中有ID可以用ID判断，没有可以使用其他值判断，只要能确定是哪一行即可
  tableColumnEditIndex.value = column.id //确定点击的单元格在哪列 
}
const dialogFormVisible = ref(false)
const dialogFormVisible1 = ref(false)
const dialogFormVisible2 = ref(false)
const new_student = ref()

const querySearch = async(queryString, cb)=>{
    if(!queryString || queryString.length==0){
        return 
    }
    let suggestionStudent = await semesterStore.suggestions(categoryId.value,queryString)
    let suggestions = []
    for(let i in suggestionStudent){
        let nickname = suggestionStudent[i].nickname
        let username = suggestionStudent[i].username
        let val = nickname+'('+username+')'
        suggestions.push({value:val})
    }
    cb(suggestions)
}
// 搜索框查询
const querySearchs = async(queryString)=>{
   
    let studentData = await semesterStore.searchStudents(categoryId.value,queryString)
    
    setTableData(studentData)

}
const addStudent = async(semesterid,username1)=>{
    let str = username1
    // 用户名必须是数字
    const regex = /\((\d+)\)/;
    const match = str.match(regex);
    
    username1 = match ? match[1] : null;
    
    await semesterStore.addSutdents(semesterid,username1)
    getTableData()
}
const new_class = ref({
    name:'',
    course:''
})
const createClass = async()=>{
    let teacher = userStore.info.username
    await semesterStore.addSemester(new_class.value.name,new_class.value.course,teacher)
    initData()
}
const centerDialogVisible = ref(false)
const deleteSemester = async()=>{
    let semesterId = categoryId.value
    await semesterStore.deleteSemester(semesterId)
    initData()
}

import createTest from '@/components/createTest.vue'



</script>
<template>

    <el-card class="page-container">
        
        <!-- 搜索表单 -->
        <el-form inline>
            <el-form-item label="班级：">
                <el-select  v-model="categoryId" style="width: 240px" @change="getTableData">
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
                <el-button type="primary" @click="querySearchs(keyword)">搜索</el-button>
                <el-button plain @click="dialogFormVisible = true">
                    添加学生
                </el-button>
                <el-button plain @click="dialogFormVisible1 = true">
                    创建班级
                </el-button>
                <el-button type="danger" @click="centerDialogVisible=true">
                    删除当前班级
                </el-button>
                <!-- <el-button type="success" @click=" dialogFormVisible2 = true">
                    发布测评计划
                </el-button> -->
                <el-dialog v-model="dialogFormVisible" title="添加学生" width="500">
                            <el-form-item label="班级">
                                    <el-select  v-model="categoryId" placeholder="请选择" style="width: 240px">
                                        <el-option 
                                            v-for="key,value in categorys" 
                                            :key="key" 
                                            :label="key"
                                            :value="value">
                                        </el-option>
                                    </el-select>
                            </el-form-item>
                    <!-- 输入姓名时出现多个选项 -->
                            <el-form :model="new_student" v-if="!(categoryId=='')" style="margin-top: 5px;">
                                <el-form-item label="姓名">
                                    <el-autocomplete
                                        v-model="new_student"
                                        :fetch-suggestions="querySearch"
                                        placeholder="请输入姓名"
                                        @select="handleSelect"
                                    />
                                </el-form-item>
                            
                            </el-form>
                            <template #footer>
                                <div class="dialog-footer">
                                    <el-button @click="dialogFormVisible = false">取消</el-button>
                                    <el-button type="primary" @click="dialogFormVisible = false;addStudent(categoryId,new_student);new_student=''">
                                    添加
                                    </el-button>
                                </div>
                            </template>
                </el-dialog>
                <el-dialog v-model="dialogFormVisible1" title="创建班级" width="500">
                            <!-- 旧班级展示 -->
                            <el-form-item 
                                    v-for="key,value in categorys" 
                                    :key="key"
                                    :label="key"
                                    :value="value"
                            >
                            </el-form-item>
                            <br>
                            <el-form-item label="新班级名称">
                                <el-input v-model="new_class.name"></el-input>
                            </el-form-item>
                            <el-form-item label="科目" style="margin-top: 5px;">
                                <el-input style="margin-left: 42px;" v-model="new_class.course"></el-input>
                            </el-form-item>
                            <template #footer>
                                <div class="dialog-footer">
                                    <el-button @click="dialogFormVisible1 = false">取消</el-button>
                                    <el-button type="primary" @click="dialogFormVisible1 = false;createClass();new_class={name:'',course:''}">
                                    创建班级
                                    </el-button>
                                </div>
                            </template>
                </el-dialog>
                <el-dialog v-model="centerDialogVisible" title="!警告!" width="500" center>
                    <span>
                        请确定是否删除 "{{ categorys[categoryId] }}"
                    </span>
                    <template #footer>
                    <div class="dialog-footer">
                        <el-button @click="centerDialogVisible = false">取消</el-button>
                        <el-button type="primary" @click="deleteSemester();centerDialogVisible = false">
                            确定
                        </el-button>
                    </div>
                    </template>
                </el-dialog>
                <!-- <el-dialog v-model="dialogFormVisible2" title="发布测评计划" width="500">
                           <createTest :formData="categoryId"></createTest>
                </el-dialog> -->
            </el-form-item>
        </el-form>
        <!-- 学生列表 -->
        <el-table :data="tableData" :edit="true" style="width: 100%;"  @cell-click="showUnitInput">
            
                <el-table-column  label="学号" prop="username" editable>
                    
                </el-table-column>
                <el-table-column  label="姓名" prop="nickname" editable>
                    
                </el-table-column>
                <el-table-column  label="性别" prop="gender">
                    <!-- <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            v-model="row.gender"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                            @input="valueInput(row, column)"
                        />
                        <span v-else>{{ row.gender }}</span>
                    </template> -->
                </el-table-column>
                <el-table-column  label="年龄" prop="age">
                    <!-- <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            v-model="row.age"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                            @input="valueInput(row, column)"
                        />
                        <span v-else>{{ row.age }}</span>
                    </template> -->
                </el-table-column>
                <el-table-column  label="电话" prop="phone"> 
                    <!-- <template #default="{ row, column }">
                        <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            @input="valueInput(row, column)"
                            v-model="row.phone"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                        />
                        <span v-else>{{ row.phone }}</span>
                    </template> -->
                </el-table-column>
                <el-table-column  label="学科能力值" prop="mu">
                    <template #default="{ row, column }">
                        <!-- <el-input
                            v-if="
                            tableRowEditId === row.id &&tableColumnEditIndex === column.id"
                            @input="valueInput(row, column)"
                            v-model="row.mu"
                            type="textarea"
                            :autosize="{ minRows: 2, maxRows: 100 }"
                        /> -->
                        <span>{{ row.mu.toFixed(2) }}</span>
                    </template>
                </el-table-column>
                
                <el-table-column  label="操作" width="100">
                    <template #default="{ row }">
                        
                        <el-button :icon="Delete" @click="deleteRow(row)" circle plain type="danger"></el-button>
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

