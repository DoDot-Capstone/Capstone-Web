from flask import Flask, render_template, redirect, request, url_for
from markupsafe import escape

HOST = 'localhost'
PORT = 8080
DEBUG = False

app = Flask(__name__, template_folder='web')

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