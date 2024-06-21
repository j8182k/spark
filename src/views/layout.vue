<script setup>
import {
    Management,
    Promotion,
    User,
    Crop,
    EditPen,
    SwitchButton,
    CaretBottom
} from '@element-plus/icons-vue'
import {useTokenStore} from '@/stores/token.js'
import {useUserStore} from '@/stores/userInfo.js'
import { ref,onMounted } from 'vue'
const userStore = useUserStore()
const tokenStore = useTokenStore()
const isStudent = ref(false)
const isTeacher = ref(false)
//条目被点击后,调用的函数
import {useRouter} from 'vue-router'
const router = useRouter();
import {ElMessage,ElMessageBox} from 'element-plus'


onMounted(()=>{
    let type = userStore.info.type
    if(type === 'teacher'){
        isTeacher.value = true
    }else{
        isStudent.value = true
    }
})

const handleCommand = (command)=>{
    //判断指令
    if(command === 'logout'){
        //退出登录
        ElMessageBox.confirm(
        '您确认要退出吗?',
        '温馨提示',
        {
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            type: 'warning',
        }
    )
        .then(async () => {
            tokenStore.removeToken()
            //2.跳转到登录页面
            router.push('/')

            ElMessage({
                type: 'success',
                message: '退出登录成功',
            })
            
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '用户取消了退出登录',
            })
        })
    }else{
        //路由
        router.push(command)
    }
}
</script>

<template>
    <!-- element-plus中的容器 -->
    <el-container class="layout-container">
        <!-- 左侧菜单 -->
        <el-aside width="200px">
            <div class="el-aside__logo"></div>
            <!-- element-plus的菜单标签 -->
            <el-menu active-text-color="#ffd04b" background-color="#232323"  text-color="#fff"
                router>
                <!-- <el-sub-menu >
                    <template #title>
                        <el-icon>
                            <UserFilled />
                        </el-icon>
                        <span>知识库管理</span>
                    </template>
                    <el-menu-item index="/chatByFiles">
                        <el-icon>
                            <User />
                        </el-icon>
                        <span>知识库问答</span>
                    </el-menu-item>
                    <el-menu-item index="/upLoad">
                        <el-icon>
                            <Crop />
                        </el-icon>
                        <span>知识文本上传</span>
                    </el-menu-item>
                </el-sub-menu> -->
                <el-menu-item index="/evaluation" v-if="isStudent">
                    <el-icon>
                        <Management />
                    </el-icon>
                    <span>智能测评</span>
                </el-menu-item>
               
                <el-menu-item index="/errorQuestion" v-if="isStudent">
                    <el-icon>
                        <User />
                    </el-icon>
                    <span>错题集</span>
                </el-menu-item>
                <el-menu-item index="/history" v-if="isStudent">
                    <el-icon>
                        <Management />
                    </el-icon>
                    <span>答题记录</span>
                </el-menu-item>
                <el-menu-item index="/imgRec" v-if="isTeacher">
                    <el-icon>
                        <Promotion />
                    </el-icon>
                    <span>上传题目</span>
                </el-menu-item>
                <el-menu-item index="/questionManage" v-if="isTeacher">
                    <el-icon>
                        <Promotion />
                    </el-icon>
                    <span>题目管理</span>
                </el-menu-item>
                <el-menu-item index="/semesterManage" v-if="isTeacher">
                    <el-icon>
                        <Promotion />
                    </el-icon>
                    <span>班级管理</span>
                </el-menu-item>
            </el-menu>
        </el-aside>
        <!-- 右侧主区域 -->
        <el-container>
            <!-- 头部区域 -->
            <el-header>
                <div>{{userStore.info.type=="student"?"学生":"老师"}}：<strong>{{ userStore.info.nickname }}</strong></div>
                <!-- 下拉菜单 -->
                <!-- command: 条目被点击后会触发,在事件函数上可以声明一个参数,接收条目对应的指令 -->
                <el-dropdown placement="bottom-end" @command="handleCommand">
                    <span class="el-dropdown__box">
                        <el-avatar
                                src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                        />
                        <el-icon>
                            <CaretBottom />
                        </el-icon>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item command="userInfo" :icon="User">基本资料</el-dropdown-item>
                            <el-dropdown-item command="" :icon="Crop">更换头像</el-dropdown-item>
                            <el-dropdown-item command="resetPassword" :icon="EditPen">重置密码</el-dropdown-item>
                            <el-dropdown-item command="logout" :icon="SwitchButton">退出登录</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </el-header>
            <!-- 中间区域 -->
            <el-main>
                <router-view></router-view>
            </el-main>
            <!-- 底部区域  background: url('@/assets/logo.png') no-repeat center / 120px auto;-->
            <el-footer>智化教育 ©2024 Created by 嵇康做得队</el-footer>
        </el-container>
    </el-container>
</template>

<style lang="scss" scoped>
.layout-container {
    height: 100vh;

    .el-aside {
        background-color: #232323;
        margin-left: -8px;
        margin-top: -8px;
        &__logo {
            height: 120px;
            
        }

        .el-menu {
            border-right: none;
        }
    }

    .el-header {
        background-color: #fff;
        display: flex;
        align-items: center;
        justify-content: space-between;

        .el-dropdown__box {
            display: flex;
            align-items: center;

            .el-icon {
                color: #999;
                margin-left: 10px;
            }

            &:active,
            &:focus {
                outline: none;
            }
        }
    }

    .el-footer {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        color: #666;
    }
}
</style>