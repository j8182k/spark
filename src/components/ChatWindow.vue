<template>
    <div class="chat-window">
      <!-- 显示聊天消息的容器 -->
      <div class="message-container">
        <div v-for="message in messages" :key="message.id" class="message">
          <div v-if="message.isMe" class="message-text mine">{{ message.text }}</div>
          <div v-else class="message-text">{{ message.text }}</div>
        </div>
      </div>
      <!-- 输入消息的表单 -->
      <form @submit.prevent="sendMessage" class="input-form">
        <input v-model="inputText" type="text" placeholder="输入消息" />
        <button type="submit">发送</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        inputText: '',
        messages: [
          { id: 1, text: '你好', isMe: false },
          { id: 2, text: 'Hi', isMe: true },
        ],
      };
    },
    methods: {
      sendMessage() {
        if (this.inputText.trim()) {
          this.messages.push({ id: Date.now(), text: this.inputText, isMe: true });
          this.inputText = '';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .chat-window {
    max-width: 400px;
    margin: 0 auto;
  }
  
  .message-container {
    margin-bottom: 10px;
  }
  
  .message {
    padding: 5px;
    margin-bottom: 5px;
  }
  
  .message-text {
    padding: 10px;
    border-radius: 5px;
  }
  
  .mine {
    background-color: lightblue;
  }
  </style>
  