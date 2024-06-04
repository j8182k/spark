from utils.sqlUtil import updateExecute, queryExecute
import json
from utils import LocTrueSkill


def queryQuestionByIds(ids):
    # 根据一个id列表查询题目
    if len(ids) == 0:
        return 1
    q_dic = {}
    # print('ids',ids)

    for id in ids:
        if id == '':
            continue
        # print('id',id)
        q = queryQuestionById(id)
        if isinstance(q, BaseException):
            continue
        q_dic.update(q)
    if len(q_dic) == 0:
        return 1
    # 格式：{id:{},......}
    # print(q_dic)
    return q_dic


# 根据问题搜索题目
def queryQuestionByQ(Q, course):
    sql_query = '''select id, Q, A, B, C, D, answer, course, mu, sigma, leve, create_time 
                    from question 
                    where Q like %\'''' + str(Q) + "\'% and course = '" + str(course) + "';"
    results = queryExecute(sql_query)
    if len(results) == 0:
        # 没有题目
        return 1
    keys = ['Q', 'A', 'B', 'C', 'D', 'answer', 'course', 'mu', 'sigma', 'leve', 'create_time']
    question_dic = {}
    for value_tu in results:
        value = list(value_tu)
        id = value[0]
        value[11] = int(value[11].timestamp())
        dic = dict(zip(keys, value[1::]))
        question_dic[id] = dic
        # 以id为索引的字典
    return question_dic


def queryQuestionById(id):
    if not str(id).isdigit():
        return 1
    id = int(id)
    sql_query = '''select id, Q, A, B, C, D, answer, course, mu, sigma, leve, create_time from question where id = \'''' + str(
        id) + "\';"
    results = queryExecute(sql_query)
    if len(results) == 0:
        # 没有题目
        return 1
    keys = ['Q', 'A', 'B', 'C', 'D', 'answer', 'course', 'mu', 'sigma', 'leve', 'create_time']
    question_dic = {}
    for value_tu in results:
        value = list(value_tu)
        id = value[0]
        value[11] = int(value[11].timestamp())
        dic = dict(zip(keys, value[1::]))
        question_dic[id] = dic
    # 以id为索引的字典
    return question_dic


def getCourse():
    sql_query = "select DISTINCT course from question"
    try:
        results = queryExecute(sql_query)
        if len(results) == 0:
            return 1
        list_rs = []
        for item in results:
            value = item[0]
            if value == '':
                continue
            list_rs.append(value)
        keys = [i for i in range(len(list_rs))]
        dic = dict(zip(keys, list_rs))
        # print("获取到课程列表：")
        # print(dic)
        # 格式:{0:name1,1:name2,....}
        return dic
    except Exception as e:
        return e


def queryQuestionByCourse(course):
    # id, Q, A, B, C, D, answer, course, mu, sigma, leve
    sql_query = '''select id, Q, A, B, C, D, answer, course, mu, sigma, leve, create_time from question where course = \'''' + course + "\' ORDER BY create_time DESC;"
    results = queryExecute(sql_query)
    if len(results) == 0 or isinstance(results,BaseException):
        # 没有题目
        return 1
    keys = ['id', 'Q', 'A', 'B', 'C', 'D', 'answer', 'course', 'mu', 'sigma', 'leve', 'create_time']
    question_dic = {}
    for value_tu in results:
        value = list(value_tu)
        id = value[0]
        value[11] = int(value[11].timestamp())
        dic = dict(zip(keys, value))
        # print(dic)
        question_dic[id] = dic
        # 以id为索引的字典
    return question_dic


# 根据 课程 和 难度 搜索题目
def queryQbyCouresAndmu(course, lower, upper):
    if upper < lower:
        print("题目查询参数错误：难度上限与下限设置错误")
        return 1
    # 根据题目难度的上限和下限查询题目
    sql_query = '''select id, Q, A, B, C, D, answer, course, mu, sigma, leve, create_time from question where course = \'''' + course + "\' and mu<" + str(
        upper) + " and mu >" + str(lower)
    results = queryExecute(sql_query)
    if len(results) == 0 or isinstance(results,BaseException):
        return 1
    keys = ['Q', 'A', 'B', 'C', 'D', 'answer', 'course', 'mu', 'sigma', 'leve', 'create_time']
    question_dic = {}
    for value_tu in results:
        value = list(value_tu)
        id = value[0]
        value[11] = int(value[11].timestamp())
        dic = dict(zip(keys, value[1::]))
        question_dic[id] = dic
        # 以id为索引的字典
    return question_dic


def match_question(username, course, num):
    # 为学生找到适合的题目:把学生与题目放一起排名，取出学生附近的题目

    # 查询学生的能力
    sql_query = "select username,mu,sigma from student_skill where course = '" + course + "' and username = '" + username + "';"

    student = queryExecute(sql_query)
    # 先对题目做一个排名
    rank_question(course)
    # 查询相关题目难度
    sql_query = "select id,mu,sigma from question where course = '" + course + "'"

    question = queryExecute(sql_query)
    # 学生能力和题目难度放一起，排名
    results = student + question
    if len(results) == 0 or isinstance(results, BaseException):
        return 1
    list_rs = []
    # print(results)
    for item in results:
        value = list(item)
        keys = ['name', 'mu', 'sigma']
        dic = dict(zip(keys, value))
        list_rs.append(dic)
    keys = [i for i in range(len(list_rs))]
    rs = dict(zip(keys, list_rs))
    # rs格式：｛index:{name:'',mu:0.0,sigma:0.0},.....｝
    # 计算排名
    rank = LocTrueSkill.calculate_rank(rs)
    # print(rank)
    # 获取用户排名
    user_leve = rank[username]

    order = {value: key for key, value in rank.items()}
    t = num
    j = 1
    match_questions_id = []
    # 获取匹配的题目id
    while t > 0 and j < len(results):
        if user_leve + j in order:
            match_questions_id.append(order[user_leve + j])
            t -= 1
        if t > 0 and user_leve - j in order:
            match_questions_id.append(order[user_leve - j])
            t -= 1
        j += 1
    results = []
    # 根据题目id取题目
    for id in match_questions_id:
        sql_query = "select * from question where id = " + str(id) + ";"
        results += queryExecute(sql_query)
    if len(results) == 0:
        # 没有题目
        print("题目查询错误：没有题目")
        return 1
    keys = ['Q', 'A', 'B', 'C', 'D', 'answer', 'course', 'mu', 'sigma', 'leve', 'create_time']
    question_dic = {}
    for value_tu in results:
        value = list(value_tu)
        id = value[0]
        dic = dict(zip(keys, value[1::]))
        question_dic[id] = dic
    # 以id为索引的字典
    return question_dic


# 对指定课程的题目排名
def rank_question(course):
    sql_query = "select id,mu,sigma from question where course = '" + course + "'"
    results = queryExecute(sql_query)
    if len(results) == 0 or isinstance(results, BaseException):
        return 1
    list_rs = []
    # print(results)
    for item in results:
        value = list(item)
        keys = ['name', 'mu', 'sigma']
        dic = dict(zip(keys, value))
        list_rs.append(dic)
    keys = [i for i in range(len(list_rs))]
    rs = dict(zip(keys, list_rs))
    # rs格式：｛index:{name:'',mu:0.0,sigma:0.0},.....｝
    rank = LocTrueSkill.calculate_rank(rs)
    # print( rank )
    for key in rank:
        sql_query = "update question set leve=" + str(rank[key]) + " where id = " + str(key) + ";"
        updateExecute(sql_query)
    return rs


# 学生的答案处理
def answerHandle(username, answer, course):
    # answer参数格式：{1: 'C', 2: 'A', 3: 'A', 4: 'D', 6: 'B'}
    # 查原答案，批改，创建历史记录，存入数据库
    # 返回值格式：{id:{user_answer:A,answer:C,right:False},...}
    # print(answer)
    if course == '' or course is None:
        course = "空"
        print("答题记录没有课程")
    history = {}
    answer = json.loads(answer)
    r = 0
    w = 0

    for key in answer:
        sql_query = "select id,answer from question where id = " + str(int(key)) + ";"
        results = queryExecute(sql_query)
        if len(results) == 0 or isinstance(results, BaseException):
            print("答案处理错误，题目没有搜索到，272行")
            return 1
        key_list = ["user_answer", "answer", "right"]
        right = answer[key] == results[0][1]
        value_list = [answer[key], results[0][1], right]
        dic = dict(zip(key_list, value_list))
        if right:
            r += 1
        else:
            w += 1
            # TrueSkill自适应算法应用，学生能力和题目难度参数更新
            # print(key)
        LocTrueSkill.s_vs_q(username, key, dic['right'])
        history[key] = dic
    history = json.dumps(history)
    acc = round(r / (r + w), 3)
    sql_query = "insert into student_answer_history (username,history,course,accuracy) values('" + username + "','" + str(
        history) + "','" + course + "'," + str(acc) + ");"
    updateExecute(sql_query)
    return history


def updateQmu(question_id, mu, sigma):
    sql_query = "UPDATE question SET mu =" + str(mu) + ", sigma =" + str(sigma) + " where id = " + str(
        question_id) + ";"
    updateExecute(sql_query)


def insertQuestion(dic):
    sql_query = '''select id, Q, A, B, C, D, answer, course, mu, sigma, leve, create_time from question where Q like \'%''' + \
                dic['Q'] + '''%\' and A like \'%''' + dic[
                    'A'] + '''%\' and B like \'%''' + dic['B'] + '''%\' and C like \'%''' + dic[
                    'C'] + '''%\' and D like \'%''' + \
                dic['D'] + '''%\''''
    results = queryExecute(sql_query)
    if len(results) != 0:
        print("题目已经存在")
        return 1
    sql_insert = ("insert into question (Q,A,B,C,D,answer,course,mu,sigma)values('"
                  + dic['Q'] + "','"
                  + dic['A'] + "','"
                  + dic['B'] + "','"
                  + dic['C'] + "','"
                  + dic['D'] + "','"
                  + dic['answer'] + "','"
                  + dic['course'] + "','"
                  + str(dic['mu']) + "','"
                  + str(dic['sigma']) +
                  "')")
    updateExecute(sql_insert)
    return 0


def deleteQuestionById(id):
    sql_delete = "delete from question where id = " + str(id) + ";"
    updateExecute(sql_delete)


def updateQuestion(id, Q, A, B, C, D, answer, course, mu, sigma, leve, knowledge):
    sql_update = "update question set Q = '" + str(Q) + "',A='" + str(A) + "',B='" + str(B) + "',C='" + str(
        C) + "',D='" + str(D) + "',answer='" + str(answer) + "',course='" + str(course) + "',mu=" + str(
        mu) + ",sigma=" + str(sigma) + ",leve=" + str(leve) + ",knowledge='" + str(knowledge) + "' where id = " + str(
        id) + ";"
    updateExecute(sql_update)
