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

def execute_query(operation):
    try:
        # 연결을 가져옴
        connection = get_connection()
        print('db연결완료')
        # 쿼리 수행
        cursor = connection.cursor(dictionary=True)
        print(operation)
        cursor.execute(operation)
        results = cursor.fetchall()
        connection.commit()
        # 결과 출력


    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'connection' in locals():
            # 연결을 풀에 반환
            connection.close()
        return results