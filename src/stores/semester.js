import {defineStore} from 'pinia'
import {ref} from 'vue'
import request from '@/util/request.js'
import { ElMessage, ElMessageBox } from 'element-plus'
import {useTokenStore} from '../stores/token.js'

export const useSemesterStore = defineStore('semester',()=>{
    

    const addSemester = async(name,course,teacher)=>{
        const params = new FormData();
        params.append('name',name)
        params.append('course',course)
        params.append('teacher',teacher)
        try{
            const response = await request.post('http://localhost:8080/addSemesters',params)
            let data = response.data
            return data
        }catch(error){
            console.error(error)
        }
    }
    const deleteSemester = async(semesterId)=>{
        const params = new FormData();
        params.append('semesterId',semesterId)
       
        try{
            const response = await request.post('http://localhost:8080/deleteSemesters',params)
            let data = response.data
            return data
        }catch(error){
            console.error(error)
        }
    }
    const getSemester = async(teacher)=>{
        const params = new FormData();
        params.append('teacher',teacher)
        try{
            const response = await request.post('http://localhost:8080/getSemesters',params)
            let data = response.data
            return data
        }catch(error){
            console.error(error)
        }
    }

    const addSutdents = async(semesterId,student)=>{
        const params = new FormData();
        params.append('student',student)
        params.append('semesterId',semesterId)
        // console.log(student,semesterId)
        try{
            const response = await request.post('http://localhost:8080/addStudents',params)
            let data = response.data
            return data
        }catch(error){
            console.error(error)
        }
    }
    const deleteStudent = async(username,semesterId)=>{
       
        const params = new FormData();
        params.append('username',username)
        params.append('semesterId',semesterId)
        try{
            const response = await request.post('http://localhost:8080/deleteStudentsFromSemester',params)
            let data = response.data
            return data
        }catch(error){
            console.error(error)
        }
    }
    const getSutdents = async(semesterId)=>{
        const params = new FormData();
        params.append('semesterId',semesterId)
        try{
            const response = await request.post('http://localhost:8080/getStudents',params)
            let data = response.data
            return data
        }catch(error){
            console.error(error)
        }
    }

    const suggestions = async(semesterId,queryString)=>{
        const params = new FormData();
        params.append('semesterId',semesterId);
        params.append('queryString',queryString);
        try{
            const response = await request.post('http://localhost:8080/suggestionStudent',params)
            let data = response.data
            return data
        }catch(error){
            console.error(error)
        }
    }
    const searchStudents = async(semesterId,queryString)=>{
        const params = new FormData();
        params.append('semesterId',semesterId);
        params.append('nickname',queryString);
        // console.log(semesterId,queryString)
        try{
            const response = await request.post('http://localhost:8080/searchStudent',params)
            let data = response.data
            return data
        }catch(error){
            console.error(error)
        }
    }



    return {getSemester,getSutdents,addSutdents,suggestions,deleteStudent,searchStudents,addSemester,deleteSemester}

},{persist:true})
