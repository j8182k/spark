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
import train from '@/views/train.vue'
import errorQuestion from '@/components/errorQuestion.vue'
import history from '@/components/history.vue'
import userInfo from '@/components/userInfo.vue'
import resetPassword from '@/components/resetPassword.vue'
import semesterManage from '@/views/semesterManage.vue'
import testPlan from '@/views/testPlan.vue'
import showTestPlanVue from '@/views/showTestPlan.vue'
import teacherHouse from '@/views/teacherHouse.vue'
import chatOnQuestion from '@/components/chatOnQuestion.vue'
import evaluation from '@/views/evaluation.vue'
import showEvalRsVue from '@/components/showEvalRs.vue'
//定义路由关系
// const routes = [
//     { path: '/', component: LoginVue },
//     {
//         path: '/layout', component: layout,redirect:(to, from, next) => {
//             // 假设你已经获取了用户类型，存储在变量 userType 中
//             const userStore = useUserStore()
//             const userType = userStore.info.type; // 或者 'student'
//             if (userType === 'teacher') {
//                 return '/questionManage'
//             } else if (userType === 'student') {
//                 return '/evaluation'
//             } else {
//                 return '/'
//             }
//         },children:[
//             { path:'/chat', component: chat},
//             { path:'/getQuestion', component: getQuestion },
//             { path: '/chatByFiles', component: chatByFiles },
//             { path: '/upLoad', component: upLoad },
//             { path: '/imgRec', component: imgRec },
//             { path: '/evaluation', component: evaluation },
//             { path: '/questionManage', component: questionManage },
//             { path: '/errorQuestion', component: errorQuestion },
//             { path: '/history', component: history },
//             { path: '/userInfo', component: userInfo },
//             { path: '/resetPassword', component: resetPassword },
//             { path: '/semesterManage', component: semesterManage },
//             { path: '/testPlan', component: testPlan },
//             { path: '/showTestPlan', component: showTestPlanVue },
//         ]
//     }
    
  
// ]

// 定义一个检查用户权限的函数
const checkUserPermission = (userType, allowedTypes) => {
    return (to, from, next) => {
        if (allowedTypes.includes(userType)) {
            next()
        } else {
            next('/') // 如果用户没有权限，重定向到登录页面或其他页面
        }
    }
}

const routes = [
    { path: '/', component: LoginVue },
    {
        path: '/layout', component: layout, redirect: (to) => {
            const userStore = useUserStore()
            const userType = userStore.info.type; // 获取用户类型
            if (userType === 'teacher') {
                return '/questionManage'
            } else if (userType === 'student') {
                return '/evaluation'
            } else {
                return '/'
            }
        }, children: [
            { path: '/teacherHouse', component: teacherHouse, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['teacher'])(to, from, next)
            }},
            { path: '/showEvalRsVue', component: showEvalRsVue, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['student'])(to, from, next)
            }},
            { path: '/chat', component: chat, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['student'])(to, from, next)
            }},
            { path: '/chatOnQuestion', component: chatOnQuestion, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['student'])(to, from, next)
            }},
            { path: '/getQuestion', component: getQuestion, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['student'])(to, from, next)
            }},
            { path: '/chatByFiles', component: chatByFiles, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['student'])(to, from, next)
            }},
            { path: '/upLoad', component: upLoad, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['teacher'])(to, from, next)
            }},
            { path: '/imgRec', component: imgRec, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['teacher'])(to, from, next)
            }},
            { path: '/train', component: train, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['student'])(to, from, next)
            }},
            { path: '/evaluation', component: evaluation, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['student'])(to, from, next)
            }},
            { path: '/questionManage', component: questionManage, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['teacher'])(to, from, next)
            }},
            { path: '/errorQuestion', component: errorQuestion, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['student'])(to, from, next)
            }},
            { path: '/history', component: history, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['student'])(to, from, next)
            }},
            { path: '/userInfo', component: userInfo },
            { path: '/resetPassword', component: resetPassword },
            { path: '/semesterManage', component: semesterManage, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['teacher'])(to, from, next)
            }},
            { path: '/testPlan', component: testPlan, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['teacher'])(to, from, next)
            }},
            { path: '/showTestPlan', component: showTestPlanVue, beforeEnter: (to, from, next) => {
                const userStore = useUserStore()
                const userType = userStore.info.type;
                checkUserPermission(userType, ['teacher'])(to, from, next)
            }},
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
