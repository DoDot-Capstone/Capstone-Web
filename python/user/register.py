# DB 연결 정보가 저장되어 있는 config
import random
from flask import request, jsonify
import time
import python.db.database

user_name=''
user_pw=''
user_em=''

def get_register():
    #데이터 옮겨받는 과정 추가할것 register.html에 전송과정추가해야함
    data_form_client = request.form
    user_name = data_form_client.get('reg_id')
    user_pw = data_form_client.get('reg_password')
    user_em = data_form_client.get('reg_email')
    now=time.localtime()
    strnow=time.strftime("%Y-%m-%d %H:%M:%S",now)

    sql = "INSERT INTO users (username, password_hash, email, created_at, updated_at)"
    sql += f"VALUES ('{user_name}', '{user_pw}', '{user_em}','{strnow}', '{strnow}');"

    try:
        python.db.database.execute_query(sql)
        return jsonify({'register_success': True})
        #회원가입 성공 페이지+로그인화면으로 돌려보내기
    except Exception as e:
        print("error : ", e)
        #회원가입 실패 페이지 ('입력정보를 확인해주세요')+회원가입페이지 새로고침
        return jsonify({'register_success': False})