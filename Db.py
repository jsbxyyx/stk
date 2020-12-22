import mariadb
import sys

conn = None


def initConnection():
    try:
        global conn
        conn = mariadb.connect(user="root", password="mariadb", host="192.168.1.9", port=3306, database="istock")
    except mariadb.Error as e:
        print(f'Error connecting to MariaDB Platform: {e}')
        sys.exit(1)


def dbExecute(fun, params=()):
    cursor = conn.cursor()
    fun(cursor, params)
    conn.commit()
