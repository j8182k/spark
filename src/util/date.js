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
    const formateToTimestep = (datetimeStr)=>{
        // const datetimeStr = '2024年6月25日 9时51分36秒';

        // 使用正则表达式解析日期时间字符串
        const regex = /(\d{4})年(\d{1,2})月(\d{1,2})日 (\d{1,2})时(\d{1,2})分(\d{1,2})秒/;
        const match = datetimeStr.match(regex);

        if (match) {
            const year = parseInt(match[1], 10);
            const month = parseInt(match[2], 10) - 1; // JavaScript的月份从0开始
            const day = parseInt(match[3], 10);
            const hour = parseInt(match[4], 10);
            const minute = parseInt(match[5], 10);
            const second = parseInt(match[6], 10);

            // 创建 Date 对象
            const date = new Date(year, month, day, hour, minute, second);

            // 获取毫秒级时间戳并转换为秒级时间戳
            const timestampInSeconds = Math.floor(date.getTime() / 1000);

            // console.log(timestampInSeconds); // 输出时间戳
            return timestampInSeconds
        } else {
            console.error('Invalid date format');
        }
    }
    const getCurrentTimestep = ()=>{
      return Math.floor(Date.now() / 1000);
    }
    const compareDate = (date1,date2)=>{
        // Convert inputs to Date objects if they are not already
          const d1 = new Date(date1);
          const d2 = new Date(date2);

          // Get the timestamp of each date
          const time1 = d1.getTime();
          const time2 = d2.getTime();

          // Compare the timestamps
          if (time1 < time2) {
              return -1;
          } else if (time1 > time2) {
              return 1;
          } else {
              return 0;
          }
    }
    return {formatDate,formatDateBytimestamp,formateToTimestep,getCurrentTimestep}

},{persist:true})
