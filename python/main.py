from flask import Flask, render_template, request
from db.models.article import Article
from db.models.user import User
from user.register import get_register
from user.login_session import login_get_info

HOST = 'localhost'
PORT = 8080
DEBUG = True

print('실행')
app = Flask(__name__, template_folder='../web', static_folder='../web/static')

@app.route("/")
def home():
    return render_template("initial.html")

@app.route("/board")
def board():
    parameter_dict = request.args.to_dict()
    page = parameter_dict["page"]
    return render_template("board.html", posts=Article.load_all_article()[int(page) * 20: (int(page) + 1) * 20 ])

@app.route("/article/<articleNo>")
def article(articleNo):
    return render_template("article.html", article=Article.load_article_with_post_id(articleNo))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/users")
def users():
    return {"users": User.load_all_user()}

@app.route("/articles")
def articles():
    return {"articles": Article.load_all_article()}

@app.route("/loginsession", methods=['POST', 'GET'])
def login_info():
    return login_get_info()

@app.route("/register", methods=['POST', 'GET'])
def do_reg():
    return get_register()

@app.route("/function")
def function():
    return render_template("function.html")


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)