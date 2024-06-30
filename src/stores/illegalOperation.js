import {defineStore} from 'pinia'
import {ref} from 'vue'
import request from '@/util/request.js'


export const useIllegalOperationStore = defineStore('IllegalOperation',()=>{
    // 违规的状态
    const state = ref(false)





    return {state}

},{persist:true})
