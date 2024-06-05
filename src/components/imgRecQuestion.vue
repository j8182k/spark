<script  setup>
import { ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import request from "@/util/request.js";
import { UploadFilled, ArrowLeft } from "@element-plus/icons-vue";
import { useQuestionStore } from "@/stores/question.js";
const fileList = ref([]);
const pictureurl = ref();
const questionStore = useQuestionStore();
const handleExceed = (files) => {
  // 清空 fileList
  fileList.value = [];

  // 获取第一个文件
  const file = files[0];

  // 生成新的文件 ID
  file.uid = Date.now() + Math.random().toString(36).substr(2, 9);

  // 将新文件添加到 fileList
  fileList.value.push(file);
  selectedFile.value = file;
  // console.log('新文件')
  // console.log(selectedFile.value)
};

const dic = ref({
  Q: "",
  A: "",
  B: "",
  C: "",
  D: "",
  answer: "",
  course: "机器学习",
  mu: 25,
  message: "",
  sigma: 8.334,
});
const setDic = (data) => {
  dic.value.Q = data.Q;
  dic.value.A = data.A;
  dic.value.B = data.B;
  dic.value.C = data.C;
  dic.value.D = data.D;
  dic.value.answer = data.answer;
  dic.value.mu = data.assess.mu;
  dic.value.message = data.assess.message;
};
const isLoading = ref(false);
// 选择要上传的文件
const selectedFile = ref();
const handleFileUpload = async (file) => {
  selectedFile.value = await file.file;
  console.log(selectedFile.value);
};
const submitForm = async () => {
  if (selectedFile.value) {
    const params = new FormData();
    params.append("img", selectedFile.value);
    // alert(selectedFile.value.name)
    try {
      isLoading.value = true;
      const response = await request.post(
        "http://localhost:8080/uploadImg",
        params,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      // console.log("response.data");
      // console.log(response.data);
      setDic(response.data);
      isLoading.value = false;
      // console.log("dic.value");
      // console.log(dic.value);
      ElMessage({
        type: "success",
        message: `图片识别成功，请按需修改`,
      });
    } catch (error) {
      console.error(error);
    }
  } else {
    alert("请选择一个图片上传");
  }
};

const Qconfirm = async () => {
  if (dic.value.Q !== "") {
    const params = new FormData();
    const s =
      '{ "Q":"' +
      dic.value.Q +
      '","A":"' +
      dic.value.A +
      '","B":"' +
      dic.value.B +
      '","C":"' +
      dic.value.C +
      '","D":"' +
      dic.value.D +
      '","answer":"' +
      dic.value.answer +
      '","course":"' +
      dic.value.course +
      '","mu":"' +
      dic.value.mu +
      '","sigma":"' +
      dic.value.sigma +
      '"}';
    params.append("question", s);

    try {
      isLoading.value = true;
      const response = await request.post(
        "http://localhost:8080/upLoadQuestion",
        params,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      isLoading.value = false;
      setTimeout(1000);
      if (response.code === "0") {
        console.log(response.data);
        ElMessage({
          type: "success",
          message: `题目上传成功`,
        });
      }
    } catch (error) {
      isLoading.value = false;
      ElMessageBox.confirm("该题目已经存在，是否生成1个类似的？", "错误", {
        confirmButtonText: "生成",
        cancelButtonText: "取消",
        type: "error",
      }).then(async () => {
        isLoading.value = true;
        const response = await questionStore.genQuestion(dic.value);
        setDic(response.data[0]);
        isLoading.value = false;
        ElMessage({
          type: "success",
          message: `新题目已生成`,
        });
      });

      // console.error(error);
    }
  } else {
    alert("没有题目");
  }
};
import { useRouter } from "vue-router";
const router = useRouter();
const back = () => {
  router.push("/questionManage");
};
</script>
<template>
  <!-- <div>

    <input type="file" @change="handleFileUpload($event)"/>
    <button @click="submitForm">上传文件</button>
  </div>-->
  <!-- <el-button type="primary" :icon="ArrowLeft" @click="back">返回</el-button> -->

  <el-card class="boxcard" v-loading="isLoading">
    <div class="card-wrapper">
      <el-card class="leftcard">
        <div class="upload">
          <label style="font-weight: bolder;font-size: 18px;">上传题目</label>
          <div style="display: flex;flex-direction: column;margin-top: 5%;">
            <div style="display: flex;">
              <el-upload
                class="upload-demo"
                drag
                action="#"
                multiple
                :limit="1"
                :file-list="fileList"
                :http-request="handleFileUpload"
                :on-exceed="handleExceed"
              >
                <el-icon class="el-icon--upload">
                  <upload-filled />
                </el-icon>
                <div class="el-upload__text">
                  把图片拖拽到此处或
                  <em>点击上传</em>
                </div>
                <template #tip>
                  <div class="el-upload__tip" style="margin-top: 3%;">
                    <span>{{'（1）像素要求：最短边至少15px，最长边最大4096px； （2）大小要求：<4MB； （3）格式要求：JPEG，PNG，BMP.'}}</span>
                  </div>
                </template>
              </el-upload>
            </div>
            <span style="text-align: center;margin: 3%;">图片文字识别选择题（可以跳过图片识别直接在上面填写题目信息）</span>
            <div style="text-align: center;">
              <el-button @click="Qconfirm" type="success" style="margin-right: 10%;">题目上传</el-button>
              <el-button @click="submitForm" type="success">识别图片</el-button>
            </div>
          </div>
        </div>
        <div style="margin-top: 5%;">
          <label style="font-weight: bolder;font-size: 18px;">展示图片</label>
          <!-- 需要后端传入图片的url地址，复制给pictureurl -->
          <div class="showpic">
            <el-image :src="pictureurl"></el-image>
          </div>
        </div>
      </el-card>
      <el-card class="rightcard">
        <label style="font-weight: bolder;font-size: 18px;">识别题目</label>
        <div class="elform" style="margin-top: 5%;">
          <el-form :label-position="top" label-width="auto" :model="dic" style="max-width: 600px;">
            <el-form-item label="问题">
              <el-input v-model="dic.Q" type="textarea" />
            </el-form-item>
            <el-form-item label="选项A">
              <el-input v-model="dic.A" type="textarea" />
            </el-form-item>
            <el-form-item label="选项B">
              <el-input v-model="dic.B" type="textarea" />
            </el-form-item>
            <el-form-item label="选项C">
              <el-input v-model="dic.C" type="textarea" />
            </el-form-item>
            <el-form-item label="选项D">
              <el-input v-model="dic.D" type="textarea" />
            </el-form-item>
            <el-form-item label="答案">
              <el-input v-model="dic.answer" type="textarea" />
            </el-form-item>
            <el-form-item label="题目类型">
              <el-input v-model="dic.course" type="textarea" value="机器学习" />
            </el-form-item>
            <el-form-item label="题目难度识别">
              <div class="slider-demo-block">
                <el-slider style="width: 500px;" v-model="dic.mu" :step="5" show-stops />
                <span
                  class="demonstration"
                >{{ (dic.mu >= 20 && dic.mu < 30 )? '正常':dic.mu >= 0 && dic.mu <20 ? '简单':dic.mu >= 30 && dic.mu < 50 ? '较难': dic.mu >= 50 && dic.mu < 70 ? '困难':'难出天际'}}</span>
              </div>
            </el-form-item>
            <el-form-item label="题目难度分析:">{{ dic.message }}</el-form-item>
          </el-form>
        </div>
      </el-card>
    </div>
  </el-card>

  <!-- <div class="center">
    <h1>上传题目</h1>
  </div>-->
  <!-- <div v-loading="isLoading" style="margin-top:3%;">
    <div style="display: flex;">
      <div style="display: flex;">
        <el-form :label-position="top" label-width="auto" :model="dic" style="max-width: 600px;">
          <el-form-item label="问题">
            <el-input v-model="dic.Q" type="textarea" />
          </el-form-item>
          <el-form-item label="选项A">
            <el-input v-model="dic.A" type="textarea" />
          </el-form-item>
          <el-form-item label="选项B">
            <el-input v-model="dic.B" type="textarea" />
          </el-form-item>
          <el-form-item label="选项C">
            <el-input v-model="dic.C" type="textarea" />
          </el-form-item>
          <el-form-item label="选项D">
            <el-input v-model="dic.D" type="textarea" />
          </el-form-item>
          <el-form-item label="答案">
            <el-input v-model="dic.answer" type="textarea" />
          </el-form-item>
          <el-form-item label="题目类型">
            <el-input v-model="dic.course" type="textarea" value="机器学习" />
          </el-form-item>
          <el-form-item label="题目难度识别">
            <div class="slider-demo-block">
              <el-slider style="width: 500px;" v-model="dic.mu" :step="5" show-stops />
              <span
                class="demonstration"
              >{{ (dic.mu >= 20 && dic.mu < 30 )? '正常':dic.mu >= 0 && dic.mu <20 ? '简单':dic.mu >= 30 && dic.mu < 50 ? '较难': dic.mu >= 50 && dic.mu < 70 ? '困难':'难出天际'}}</span>
            </div>
          </el-form-item>
          <el-form-item label="题目难度分析:">{{ dic.message }}</el-form-item>
        </el-form>
      </div>

      <div style="display: flex;flex-direction: column;margin-left: 5%;">
        <div style="display: flex;">
          <el-upload
            class="upload-demo"
            drag
            action="#"
            multiple
            :limit="1"
            :file-list="fileList"
            :http-request="handleFileUpload"
            :on-exceed="handleExceed"
          >
            <el-icon class="el-icon--upload">
              <upload-filled />
            </el-icon>
            <div class="el-upload__text">
              把图片拖拽到此处或
              <em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                <span>{{'（1）像素要求：最短边至少15px，最长边最大4096px； （2）大小要求：<4MB； （3）格式要求：JPEG，PNG，BMP.'}}</span>
              </div>
            </template>
          </el-upload>
        </div>图片文字识别选择题（可以跳过图片识别直接在上面填写题目信息）
        <div style="display: flex;">
          <el-button @click="Qconfirm" type="success">题目上传</el-button>
          <el-button @click="submitForm" type="success">识别图片</el-button>
        </div>
      </div>
    </div>
  </div>-->
</template>

<style scoped>
.center {
  display: flex;

  justify-content: center;
  align-items: center;
  height: 0vh; /* 视口高度 */
}
.slider-demo-block {
  max-width: 600px;
  display: flex;
  align-items: center;
}
.slider-demo-block .el-slider {
  margin-top: 0;
  margin-left: 12px;
}
.slider-demo-block .demonstration {
  font-size: 14px;
  /* color: var(--el-text-color-secondary); */
  color: crimson;
  line-height: 44px;
  flex: 1;
  margin-left: 10%;
  /* overflow: hidden; */
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 0;
}
.slider-demo-block .demonstration + .el-slider {
  flex: 0 0 70%;
}

.card-wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr; /* 等分宽度 */
  gap: 10px; /* 可选项，设置列之间的间隔 */
}
</style>
