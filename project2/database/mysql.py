import mysql
from datetime import datetime
from mysql.connector import pooling

# Connection pool 생성
dbconfig = {
    "host": '203.250.133.118',
    "user": "root",
    "password": "lab303",
    "database": "capstone"
}

pool = pooling.MySQLConnectionPool(
    pool_name="my_pool",
    pool_size=10,
    **dbconfig
)

# Connection pool에서 연결 가져오기
def get_connection():
    return pool.get_connection()