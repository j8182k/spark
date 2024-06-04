from utils.sqlUtil import updateExecute, queryExecute
import json


def queryHistory(username, course):
    print(course)
    sql_query = "select id,username,history,create_time,course,accuracy from student_answer_history where username = '" + username + "' and course = '" + course + "' ORDER BY create_time DESC;"
    rs = queryExecute(sql_query)
    # print('rs',rs)
    if len(rs) == 0 or isinstance(rs, BaseException):
        return 1
    arr = []
    for line in rs:
        keys = ['h_id', 'username', 'history', 'create_time', 'course', 'accuracy']
        # line[3] = int(line[3].timestamp())
        values = list(line)
        values[3] = int(values[3].timestamp())
        arr.append(dict(zip(keys, values)))
    return arr


# 按时间列出历史记录,主要用于曲线图描绘
def queryH_TByCourse(username, course):
    sql_query = "select history,create_time,accuracy from student_answer_history where username = '" + username + "' and course = '" + course + "' ORDER BY create_time DESC;"
    rs = queryExecute(sql_query)
    if len(rs) == 0 or isinstance(rs, BaseException):
        return 1
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


# 以id为索引的历史记录
def queryHby_C_U(username, course):
    sql_query = "select id,username,history,create_time,course,accuracy from student_answer_history where username = '" + username + "' and course = '" + course + "' ORDER BY create_time DESC;"
    rs = queryExecute(sql_query)
    if len(rs) == 0:
        return 1
    result = {}
    for line in rs:
        keys = ['username', 'history', 'create_time', 'course', 'accuracy']
        line[3] = int(line[3].timestamp())
        result[line[0]] = dict(zip(keys, list(line[1::])))
    # 格式：{id:{....}}
    return result


# 搜索历史记录
def queryHistoryById(id):
    sql_query = "select username,history,create_time,course,accuracy from student_answer_history where id = " + str(
        id) + " ORDER BY create_time DESC;"
    # print(sql_query)
    rs = queryExecute(sql_query)
    # print('历史记录', rs)
    if len(rs) == 0 or isinstance(rs, BaseException):
        return 1

    rs = rs[0]
    rs[2] = int(rs[2].timestamp())
    keys = ['username', 'history', 'create_time', 'course', 'accuracy']
    rs = list(rs)
    rs = dict(zip(keys, rs))
    rs = {id: rs}
    # 格式：{id:{....}}
    return rs
