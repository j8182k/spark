import json
import mysql.connector
import LocTrueSkill
import sparkAPI

# 数据库设置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'spark'
}


def queryQuestionByIds(ids):
    # 根据一个id列表查询题目
    q_dic = {}
    # print('ids',ids)
    for id in ids:
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
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = '''select id, Q, A, B, C, D, answer, course, mu, sigma, leve, create_time 
                    from question 
                    where Q like %\'''' + str(Q) + "\'% and course = '" + str(course) + "';"
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        if len(results) == 0:
            # 没有题目
            cursor.close()
            connection.close()
            return 1
        keys = ['Q', 'A', 'B', 'C', 'D', 'answer', 'course', 'mu', 'sigma', 'leve', 'create_time']
        question_dic = {}
        for value_tu in results:
            value = list(value_tu)
            id = value[0]
            dic = dict(zip(keys, value[1::]))
            question_dic[id] = dic
        connection.close()
        cursor.close()
        # 以id为索引的字典
        return question_dic
    except Exception as e:
        return e


def queryQuestionById(id):
    if not str(id).isdigit():
        return 1
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    id = int(id)
    sql_query = '''select id, Q, A, B, C, D, answer, course, mu, sigma, leve, create_time from question where id = \'''' + str(
        id) + "\';"
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        if len(results) == 0:
            # 没有题目
            cursor.close()
            connection.close()
            return 1
        keys = ['Q', 'A', 'B', 'C', 'D', 'answer', 'course', 'mu', 'sigma', 'leve', 'create_time']
        question_dic = {}
        for value_tu in results:
            value = list(value_tu)
            id = value[0]
            dic = dict(zip(keys, value[1::]))
            question_dic[id] = dic
        connection.close()
        cursor.close()
        # 以id为索引的字典
        return question_dic
    except Exception as e:
        return e


def queryQuestionByCourse(course):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    # id, Q, A, B, C, D, answer, course, mu, sigma, leve
    sql_query = '''select id, Q, A, B, C, D, answer, course, mu, sigma, leve, create_time from question where course = \'''' + course + "\' ORDER BY create_time DESC;"
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        if len(results) == 0:
            cursor.close()
            connection.close()
            # 没有题目
            return 1
        keys = ['id', 'Q', 'A', 'B', 'C', 'D', 'answer', 'course', 'mu', 'sigma', 'leve', 'create_time']
        question_dic = {}
        for value_tu in results:
            value = list(value_tu)
            id = value[0]
            dic = dict(zip(keys, value))
            # print(dic)
            question_dic[id] = dic
        connection.close()
        cursor.close()
        # 以id为索引的字典
        return question_dic
    except Exception as e:
        return e


# 根据 课程 和 难度 搜索题目
def queryQbyCouresAndmu(course, lower, upper):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    if upper < lower:
        print("题目查询参数错误：难度上限与下限设置错误")
        return 1
    # 根据题目难度的上限和下限查询题目
    sql_query = '''select id, Q, A, B, C, D, answer, course, mu, sigma, leve, create_time from question where course = \'''' + course + "\' and mu<" + str(
        upper) + " and mu >" + str(lower)
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        if len(results) == 0:
            cursor.close()
            connection.close()
            return 1
        keys = ['Q', 'A', 'B', 'C', 'D', 'answer', 'course', 'mu', 'sigma', 'leve', 'create_time']
        question_dic = {}
        for value_tu in results:
            value = list(value_tu)
            id = value[0]
            dic = dict(zip(keys, value[1::]))
            question_dic[id] = dic
        connection.close()
        cursor.close()
        # 以id为索引的字典
        return question_dic
    except Exception as e:
        return e


# 检索课程信息
def getCourse():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = "select DISTINCT course from question"
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        if len(results) == 0:
            connection.close()
            cursor.close()
            return 1
        list_rs = []
        for item in results:
            value = item[0]
            if value == '':
                continue
            list_rs.append(value)
        keys = [i for i in range(len(list_rs))]
        dic = dict(zip(keys, list_rs))
        cursor.close()
        connection.close()
        # print("获取到课程列表：")
        # print(dic)
        # 格式:{0:name1,1:name2,....}
        return dic
    except Exception as e:
        return e


def match_question(username, course, num):
    connection = mysql.connector.connect(**db_config)
    # 为学生找到适合的题目:把学生与题目放一起排名，取出学生附近的题目
    cursor = connection.cursor()
    # 查询学生的能力
    sql_query = "select username,mu,sigma from student_skill where course = '" + course + "' and username = '" + username + "';"
    try:
        cursor.execute(sql_query)
        student = cursor.fetchall()
        # 先对题目做一个排名
        rank_question(course)
        # 查询相关题目难度
        sql_query = "select id,mu,sigma from question where course = '" + course + "'"
        cursor.execute(sql_query)
        question = cursor.fetchall()
        # 学生能力和题目难度放一起，排名
        results = student + question
        if len(results) == 0:
            cursor.close()
            connection.close()
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
            cursor.execute(sql_query)
            results += cursor.fetchall()
        if len(results) == 0:
            # 没有题目
            cursor.close()
            connection.close()
            print("题目查询错误：没有题目")
            return 1
        keys = ['Q', 'A', 'B', 'C', 'D', 'answer', 'course', 'mu', 'sigma', 'leve', 'create_time']
        question_dic = {}
        for value_tu in results:
            value = list(value_tu)
            id = value[0]
            dic = dict(zip(keys, value[1::]))
            question_dic[id] = dic
        connection.close()
        cursor.close()
        # 以id为索引的字典
        return question_dic
    except Exception as e:
        cursor.close()
        connection.close()
        return e


# 对指定课程的题目排名
def rank_question(course):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = "select id,mu,sigma from question where course = '" + course + "'"
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        if len(results) == 0:
            cursor.close()
            connection.close()
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
            cursor.execute(sql_query)
        cursor.close()
        connection.commit()
        connection.close()
        return rs
    except Exception as e:
        cursor.close()
        connection.rollback()
        connection.close()
        return e


# 学生的答案处理
def answerHandle(username, answer, course):
    # answer参数格式：{1: 'C', 2: 'A', 3: 'A', 4: 'D', 6: 'B'}
    # 查原答案，批改，创建历史记录，存入数据库
    # 返回值格式：{id:{user_answer:A,answer:C,right:False},...}
    # print(answer)
    if course == '' or course is None:
        course = "空"
        print("答题记录没有课程")
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    history = {}
    answer = json.loads(answer)
    r = 0
    w = 0
    try:
        for key in answer:
            sql_query = "select id,answer from question where id = " + str(int(key)) + ";"
            cursor.execute(sql_query)
            results = cursor.fetchall()
            if len(results) == 0:
                cursor.close()
                connection.close()
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
        cursor.execute(sql_query)
        connection.commit()
        connection.close()
        return history
    except Exception as e:
        cursor.close()
        connection.close()
        return e


# 按时间列出历史记录
def queryH_TByCourse(username, course):
    connection = mysql.connector.connect(**db_config)
    # 查找某人课程的答题历史
    cursor = connection.cursor()
    sql_query = "select history,create_time,accuracy from student_answer_history where username = '" + username + "' and course = '" + course + "' ORDER BY create_time DESC;"
    try:
        cursor.execute(sql_query)
        rs = cursor.fetchall()
        if len(rs) == 0:
            cursor.close()
            connection.close()
            return 1
        cursor.close()
        connection.close()
        # print(rs)
        # 时间:记录
        record = {}
        for line in rs:
            times = int(line[1].timestamp())
            history = json.loads(line[0])
            history['accuracy'] = line[2]
            record[times] = history
        # print(record)
        # 返回格式：{时间:记录，。。。。}
        return record
    except Exception as e:
        cursor.close()
        connection.close()
        return e


# 以id为索引的历史记录
def queryH_by_C_U(username, course):
    connection = mysql.connector.connect(**db_config)
    # 查找某人课程的答题历史
    cursor = connection.cursor()
    sql_query = "select id,username,history,create_time,course,accuracy from student_answer_history where username = '" + username + "' and course = '" + course + "' ORDER BY create_time DESC;"
    try:
        cursor.execute(sql_query)
        rs = cursor.fetchall()
        if len(rs) == 0:
            cursor.close()
            connection.close()
            return 1
        result = {}
        for line in rs:
            keys = ['username', 'history', 'create_time', 'course', 'accuracy']
            result[line[0]] = dict(zip(keys, list(line[1::])))
        # print(rs)
        cursor.close()
        connection.close()
        # 格式：{id:{....}}
        return result
    except Exception as e:
        cursor.close()
        connection.close()
        return e


# 搜索历史记录
def queryHistoryById(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = "select username,history,create_time,course,accuracy from student_answer_history where id = " + str(
        id) + " ORDER BY create_time DESC;"
    try:
        cursor.execute(sql_query)
        rs = cursor.fetchall()[0]
        if len(rs) == 0:
            cursor.close()
            connection.close()
            return 1
        keys = ['username', 'history', 'create_time', 'course', 'accuracy']
        rs = list(rs)
        rs = dict(zip(keys, rs))
        rs = {id: rs}
        # print(rs)
        cursor.close()
        connection.close()
        # 格式：{id:{....}}
        return rs
    except Exception as e:
        cursor.close()
        connection.close()
        return e


def updateQmu(question_id, mu, sigma):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = "UPDATE question SET mu =" + str(mu) + ", sigma =" + str(sigma) + " where id = " + str(
        question_id) + ";"
    # print(sql_query)
    try:
        cursor.execute(sql_query)
        cursor.close()
        connection.commit()
        connection.close()
    except Exception as e:
        cursor.close()
        connection.rollback()
        connection.close()
        return e


def insertQuestion(dic):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = '''select id, Q, A, B, C, D, answer, course, mu, sigma, leve, create_time from question where Q like \'%''' + \
                dic['Q'] + '''%\' and A like \'%''' + dic[
                    'A'] + '''%\' and B like \'%''' + dic['B'] + '''%\' and C like \'%''' + dic[
                    'C'] + '''%\' and D like \'%''' + \
                dic['D'] + '''%\''''
    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        if len(results) != 0:
            print("题目已经存在")
            cursor.close()
            connection.close()
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
        cursor.execute(sql_insert)
        connection.commit()
        connection.close()
        # print("一个新题目保存到数据库：")
        # print(dic)
        return 0
    except Exception as e:
        cursor.close()
        connection.rollback()
        connection.close()
        return e


def insertErrorQ(username, q_id, course, info, analysis, knowledge):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    info = str(info).replace("'", "\\'").replace('"', '\\"')
    analysis = str(analysis).replace("'", "\\'").replace('"', '\\"')
    knowledge = str(knowledge).replace("'", "\\'").replace('"', '\\"')
    sql_query = "insert into error_questions (username,q_id,course,info,analysis,knowledge) values( '" + str(
        username) + "'," + str(
        q_id) + ",'" + str(course) + "','" + str(info) + "','" + str(analysis) + "','" + str(knowledge) + "');"
    # print(sql_query)
    try:
        cursor.execute(sql_query)
        cursor.close()
        connection.commit()
        connection.close()
        return 0
    except Exception as e:
        cursor.close()
        connection.rollback()
        connection.close()
        return e


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
            addErrorQByQuestion(username, q_id)
    return 0


def addErrorQByQuestion(username, q_id):
    info = queryQuestionById(q_id)
    course = info['course']
    analysis = sparkAPI.analysisQ(info)
    knowledge = sparkAPI.extractKnowledge(info)
    return insertErrorQ(username, q_id, course, info, analysis, knowledge)


# 查询用户的所有错题
def queryEQ(username, course):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = "select * from error_questions where username = '" + str(username) + "' and course = '"+str(course)+"';"
    try:
        cursor.execute(sql_query)
        query_rs = cursor.fetchall()
        if len(query_rs) == 0:
            cursor.close()
            connection.close()
            return 1
        result = []
        for line in query_rs:
            keys = ['username','q_id','course','info', 'analysis', 'knowledge', 'create_time']
            values = list(line)
            result.append(dict(zip(keys,values)))
        connection.close()
        cursor.close()
        return result
    except Exception as e:
        connection.rollback()
        connection.close()
        cursor.close()
        return e


def deleteQuestionById(id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        sql_delete = "delete from question where id = " + str(id) + ";"
        cursor.execute(sql_delete)
        connection.commit()
        connection.close()
        cursor.close()
        return 0
    except Exception as e:
        connection.rollback()
        connection.close()
        cursor.close()
        return e


def updateQuestion(id, Q, A, B, C, D, answer, course, mu, sigma, leve, knowledge):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_update = "update question set Q = '" + str(Q) + "',A='" + str(A) + "',B='" + str(B) + "',C='" + str(
        C) + "',D='" + str(D) + "',answer='" + str(answer) + "',course='" + str(course) + "',mu=" + str(
        mu) + ",sigma=" + str(sigma) + ",leve=" + str(leve) + ",knowledge='" + str(knowledge) + "' where id = " + str(
        id) + ";"
    try:
        cursor.execute(sql_update)
        connection.commit()
        connection.close()
        cursor.close()
        return 0
    except Exception as e:
        connection.rollback()
        connection.close()
        cursor.close()
        return e


def addCourse(name, students, teacher):
    pass


if __name__ == '__main__':
    # queryEQByU_C('Admin', '机器学习')
    # queryEQByh_id(145)
    pass
    # collectErrorQ(145)
    # updateQmu(1, 30, 7)
    # getHistoryByCourse('Admin', '机器学习')
    # getHistoryById(127)
    # s = {
    #       'Q': '.在以下不同的场景中，使用的分析方法不正确的有（）',
    #      'A': '.根据用户的历史搜索记录和点击行为，用协同过滤算法推荐用户可能感兴趣的新闻文章',
    #      'B': '.根据社交媒体上的实时动态，用情感分析算法预测公众对于某一事件的情绪倾向',
    #      'C': '.用关联规则算法分析出购买了运动鞋的用户，是否适合推荐运动服装',
    #      'D': '.根据用户最近在线学习的课程内容，用决策树算法识别出用户的学习兴趣领域',
    #      'answer': 'A',
    #      'course': '机器学习',
    #      'mu': 22.0,
    #      'sigma': 8.7
    #     }
    # saveQuestion(s)
    # rs = queryQuestionByCourse('机器学习')
    # print(rs)
    # queryQbyCouresAndmu('机器学习', 20, 30)
    # rank_question('机器学习')
    # match_question('Admin', '机器学习', 5)
    # # answerHandle('Admin', {1: 'C', 2: 'A', 3: 'A', 4: 'D', 6: 'B'})
    # rs = queryHistoryById(53)
    # print(rs)
