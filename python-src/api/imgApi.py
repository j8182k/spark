"""
  印刷文字识别WebAPI接口调用示例接口文档(必看)：https://doc.xfyun.cn/rest_api/%E5%8D%B0%E5%88%B7%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB.html
  上传图片base64编码后进行urlencode要求base64编码和urlencode后大小不超过4M最短边至少15px，最长边最大4096px支持jpg/png/bmp格式
  (Very Important)创建完webapi应用添加合成服务之后一定要设置ip白名单，找到控制台--我的应用--设置ip白名单，如何设置参考：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=41891
  错误码链接：https://www.xfyun.cn/document/error-code (code返回错误码时必看)
  @author iflytek
"""
# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import json

# from urllib import parse
# 印刷文字识别 webapi 接口地址
URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/general"
# 应用ID (必须为webapi类型应用，并印刷文字识别服务，参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481)
APPID = "f27a5eb0"
# 接口密钥(webapi类型应用开通印刷文字识别服务后，控制台--我的应用---印刷文字识别---服务的apikey)
API_KEY = "03c43ee836daa0ad286783c500e4e82e"


def getHeader():
    #  当前时间戳
    curTime = str(int(time.time()))
    #  支持语言类型和是否开启位置定位(默认否)
    param = {"language": "cn|en", "location": "false"}
    param = json.dumps(param)
    paramBase64 = base64.b64encode(param.encode('utf-8'))

    m2 = hashlib.md5()
    str1 = API_KEY + curTime + str(paramBase64, 'utf-8')
    m2.update(str1.encode('utf-8'))
    checkSum = m2.hexdigest()
    # 组装http请求头
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def imgRec(img):
    # 上传文件并进行base64位编码
    # with open(imgPath, 'rb') as f:
    #     f1 = f.read()

    f1_base64 = str(base64.b64encode(img.read()), 'utf-8')

    data = {
        'image': f1_base64
    }

    r = requests.post(URL, data=data, headers=getHeader())

    # 错误码链接：https://www.xfyun.cn/document/error-code (code返回错误码时必看)
    string = r.content.decode('utf-8')  # 使用UTF-8编码进行解码
    # 将字符串转换成键值对
    dic_str = json.loads(string)
    linelist = dic_str['data']['block'][0]['line']
    rs = ''
    for line in linelist:
        rs += line['word'][0]['content'] + '\n'
    return rs

# if __name__ == '__main__':
#     imgRec('毕业要求.jpg')

# {"code": "0", "data": {"block": [
# {"type": "text",
# "line": [
#     {"confidence": 1, "word": [{"content": "1.以第一作者发表以下论文之一：CCFC类中文期刊以上论文1"}]},
#     {"confidence": 1, "word": [{"content": "篇，CCFC类国际会议以上论文1篇，EI检索的期刊或会议论文1篇，"}]},
#     {"confidence": 1, "word": [{"content": "或者以第二作者（导师为第一作者）发表CCFB类及以上的期刊、会"}]},
#     {"confidence": 1, "word": [{"content": "议论文；"}]},
#     {"confidence": 1, "word": [{"content": "2.受理发明专利1项（申请人排名第一或者导师第一、申请人第"}]},
#     {"confidence": 1, "word": [{"content": "二）,或第一著作权人登记软件著作权1项；"}]},
#     {"confidence": 1, "word": [{"content": "3.在研究生期间，参加以下程序设计类的测试或比赛并满足以下"}]},
#     {"confidence": 1, "word": [{"content": "条件之一：(1)通过CCF-CSP考试，排名在前3%;(2)参加蓝桥杯"}]},
#     {"confidence": 1, "word": [{"content": "全国软件和信息技术专业人才大赛并在全国决赛获二等奖及以上；"}]},
#     {"confidence": 1, "word": [{"content": "(3)ICPC亚洲区域赛/CCPC(中国大学生程序设计竞赛）获得银奖"}]},
#     {"confidence": 1, "word": [{"content": "及以上；(4)参加CCF-CCSP决赛获银奖及以上；"}]},
#     {"confidence": 1, "word": [{"content": "4.参加中国研究生创新实践系列大赛并获奖，一等奖前3,二等"}]},
#     {"confidence": 1, "word": [{"content": "奖前2名，三等奖第1名；中国软件杯一等奖前3名，二等奖前2名；"}]},
#     {"confidence": 1, "word": [{"content": "互联网+省赛的一等奖前2,二等奖第1名；互联网+国赛和挑战杯国"}]},
#     {"confidence": 1, "word": [{"content": "赛二等奖以上的获奖成员；计算机领域国际A类会议的竞赛获得前"}]},
#     {"confidence": 1, "word": [{"content": "3名（排名前3)。"}]}
#     ]
#     }
#     ]}, "desc": "success",
#  "sid": "wcr009c1fc2@dx2fb51992ca186f1a00"}
