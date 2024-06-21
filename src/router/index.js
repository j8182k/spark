import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/userInfo.js'
import {ref,onMounted} from 'vue'
// const userStore = useUserStore()
// const first_view = ref()
// onMounted(()=>{
//     let typ = userStore.info.type 
//     if(typ==='student'){
//         first_view.value = '/evaluation'
//     }else{
//         first_view.value = '/questionManage'
//     }
// })
//导入组件
import LoginVue from '@/views/login.vue'
import upLoad from '@/components/upLoadFile.vue'
import chat from '@/components/chat.vue'
import questionManage from '@/views/questionManage.vue'
import chatByFiles from '@/components/chatByfile.vue'
import imgRec from '@/components/imgRecQuestion.vue'
import layout from '@/views/layout.vue'
import getQuestion from '@/components/getQuestion.vue'
import evaluation from '@/views/evaluation.vue'
import errorQuestion from '@/components/errorQuestion.vue'
import history from '@/components/history.vue'
import userInfo from '@/components/userInfo.vue'
import resetPassword from '@/components/resetPassword.vue'
import semesterManage from '@/views/semesterManage.vue'
//定义路由关系
const routes = [
    { path: '/', component: LoginVue },
    {
        path: '/layout', component: layout,redirect:(to, from, next) => {
            // 假设你已经获取了用户类型，存储在变量 userType 中
            const userStore = useUserStore()
            const userType = userStore.info.type; // 或者 'student'
            if (userType === 'teacher') {
                return '/questionManage'
            } else if (userType === 'student') {
                return '/evaluation'
            } else {
                return '/'
            }
        },children:[
            { path:'/chat', component: chat},
            { path:'/getQuestion', component: getQuestion },
            { path: '/chatByFiles', component: chatByFiles },
            { path: '/upLoad', component: upLoad },
            { path: '/imgRec', component: imgRec },
            { path: '/evaluation', component: evaluation },
            { path: '/questionManage', component: questionManage },
            { path: '/errorQuestion', component: errorQuestion },
            { path: '/history', component: history },
            { path: '/userInfo', component: userInfo },
            { path: '/resetPassword', component: resetPassword },
            { path: '/semesterManage', component: semesterManage },


        ]
    }
    
  
]
//创建路由器
const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

//导出路由
export default router
