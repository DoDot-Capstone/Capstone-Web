from flask import Flask, render_template, redirect, request, url_for
import flask_login # @login_required를 통해 로그인 권한이 필요한 기능을 통제할수있다
from markupsafe import escape
import app

HOST = 'localhost'
PORT = 8080
DEBUG = False

app = app.create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page1/<int:id>')
def page1(id):
    return render_template('page1.html', number=id)

@app.route('/page2/<path:str>')
def page2(str):
    return render_template('page2.html', data=escape(str))

@app.route('/page3/<username>')
def page3(username):
    return render_template('page3.html', name=escape(username))

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)