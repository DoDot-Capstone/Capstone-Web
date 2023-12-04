# DB 연결 정보가 저장되어 있는 config
import PythonWeb.db.mysql

user_id=1
user_name=''
user_pw=''
user_em=''
#데이터 옮겨받는 과정 추가할것
sql = "INSERT INTO users (user_id, username, password_hash, email)"
sql += f"VALUES ({user_id}, {user_name}, {user_pw}, {user_em});"

try:
    result=PythonWeb.db.mysql.execute_query(sql)
    #회원가입 성공 페이지+로그인화면으로 돌려보내기
except:
    #회원가입 실패 페이지 ('입력정보를 확인해주세요')+회원가입페이지 새로고침
    pass