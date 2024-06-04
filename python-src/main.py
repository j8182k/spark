# -*- coding:utf-8 -*-
import hashlib
import base64
import hmac
import time
import json
import requests
from api.Document_Q_And_A import chatByfile
from flask import Flask, jsonify, request
from flask_cors import CORS
# import sparkAPI
from api import sparkAPI, imgApi
# import imgApi
# import Question
# import User
from questionManage import Questions as Question
from questionManage import QuestionHistory, ErrorQuestions
from user import User
import jwt
from functools import wraps

# 全局变量-----知识库文本
globals()['fileDict'] = {}
app = Flask(__name__)
# 允许跨域
CORS(app)
app.config['SECRET_KEY'] = 'ni shuo de dou hen dui'


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 前端要在请求头中添加 'Authorization'：token
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            # 解析令牌
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS384')
            # {'username': 'HuxinYue', 'exp': 1715404962.597749}
            # print(data)
            print("通过验证")
        except:
            # token过期，抛出异常
            print("token过期")
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated_function


class Document_Upload:
    def __init__(self, APPId, APISecret, timestamp):
        self.APPId = APPId
        self.APISecret = APISecret
        self.Timestamp = timestamp

    def get_origin_signature(self):
        m2 = hashlib.md5()
        data = bytes(self.APPId + self.Timestamp, encoding="utf-8")
        m2.update(data)
        checkSum = m2.hexdigest()
        return checkSum

    def get_signature(self):
        # 获取原始签名
        signature_origin = self.get_origin_signature()
        # 使用加密键加密文本
        signature = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha1).digest()
        # base64密文编码
        signature = base64.b64encode(signature).decode(encoding='utf-8')
        return signature

    def get_header(self):
        signature = self.get_signature()
        header = {
            "appId": self.APPId,
            "timestamp": self.Timestamp,
            "signature": signature
        }
        return header


# 四项选择题格式化
def Q_format(s):
    list1 = s.split('\n')
    # 去掉空字符串
    if '' in list1:
        list1.remove('')
    list1[0] = '.' + list1[0].split('.')[1]
    dic = {
        'Q': '',
        'A': '',
        'B': '',
        'C': '',
        'D': '',
        'answer': ''
    }
    for i in range(len(list1)):
        # 去除空格防止误判
        list1[i] = list1[i].strip()
        # 拼接
        if i + 1 < len(list1):
            # 下一行开头不是字母，将当前行拼接到下一行
            if list1[i + 1][0] not in ['A', 'B', 'C', 'D']:
                list1[i + 1] = list1[i] + list1[i + 1]
                i += 1
                continue
        if list1[i][0] == 'A':
            dic['A'] = list1[i][1::]
        elif list1[i][0] == 'B':
            dic['B'] = list1[i][1::]
        elif list1[i][0] == 'C':
            dic['C'] = list1[i][1::]
        elif list1[i][0] == 'D':
            dic['D'] = list1[i][1::]
        else:
            # 答案有可能是多项
            j = -1
            # 截取答案
            while -j <= len(list1[i]) and list1[i][j] in ['A', 'B', 'C', 'D']:
                j -= 1
            dic['Q'] = list1[i][:j + 1:]
            dic['answer'] = list1[i][j + 1::]
    return dic


def initFileDict():
    fileDict = {}
    with open('file_list.txt', 'r') as file:
        for line in file:
            if line == '\n':
                continue
            # .strip()移除字符串头尾的空白字符
            name = line.strip().split(':')[0]
            id = line.strip().split(':')[1]
            fileDict[name] = id
    globals()['fileDict'] = fileDict


def showFiles():
    print('目前知识库中的文本如下：')
    with open('file_list.txt', 'r') as file:
        for line in file:
            if line == '\n':
                continue
            # .strip()移除字符串头尾的空白字符
            print(line.strip().split(':')[0])


@app.route('/login', methods=['POST'])
def login():
    type = request.form.get('type')
    # print(type)
    username = request.form.get('username')
    # print(username)
    password = request.form.get('password')
    # print(password)
    print(type, username, password)
    rs = User.login(type, username, password)
    if rs == '密码正确':
        # 生成token,有效期是1小时,加密算法是RS384
        token = jwt.encode({'username': username, 'exp': time.time() + 60 * 60 * 1}, app.config['SECRET_KEY'],
                           algorithm='HS384')
        return jsonify({"code": "0", "desc": "密码正确", "data": token})
    elif rs == '没有该用户':
        return jsonify({"code": "1", "desc": "没有该用户", "data": username})
    return jsonify({"code": "1", "desc": "密码错误", "data": username})


# 更新用户信息
@app.route('/updateInfo', methods=['POST'])
@login_required
def updateInfo():
    userInfo = request.form.get('userInfo')
    # 提交更新信息
    new_password = request.form.get('new_password')
    if new_password is None or new_password == 'undefined':
        code = User.updataInfo(userInfo)
    else:
        code = User.updatePassword(userInfo, new_password)
    if code == 1:
        return jsonify({"code": "1", "desc": "密码重复", "data": ''})
    return jsonify({"code": "0", "desc": "成功", "data": ''})


# 上传文件
@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    files = request.files['files']
    print(files.filename)
    APPId = "f27a5eb0"
    APISecret = "NDllMTIxNzBmZjEwNGY2NzEwMGIzNWQ5"
    curTime = str(int(time.time()))
    document_upload = Document_Upload(APPId, APISecret, curTime)
    headers = document_upload.get_header()
    request_url = "https://chatdoc.xfyun.cn/openapi/fileUpload"
    body = {
        "url": "",
        "fileName": files.filename,
        "fileType": "wiki",
        "needSummary": False,
        "stepByStep": False,
        "callbackUrl": "your_callbackUrl"
    }
    response = requests.post(request_url, files={'file': (files.filename, files)}, data=body, headers=headers)

    string = response.content.decode('utf-8')  # 使用UTF-8编码进行解码
    # 将字符串转换成键值对
    dic_str = json.loads(string)
    with open("file_list.txt", "a") as file:
        file.write(files.filename + ':' + dic_str['data']['fileId'] + '\n')
    initFileDict()
    return jsonify({"code": dic_str['code'], "desc": dic_str['desc'], "data": dic_str['data']})


# 直接问答
@app.route('/chatBytext', methods=['POST'])
@login_required
def chatBytext():
    question = request.form.get('question')
    answer = sparkAPI.chatAPI(question)
    # print(answer)
    return jsonify({"code": "0", "desc": "成功", "data": answer})


# 文本问答
@app.route('/chatOnfiles', methods=['POST'])
@login_required
def chatOnfiles():
    # 根据文本回答问题
    question = request.form.get('question')
    fileName = request.form.get('fileName')
    fileId = globals()['fileDict'][fileName]
    answer = chatByfile(fileId, question)
    return jsonify({"code": "0", "desc": "成功", "data": answer})


# 获取知识库文本
@app.route('/getFileNames', methods=['GET'])
@login_required
def getFileNames():
    return jsonify({"code": "0", "desc": "成功", "data": globals()['fileDict']})


# 图片识别
@app.route('/uploadImg', methods=['POST'])
@login_required
def uploadImg():
    img = request.files['img']
    if img is None:
        question = request.form.get('question')
        question = sparkAPI.genQuestionApi(question)
    else:
        rs = imgApi.imgRec(img)
        question = Q_format(rs)
    answer = sparkAPI.assessQuestion(question)
    question['assess'] = answer
    # print(question)
    return jsonify({"code": "0", "desc": "成功", "data": question})


@app.route('/upLoadQuestion', methods=['POST'])
@login_required
def upLoadQuestion():
    question = request.form.get('question')
    # print(question)
    dic = json.loads(question)
    # print(dic['Q'])
    if Question.insertQuestion(dic) == 0:
        return jsonify({"code": "0", "desc": "成功", "data": question})
    else:
        return jsonify({"code": "1", "desc": "题目已存在", "data": question})


@app.route('/getUserinfo', methods=['POST'])
@login_required
def getUserinfo():
    username = request.form.get('username')
    type = request.form.get('type')
    userInfo = User.queryUser(type, username)
    if userInfo == '没有该用户':
        return jsonify({"code": "1", "desc": "没有该用户", "data": userInfo})
    return jsonify({"code": "0", "desc": "用户信息", "data": userInfo})


@app.route('/getQuestions', methods=['POST'])
@login_required
def getQuestions():
    ids = request.form.get('ids')
    # print('ids',ids)
    if not (ids is None) and ids != 'undefined':
        ids = ids.split(',')
        rs = Question.queryQuestionByIds(ids)
        # print('rs',rs)
        return jsonify({"code": "0", "desc": "题目获取成功", "data": rs})
    # 题目课程
    course = request.form.get('course')
    # 学生
    username = request.form.get('username')
    # 题目数量
    num = request.form.get('num')

    if username is None or username == 'undefined':
        # 查课程中所有题目
        question_list = Question.queryQuestionByCourse(course)

        print('question_list', question_list)
    else:
        if num is None or not str.isdigit(num):
            num = 1
        num = int(num)
        # 获取测评题目
        question_list = Question.match_question(username, course, num)
    # question_list = {index:{},...}
    if question_list == 1:
        return jsonify({"code": "1", "desc": "没有查询结果", "data": ''})
    return jsonify({"code": "0", "desc": "题目获取成功", "data": question_list})


@app.route('/getCourse', methods=['GET'])
@login_required
def getCourse():
    courseDic = Question.getCourse()
    return jsonify({"code": "0", "desc": "获取课程表", "data": courseDic})


@app.route('/getUserSkill', methods=['POST'])
@login_required
def getUserSkills():
    username = request.form.get('username')
    course = request.form.get('course')
    skill = User.getSkills(username, course)
    return jsonify({"code": "0", "desc": "获取学生课程能力", "data": skill})


@app.route('/submit', methods=['POST'])
@login_required
def submit():
    q_history = request.form.get('q_history')
    username = request.form.get('username')
    course = request.form.get('course')
    rs = Question.answerHandle(username, q_history, course)
    return jsonify({"code": "0", "desc": "答案提交", "data": rs})


# 调用大模型生成题目
@app.route('/genQuestion', methods=['POST'])
@login_required
def genQuestion():
    question = request.form.get('question')
    num = request.form.get('num')
    question = json.loads(question)
    if 'id' in question:
        del question['id']
    if 'leve' in question:
        del question['leve']
    rs_dic = sparkAPI.genQuestionApi(question, num)
    return jsonify({"code": "0", "desc": "答案提交", "data": rs_dic})


# 获取答题历史记录
@app.route('/getHistory', methods=['POST'])
@login_required
def getHistory():
    course = request.form.get('course')
    username = request.form.get('username')
    record = QuestionHistory.queryHistory(username, course)
    # print(record) 格式：[{},...]
    return jsonify({"code": "0", "desc": "答题记录获取", "data": record})


# 更新题目信息
@app.route('/updateQuestion', methods=['POST'])
@login_required
def updateQuestion():
    opt = request.form.get('opt')
    question = request.form.get('question')
    if opt == '编辑':
        question = json.loads(question)
        Question.updateQuestion(question['id'], question['Q'], question['A'],
                                question['B'], question['C'], question['D'],
                                question['answer'], question['course'], question['mu'],
                                question['sigma'], question['leve'], question['knowledge'])
    elif opt == '删除':
        question = json.loads(question)
        Question.deleteQuestionById(question['id'])
    elif opt == '搜索':
        keyword = request.form.get('keyword')
        question = Question.queryQuestionById(keyword)
        if question == 1:
            course = request.form.get('course')
            question = Question.queryQuestionByQ(keyword, course)
        return jsonify({"code": "0", "desc": "题目已获取", "data": question})
    return jsonify({"code": "0", "desc": "题目已修改", "data": ''})


# 上传错题
@app.route('/addErrorQuestion', methods=['POST'])
@login_required
def addErrorQuestion():
    username = request.form.get('username')
    q_id = request.form.get('q_id')
    h_id = request.form.get('h_id')
    print(username,q_id)
    rs = ''
    if q_id is None or q_id == 'undefined':
        rs = ErrorQuestions.collectErrorQ(h_id)
    else:
        # 单题上传
        rs = ErrorQuestions.addErrorQ(username, q_id)
    if isinstance(rs,BaseException):
        return jsonify({"code": "1", "desc": "错题上传失败", "data": ''})
    else:
        return jsonify({"code": "0", "desc": "错题上传成功", "data": ''})


# 获取错题集
@app.route('/getErrorQuestion', methods=['POST'])
@login_required
def getErrorQuestion():
    username = request.form.get('username')
    course = request.form.get('course')
    errorQuestions = ErrorQuestions.queryEQ(username, course)
    if isinstance(errorQuestions,BaseException):
        return jsonify({"code": "1", "desc": "错题获取失败", "data": errorQuestions})
    print(errorQuestions)
    return jsonify({"code": "0", "desc": "错题已获取", "data": errorQuestions})


# 启动所有接口
if __name__ == '__main__':
    # 知识库文本列表初始化
    initFileDict()
    app.run(host='0.0.0.0', port=8080)

# 提交本地文件

# def get_files_and_body(self):
#     body = {
#         "url": "",
#         "fileName": self.file.name,
#         "fileType": "wiki",
#         "needSummary": False,
#         "stepByStep": False,
#         "callbackUrl": "your_callbackUrl"
#     }
#     # files = {'file': open(file_path, 'rb')}
#     return body


# ｛
#             code: "状态码",
#             desc: “结果描述”,
#             data: “数据”
# ｝
# @app.route('/estimate/fileUpload', methods=['POST', 'GET'])
# def upload():
#     APPId = "f27a5eb0"
#     APISecret = "NDllMTIxNzBmZjEwNGY2NzEwMGIzNWQ5"
#     curTime = str(int(time.time()))
#     request_url = "https://chatdoc.xfyun.cn/openapi/fileUpload"
#     file_dic = request.files
#     if len(file_dic) == 0:
#         print('没有文件')
#         return jsonify({"code": 1, "desc": "没有文件", "data": ""})
#     file = file_dic['file']
#     document_upload = Document_Upload(APPId, APISecret, curTime, file)
#     headers = document_upload.get_header()
#     body = document_upload.get_files_and_body()
#     files = {'file': file}
#     # 发起远程请求，获取响应
#     response = requests.post(request_url, files=files, data=body, headers=headers)
#     # print(response.content)
#     string = response.content.decode('utf-8')  # 使用UTF-8编码进行解码
#     # 将字符串转换成键值对
#     dic_str = json.loads(string)
#     # { "flag": true, "code": 0, "desc": null, "data": {"parseType": "TEXT", "quantity": "1", "letterNum": "1348",
#     # "fileId": "aa40bafebca140d6aa2956bbf921e343"}, "sid": "0a95e533efb746e88c9afc65d4ab26e7"}
#     print(dic_str['data'])
#     print(dic_str['desc'])
#     print(dic_str['code'])
#
#     return jsonify({"code": dic_str['code'], "desc": dic_str['desc'], "data": dic_str['data']})
#
