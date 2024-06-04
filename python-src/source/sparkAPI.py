# coding: utf-8
import _thread as thread
import os
import time
import base64

import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket
import openpyxl
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

globals()['result_content'] = ''


class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + urlencode(v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,a,b):
    print("")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, query=ws.query, domain=ws.domain))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]

        globals()['result_content'] += content

        if status == 2:
            print("")
            ws.close()


def gen_params(appid, query, domain):
    """
    通过appid和用户的提问来生成请参数
    """

    data = {
        "header": {
            "app_id": appid,
            "uid": "1234",
            # "patch_id": []    #接入微调模型，对应服务发布后的resourceid          
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": 0.5,
                "max_tokens": 4096,
                "auditing": "default",
            }
        },
        "payload": {
            "message": {
                "text": [{"role": "user", "content": query}]
            }
        }
    }
    return data


def main(appid, api_secret, api_key, gpt_url, domain, query):
    wsParam = Ws_Param(appid, api_key, api_secret, gpt_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.query = query
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


def chatAPI(query):
    main(
        appid="f27a5eb0",
        api_secret="NDllMTIxNzBmZjEwNGY2NzEwMGIzNWQ5",
        api_key="b1a85d3698a2f5277390c559f1e5a05d",
        gpt_url="wss://spark-api.xf-yun.com/v3.5/chat",
        domain="generalv3.5",
        query=query
    )
    rs = globals()['result_content']
    globals()['result_content'] = ''
    # 去掉开头无效的两行
    return rs


def genQuestionApi(question, num=1):
    speak = str(question) + "\n请按照上述格式生成一个类似的题目，其中course不变"
    rs_dic = {}
    if num is None:
        num = 1
    for i in range(int(num)):
        answer = chatAPI(speak)
        print('题目生成结果：' + answer)
        answer = answer.replace("'", '"')
        answer = json.loads(answer)
        assess = assessQuestion(answer)
        answer['assess'] = assess
        rs_dic[i] = answer
    return rs_dic


def assessQuestion(question):
    speak = str(
        question) + "\n请评价上述题目难度，0~20容易，20~30正常，30~50较难，50~70困难，70~100最难，请按｛'mu':0.0,'message':'评价'｝格式生成答案,其中mu指难度值，message指评价信息"
    answer = chatAPI(speak)
    answer = answer.replace("'", '"')
    answer = json.loads(answer)
    return answer


# import Question


def extractKnowledge(question):
    speak = str(question) + '''\n请提取上述题目涉及的所有知识点，请按{1:"",2:"",3:"",...}json格式输出'''
    # print(speak)
    knowledge = chatAPI(speak)
    # print(knowledge)
    return knowledge


# 按照知识点生成题目
def genQuestionByKnowledge(knowledge):
    speak = str(knowledge) + '''\n请参照上述要点，按照以下模板：\n
“{'Q': '.数据科学家可能会同时使用多个算法（模型）进行预测，并且最后把这些算法的结果集成起来进行最后的预测（集成学习）,以下对集成学习说法正确的是', 'A': '.单个模型之间有高相关性', 'B': '.单个模型之间有低相关性', 'C': '.在集成学习中使用“平均权重”而不是“投票”会比较好', 'D': '.单个模型都是用的一个算法', 'answer': 'B', 'course': '机器学习'}”
生成一个题目，不要有多余的答案'''
    # print("speak:")
    # print(speak)
    question = chatAPI(speak)
    # print("answer:")
    # print(answer)
    return question


def analysisQ(question):
    speak = str(question) + "\n请分析上述题目"
    analysis = chatAPI(speak)
    return analysis


if __name__ == '__main__':
    # question = Question.queryQuestionById(16)
    # knowledge = extractKnowledge(question)
    # genQuestionByKnowledge(knowledge)
    pass
