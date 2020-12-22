import mariadb

pool = None
user = "root"
password = "mariadb"
host = "192.168.1.9"
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
        conn = pool.get_connection()
    except mariadb.Error as e:
        print(f'Error connecting to MariaDB Platform: {e}')
    return conn


def dbExecute(fun, params=()):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        result = fun(cursor, params)
        conn.commit()
        return result
    except Exception as e:
        print(f'dbExecute error. {e}')
        conn.rollback()
    finally:
        conn.close()
