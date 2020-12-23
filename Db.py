import mariadb

pool = None
user = "root"
password = "mariadb"
host = "mariadb.host"
port = 3306
database = "istock"


def initConnectionPool():
    global pool
    pool = mariadb.ConnectionPool(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        pool_name="app",
        pool_size=8
    )
    return pool


def getConnection():
    try:
        if pool is None:
            initConnectionPool()
        conn = pool.get_connection()
    except mariadb.Error as e:
        print(f'Error connecting to MariaDB Platform: {e}')
    return conn


def execute(fun, params=()):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        result = fun(cursor, params)
        conn.commit()
        return result
    except Exception as e:
        print(f'execute error. {e}')
        conn.rollback()
    finally:
        conn.close()


def batchUpdate(sql, paramsList):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        for i in range(len(paramsList)):
            params = paramsList[i]
            cursor.execute(sql, params)
        conn.commit()
    except Exception as e:
        print(f'batchUpdate error. {e}')
        conn.rollback()
    finally:
        conn.close()
