import { createRouter, createWebHistory } from 'vue-router'

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
//定义路由关系
const routes = [
    { path: '/login', component: LoginVue },
    {
        path: '/', component: layout,redirect:'/evaluation',children:[
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
            { path: '/resetPassword', component: resetPassword }


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
