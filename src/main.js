// import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router'
import ElementPlus from "element-plus"
import 'element-plus/dist/index.css'
import {createPinia} from 'pinia'
import { createPersistedState } from 'pinia-persistedstate-plugin'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
const pinia = createPinia()
const persist = createPersistedState()
pinia.use(persist)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }

app.use(pinia)

app.use(router)
app.use(ElementPlus)
app.mount('#app')
