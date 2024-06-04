import mysql.connector


def getConnection():
    # 数据库设置
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'spark'
    }
    connection = mysql.connector.connect(**db_config)
    return connection


def closes(connection, cursor):
    connection.close()
    cursor.close()


def updateExecute(sql):
    connection = getConnection()
    cursor = connection.cursor()
    rs = ''
    try:
        cursor.execute(sql)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(e)
        rs = e
    finally:
        closes(connection, cursor)
        return rs


def queryExecute(sql):
    connection = getConnection()
    cursor = connection.cursor()
    rs = ''
    try:
        cursor.execute(sql)
        rs = cursor.fetchall()
    except Exception as e:
        connection.rollback()
        print(e)
        rs = e
    finally:
        closes(connection, cursor)
        return rs


if __name__ == '__main__':
    rs = queryExecute('select * from student')
    print(rs)
