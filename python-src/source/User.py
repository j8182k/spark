import json

import mysql.connector
import hashlib


def md5_encrypt(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def queryUser(type, username):
    if username is None or type == "":
        return '没有该用户'
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'spark'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    if type == 'student':
        sql_query = "select username,password,nickname,gender,age,class from student where username='" + username + "'"
        key = ['username', 'password', 'nickname', 'gender', 'age', 'class']
    else:
        sql_query = "select username,password,nickname,gender,age,class,phone from teacher where username='" + username + "'"
        key = ['username', 'password', 'nickname', 'gender', 'age', 'class', 'phone']
    cursor.execute(sql_query)
    rs = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(rs) == 0:
        return '没有该用户'
    else:
        rs = list(rs[0])
        dic = dict(zip(key, rs))

        return dic


def login(type, username, password):
    if username is None or password is None or type == "":
        return '没有该用户'
    password = md5_encrypt(password)
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'spark'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = "select * from " + type + " where username='" + username + "'"
    cursor.execute(sql_query)
    rs = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(rs) == 0:
        return '没有该用户'
    elif rs[0][1] != password:
        return '密码错误'
    else:
        return '密码正确'


def updatePassword(userInfo, new_password):
    print('new_password',new_password)
    print('userInfo',userInfo)
    if isinstance(userInfo, str):
        userInfo = json.loads(userInfo)
    # 密码重复返回1，不重复返回0
    password = userInfo['password']
    new_password = md5_encrypt(new_password)
    if password == new_password:
        return 1
    else:
        userInfo['password'] = new_password
        updataInfo(userInfo)
        return 0


def checkPassword(userInfo, old_password):
    if isinstance(userInfo, str):
        userInfo = json.loads(userInfo)
    # 密码重复返回1，不重复返回0
    password = userInfo['password']
    old_password = md5_encrypt(old_password)
    if password == old_password:
        return True
    else:
        return False


def updataInfo(userInfo):
    print(userInfo)
    if isinstance(userInfo, str):
        userInfo = json.loads(userInfo)
    username = userInfo['username']
    type = userInfo['type']
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'spark'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    if type == 'student':
        sql_updata = "update student set nickname = '" + userInfo['nickname'] + "',gender = '" + userInfo[
            'gender'] + "',password = '" + userInfo['password'] + "',age=" + str(userInfo['age']) + ",class='" + \
                     userInfo['class'] + "' where username='" + str(username) + "';"
    else:
        sql_updata = "update teacher set nickname = '" + userInfo['nickname'] + "',gender = '" + userInfo[
            'gender'] + "',password = '" + userInfo['password'] + "',age=" + str(userInfo['age']) + ",class='" + \
                     userInfo['class'] + "',phone='" + str(userInfo['phone']) + "' where username='" + str(
            username) + "';"
    cursor.execute(sql_updata)
    connection.commit()
    cursor.close()
    connection.close()
    return 0


def add_student(username, password, nickname='无名氏', gender='空', age=0, cls='空'):
    if username is None or password is None:
        return False
    password = md5_encrypt(password)
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'spark'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = '''insert into student values(\'''' + username + '''\',\'''' + password + "','" + nickname + "','" + gender + "'," + str(
        age) + ",'" + cls + "')"
    cursor.execute(sql_query)
    connection.commit()
    cursor.close()
    connection.close()
    return True


def add_teacher(username, password, nickname='无名氏', gender='空', age=0, cls='空', phone=0):
    if username is None or password is None:
        return False
    password = md5_encrypt(password)
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'spark'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = '''insert into teacher values(\'''' + username + '''\',\'''' + password + "','" + nickname + "','" + gender + "'," + str(
        age) + ",'" + cls + "'," + str(phone) + ")"
    cursor.execute(sql_query)
    connection.commit()
    cursor.close()
    connection.close()
    return True


def getSkills(username, course):
    # 数据库设置
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'spark'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = "select mu,sigma  from  student_skill where username = '" + username + "' and course = '" + course + "'; "
    cursor.execute(sql_query)
    rs = cursor.fetchall()
    if len(rs) == 0:
        rs = [(25, 8.334)]
        sql_query = "insert into student_skill(username,course,mu,sigma) values('" + username + "','" + course + "'," + str(
            25) + "," + str(8.334) + ");"
        cursor.execute(sql_query)
        connection.commit()
    connection.close()
    cursor.close()
    keys = ['mu', 'sigma']
    result = dict(zip(keys, [rs[0][0], rs[0][1]]))
    return result


def setSkill(username, mu, sigma, course):
    # 数据库设置
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'spark'
    }
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    sql_query = "UPDATE student_skill SET mu = " + str(mu) + ", sigma = " + str(
        sigma) + " WHERE username= '" + username + "' and course = '" + course + "';"
    cursor.execute(sql_query)
    connection.commit()


if __name__ == '__main__':
    # getSkills('Admin', '深度学习')
    # setSkill('Admin',20,7,'深度学习')
    # u = queryUser('teacher','Admin')
    # print(u)
    s = {'username': 'Admin', 'type': 'teacher', 'password': '827ccb0eea8a706c4c34a16891f84e7b', 'nickname': '特朗普',
         'gender': '男', 'age': 77, 'class': '空', 'phone': 0}
    updataInfo(s)
    pass
