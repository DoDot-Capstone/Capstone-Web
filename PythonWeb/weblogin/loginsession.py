from flask import render_template, redirect, request, url_for
from login import app
from flask_login import login_user, logout_user

import user


@app.route('/')
def root():
    return redirect('/login')


@app.route('/login')
def login():
    return render_template('common/template_login.html')


# 로그인 실행
# 로그인 계정 정보는 post로 받아오지만
# 일반 리소스들은 get으로 받아오므로 get과 post모두 선언해줘야 한다.
@app.route('/login/get_info', methods=['GET', 'POST'])
def login_get_info():
    user_id = request.form.get('userID')
    user_pw = request.form.get('userPW')

    if user_id is None or user_pw is None:
        return redirect('/relogin')

    # 사용자가 입력한 정보가 회원가입된 사용자인지 확인
    user_info = user.User.get_user_info(user_id, user_pw)

    if user_info['result'] != 'fail' and user_info['count'] != 0:
        # 사용자 객체 생성
        login_info = user.User(user_id=user_info['data'][0]['USER_ID'])
        # 사용자 객체를 session에 저장
        login_user(login_info)
        return redirect('/main')
    else:
        return redirect('/relogin')


# 로그인 실패 시 재로그인
@app.route('/relogin')
def relogin():
    login_result_text = "로그인에 실패했습니다. 다시 시도해주세요."

    return render_template('common/template_login.html', login_result_text=login_result_text)


# 로그아웃
@app.route('/logout')
def logout():
    # session 정보를 삭제한다.
    logout_user()
    return redirect('/')