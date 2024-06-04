from utils.sqlUtil import updateExecute, queryExecute
import json
from api import sparkAPI
from .QuestionHistory import queryHistoryById
from .Questions import queryQuestionById
import datetime


# 查询用户的所有错题
def queryEQ(username, course):
    sql_query = "select * from error_questions where username = '" + str(username) + "' and course = '" + str(
        course) + "';"
    query_rs = queryExecute(sql_query)
    if len(query_rs) == 0 or isinstance(query_rs, BaseException):
        return 1
    result = []
    for line in query_rs:
        keys = ['username', 'q_id', 'course', 'info', 'analysis', 'knowledge', 'create_time']
        line[6] = int(line[6].timestamp())
        values = list(line)
        result.append(dict(zip(keys, values)))
    return result


def insertErrorQ(username, q_id, course, info, analysis, knowledge):
    info = json.dumps(info, ensure_ascii=False)

    knowledge = json.dumps(knowledge, ensure_ascii=False)
    sql = "insert into error_questions (username,q_id,course,info,analysis,knowledge) values( '" + str(
        username) + "'," + str(
        q_id) + ",'" + str(course) + "','" + str(info) + "','" + str(analysis) + "','" + str(knowledge) + "');"
    # print('sql', sql)
    return updateExecute(sql)


def updateErrorQ(username, q_id, course, info, analysis, knowledge):
    info = str(info).replace("'", "\\'").replace('"', '\\"')
    analysis = str(analysis).replace("'", "\\'").replace('"', '\\"')
    knowledge = str(knowledge).replace("'", "\\'").replace('"', '\\"')
    sql = ("update error_questions set course='" + str(course) + "',info='" + str(info) + "',analysis='"
           + str(analysis) + "',knowledge='" + str(knowledge) + "' where username='" + str(
                username) + "' and  q_id=" + str(q_id) + ";")

    rs = updateExecute(sql)
    # 如果没有添加该错题则直接插入
    if isinstance(rs, BaseException):
        insertErrorQ(username, q_id, course, info, analysis, knowledge)


# 错题收集,针对一条答题历史
def collectErrorQ(history_id):
    history_line = queryHistoryById(history_id)
    username = history_line[history_id]['username']
    history = history_line[history_id]['history']
    history = json.loads(history)
    # 遍历记录中的题目
    # history格式：{q_id:{},....}
    for key in history:
        question = history[key]
        # print(question,key)
        if not question['right']:
            q_id = key
            addErrorQ(username, q_id)
    return 0


def addErrorQ(username, q_id):
    info = queryQuestionById(q_id)
    print(info)
    info = info[int(q_id)]
    info['create_time'] = info['create_time'].timestamp()
    course = info['course']
    return insertErrorQ(username, q_id, course, info, '智能分析', {1: "知识点"})


# 分析错题并且提取知识点
def analysisErrorQ(username, q_id):
    info = queryQuestionById(q_id)
    course = info['course']
    analysis = sparkAPI.analysisQ(info)
    knowledge = sparkAPI.extractKnowledge(info)
    return updateErrorQ(username, q_id, course, info, analysis, knowledge)
