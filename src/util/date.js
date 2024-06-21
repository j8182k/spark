import {defineStore} from 'pinia'

export const useDateStore = defineStore('dateformat',()=>{
    
    const formatDate = (dateStr)=> {
        // console.log('dateStr',dateStr)
        let date = null
        if(date instanceof Date){
              date = dateStr
        }else{              
              date = new Date();
              date.setTime(dateStr*1000)
              // console.log(date)
        }
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const hours = date.getHours();
        const minutes = date.getMinutes();
        const seconds = date.getSeconds();
        const chineseMonths = [
          '1月', '2月', '3月', '4月', '5月', '6月',
          '7月', '8月', '9月', '10月', '11月', '12月'
        ];
        const formattedDate = `${year}年${chineseMonths[month - 1]}${day}日 ${hours}时${minutes}分${seconds}秒`;
        return formattedDate;
      }
      
    const formatDateBytimestamp = (timestamp)=>{
      // console.log('timestamp',timestamp)
      const date = new Date(timestamp*1000)
      // console.log('date',date)
      const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const hours = date.getHours();
        const minutes = date.getMinutes();
        const seconds = date.getSeconds();
        const chineseMonths = [
          '1月', '2月', '3月', '4月', '5月', '6月',
          '7月', '8月', '9月', '10月', '11月', '12月'
        ];
        const formattedDate = `${year}年${chineseMonths[month - 1]}${day}日 ${hours}时${minutes}分${seconds}秒`;
        return formattedDate;
    }
    //   const dateStr = "Tue, 21 May 2024 10:10:21 GMT";
    //   const formattedDate = formatDate(dateStr);
    //   console.log(formattedDate); // 输出：2024年5月21日 10时10分21秒

    return {formatDate,formatDateBytimestamp}

},{persist:true})
