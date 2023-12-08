from flask import Flask, render_template, request, redirect, url_for
from db.models.article import Article
from user.register import get_register
from gpt.chatgpt import getGptReply
from python.gpt.search import getSearchReply
from user.login_auth import login_get_info
from flask_login import LoginManager, logout_user, current_user
from flask_login.mixins import AnonymousUserMixin
from user.user import User

HOST = 'localhost'
PORT = 8080
DEBUG = True

print('실행')

login_manager = LoginManager()
app = Flask(__name__, template_folder='../web', static_folder='../web/static')
login_manager.init_app(app)
app.secret_key = 'super_secret_key'

@app.route("/")
def home():
    return render_template("initial.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/auth", methods=['POST', 'GET'])
def login_auth():
    return login_get_info()

@app.route("/logout",methods=['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('home'))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=['POST', 'GET'])
def do_reg():
    return get_register()

@login_manager.user_loader
def load_user(user_id):
	return User(user_id)

@app.route("/introduction")
def introduction():
    return render_template("introduction.html")

@app.route("/function")
def function():
    # 현재 사용자가 인증되었는지 확인합니다
    if current_user.is_authenticated:
        # 사용자가 인증되었으면 "function.html" 템플릿을 렌더링합니다.
        return render_template("function.html")
    else:
        # 사용자가 인증되지 않았다면 로그인 페이지로 리다이렉트합니다.
        return redirect(url_for('login'))

@app.route("/function", methods=['POST', 'GET'])
def do_gpt():
    return getGptReply()
@app.route("/search", methods=['POST', 'GET'])
def search():
    return getSearchReply()

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/upload", methods = ["POST"])
def upload_request():
    if isinstance(current_user, AnonymousUserMixin):
        status = 403

    else:
        user_id = current_user.user_id
        formdata = request.form
        title = formdata.get("title")
        content = formdata.get("content")
        status = Article.insert_article(title, content, user_id)
        
    return app.response_class(response={}, status = status)

@app.route("/delete/<articleNo>", methods = ["POST"])
def delete_article(articleNo):
    if (isinstance(current_user, AnonymousUserMixin)):
        status = 403

    else:
        user_id = current_user.user_id
        status = Article.delete_article(articleNo, user_id)

    return app.response_class(response={}, status = status)

@app.route("/board")
def board():
    parameter_dict = request.args.to_dict()
    page = 1
    count = 15
    if "page" in parameter_dict.keys():
        page = int(parameter_dict["page"])

    if "count" in parameter_dict.keys():
        count = int(parameter_dict["count"])

    if "search" in parameter_dict.keys():
        search_value = parameter_dict["search"]
        return render_template("board.html", posts=Article.search_article(search_value, page, count),
                                search_value=search_value,
                                page=page,
                                max_page=Article.get_max_page(search_value))

    else:
        return render_template("board.html", posts=Article.get_all_article(page, count),
                                search_value="",
                                page=page,
                                max_page=Article.get_max_page())

@app.route("/article/<articleNo>")
def article(articleNo):
    return render_template("article.html", article=Article.load_article_with_post_id(articleNo))


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
