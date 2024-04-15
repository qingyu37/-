import pymysql


def getConn():
    # 与数据库建立连接
    try:
        conn = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, database='student')
        print("数据库连接成功")
        return conn
    except Exception as e:
        print(e)
        return None


def closeConn(conn, cursor):
    # 与数据库断开连接
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("数据库关闭成功")
    except Exception as e:
        print(e)
        return None
