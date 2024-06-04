import {defineStore} from 'pinia'
import {ref} from 'vue'
import {ElMessage,ElMessageBox} from 'element-plus'
export const usepageStore = defineStore('page',()=>{
    
    // 页大小
    const pageSize = ref(3)
    // 页数
    const pageNum = ref()
    // 总记录条数
    const total = ref()
    // 数据，必须是列表
    const data = ref([])
    // 当前页
    const currentPage = ref(1)

    const setPageSize = (size)=>{
        pageSize.value = size
    }
    const setCurrentPage = (index)=>{
        currentPage.value = index
    }
    const setData = (datas)=>{
        // console.log('datas',datas)
        data.value = data.value.concat(datas)
        total.value = Object.keys(datas).length
        pageNum.value = Math.ceil(total.value/pageSize.value)
    }

    const init = (datas,size)=>{
        clear()
        setPageSize(size)
        setData(datas)
        // console.log('size',size)
        let rs = indexPageData(currentPage.value)
        // console.log('rs',rs)
        return rs
    }
    const indexPageData = (index)=>{
        currentPage.value = index
        let first_index = (index -1)* pageSize.value 
        // 当前页数据
        let currentData = []
        for(let t = 1;t<=pageSize.value&&(t+first_index)<=total.value;t++){
            currentData.push(data.value[t+first_index-1])
        }
        // console.log('currentData',currentData)
        return currentData
    }
    const nextPage = ()=>{
        if(currentPage.value >= pageNum ){
            ElMessage.error('这是最后1页')
            return indexPageData(currentPage.value)
        }else{
            currentPage.value ++
            return indexPageData(currentPage.value)
        }
    }
    const frontPage = ()=>{
        if(currentPage.value <= 1 ){
            ElMessage.error('这是第1页')
            return indexPageData(currentPage.value)
        }else{
            currentPage.value --
            return indexPageData(currentPage.value)
        }
    }
    

    const clear = ()=>{
            // 页大小
        pageSize.value = 3
        // 页数
        pageNum.value = 0
        // 总记录条数
        total.value = 0
        // 数据，必须是列表
        data.value = []
        // 当前页
        currentPage.value = 1

    }
    return {init,indexPageData,nextPage,frontPage,setCurrentPage,setPageSize,pageSize,pageNum,total,data,currentPage}

},{persist:true})
