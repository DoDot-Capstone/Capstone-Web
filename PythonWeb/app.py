# app.py

from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='web')
    # 여기에 애플리케이션 설정 및 라우트 등을 추가
    return app
