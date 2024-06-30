<script setup>
import {
    Service
} from '@element-plus/icons-vue'
import { ref, onMounted,nextTick, computed, watch } from "vue";
import { ElMessage } from "element-plus";
import io from 'socket.io-client';
import { useChatStore } from '@/util/chat.js';
import { useUserStore } from "@/stores/userInfo";

const userStore = useUserStore()
const chatStore = useChatStore()
const question = ref(""); //输入框值
const chatList = ref([]); //循环的聊天数组
const scrollbarRef = ref(null);
const socket = ref(null);
const clear  = ()=>{
  question.value = ""
  chatList.value = []
  scrollbarRef.value = null
  socket.value = null
}
const init= ()=>{
  socket.value = io('http://localhost:8080');
  let question = chatStore.getPreQuestion()
  console.log('获取question',question)
  askClick(question)
}
onMounted(() => {
  clear()
  init()
});
const messagesWithTimestamps = computed(() => {
  return chatList.value.map((item, index) => ({
    ...item,
    showTime: index === 0 || shouldShowTime(index),
  }));
});
const shouldShowTime = (index) => {
  const current = new Date(chatList.value[index - 1].timestamp);
  const next = new Date(chatList.value[index].timestamp);
  const diff = next ? next - current : 0;
  return diff > 3 * 60 * 1000; // 如果间隔超过3分钟返回true
};
const isLoading = ref(false);
const askClick = async (val) => {
  if (val !== "") {
    question.value = "";
    isLoading.value = true;
    const answer = await chatStore.chat(val);
    chatList.value.push({
      question: val, // 问题
      answer: answer, // 回答
      timestamp: new Date(), // 时间戳
      to: "", // 接收者
      from: "", // 发送者
    });
    isLoading.value = false;
    scrollToBottom();
  } else {
    ElMessage("不能发送空白消息");
  }
};
const scrollToBottom = () => {
  nextTick(() => {
    const scrollRef = scrollbarRef.value;
    if (scrollRef) {
      
      scrollRef.wrapRef.scrollTop = scrollRef.wrapRef.scrollHeight;;
    }
  });
};
watch(
  chatList,
  () => {
    scrollToBottom();
  },
  { deep: true }
);
const formatSendTime = (sendTime) => {
  const now = new Date();
  const sendDate = new Date(sendTime);
  const timeDiff = now - sendDate;
  const startOfToday = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate()
  );
  const startOfTargetDate = new Date(
    sendDate.getFullYear(),
    sendDate.getMonth(),
    sendDate.getDate()
  );
  const oneDay = 24 * 60 * 60 * 1000;
  if (timeDiff < 0) {
    return "Invalid time";
  }
  if (startOfToday.getTime() === startOfTargetDate.getTime()) {
    return formatTime(sendDate);
  }
  if (timeDiff < oneDay) {
    return "昨天 " + formatTime(sendDate);
  }
  if (timeDiff < 7 * oneDay) {
    const weekday = getWeekday(sendDate);
    return weekday + " " + formatTime(sendDate);
  }
  return (
    sendDate.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    }) +
    " " +
    formatTime(sendDate)
  );
};

const formatTime = (date) => {
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  return hours + ":" + minutes;
};

const getWeekday = (date) => {
  const weekdays = [
    "星期天",
    "星期一",
    "星期二",
    "星期三",
    "星期四",
    "星期五",
    "星期六",
  ];
  return weekdays[date.getDay()];
};
import {useRouter} from 'vue-router'
const router = useRouter();

const back = ()=>{
    router.push('/history')
}


</script>
<template>
  <el-button type="primary" class="btn" @click="back()">返回</el-button>
  <el-container style="height: 100%" ref="bodyform">
    <div class="el_main_content">
      <div class="main_content_header">智能答疑</div>
      <div class="main_content_center">
        <el-scrollbar
          class="faultExpertConsultation_scrollbar"
          ref="scrollbarRef"
        >
          <!--对话内容-->
          <div
            v-for="(item, index) in messagesWithTimestamps"
            :key="index"
            v-show="messagesWithTimestamps.length > 0"
          >
            <!--对话时间-->
            <div v-if="item.showTime" class="chat_time">
              {{ formatSendTime(item.timestamp) }}
            </div>
            <!--提问-->
            <div class="question chat">
              <div class="chat_question chat_common">
                <span>{{ item.question }}</span>
              </div>
              <el-avatar class="avatar">
                <span class="me">我</span>
              </el-avatar>
            </div>
            <!--回答-->
            <div class="answer chat" v-if="item.answer">
              <el-avatar :icon="Service" />
              <div class="chat_answer chat_common">
                <span>{{ item.answer }}</span>
              </div>
            </div>
          </div>
        </el-scrollbar>
      </div>
      <div class="main_content_footer">
        <div class="input_box">
          <textarea class="chat-input no-border" v-model="question" />
        </div>
        <div class="btn_box" v-loading="isLoading">
          <el-button type="primary" class="btn" @click="askClick(question);">发送</el-button>
        </div>
      </div>
    </div>
  </el-container>
</template>
<style>
.no-border {
  border: none;
  /* 可选的样式，以去除焦点时的边框（如果需要的话） */
  outline: none;
  width: none;
  height: none;
  resize: none;
}
</style>
 
<style lang="less" scoped>
.el_main_content {
  width: 50%;
  height: 90%;
  border-radius: 5px;
  border: 1px solid #e4e7ed;
  box-shadow: 0px 0px 12px rgba(0, 0, 0, 0.12);
  margin: auto;
 
  .main_content_header {
    width: 100%;
    height: 50px;
    border-radius: 5px;
    background-color: #f2f2f2;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
  }
 
  .main_content_center {
    width: 100%;
    position: relative;
    height: calc(100% - 170px);
    margin: 10px 0px;
 
    .chat_time {
      display: flex;
      justify-content: center;
      font-size: 10px;
    }
    .question {
      justify-content: flex-end;
    }
    .chat_question {
      background-color: #8ce45f;
      margin-right: 5px;
      color: #ffffff;
    }
    .chat_answer {
      background-color: #f2f3f5;
      margin-left: 5px;
    }
    .chat {
      width: 98%;
      margin: 10px auto;
      display: flex;
    }
    .chat_common {
      max-width: 40%;
      padding: 10px;
      border-radius: 2px;
      word-break: break-all;
      display: flex;
      align-items: center;
    }
    .avatar {
      background-color: #409eff;
      border: 2px solid #409eff;
    }
    .me {
      font-size: 16px;
      color: #ffffff;
      font-weight: bold;
    }
  }
 
  .main_content_footer {
    width: 100%;
    height: 100px;
    border-top: 1px solid #e4e7ed;
    .input_box {
      width: 100%;
      height: 60px;
      .chat-input {
        width: calc(100% - 20px);
        padding: 10px;
        margin: auto;
      }
    }
    .btn_box {
      width: 100%;
      height: 40px;
      display: flex;
      justify-content: flex-end;
      align-items: center;
      .btn {
        margin-right: 10px;
      }
    }
  }
}
</style>