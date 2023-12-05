from flask import Flask, render_template, request
from datetime import datetime
from database import mysql
from database.models.article import Article
from database.models.user import User
from weblogin.loginsession import login_get_info

app = Flask(__name__, template_folder='html')

@app.route("/")
def home():
    return render_template("initial.html")

@app.route("/board.html")
def board():
    parameter_dict = request.args.to_dict()
    page = parameter_dict["page"]
    return render_template("board.html", posts = Article.load_all_article()[int(page) * 20: (int(page) + 1) * 20 ])

@app.route("/article/<articleNo>.html")
def article(articleNo):
    return render_template("article.html", article = Article.load_article_with_post_id(articleNo))

@app.route("/login.html")
def login():
    return render_template("login.html")

@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/upload.html")
def upload():
    return render_template("upload.html")

@app.route("/users")
def users():
    return {"users": User.load_all_user()}

@app.route("/articles")
def articles():
    return {"articles": Article.load_all_article()}

@app.route("/loginsession")
def login_get_info():
    login_get_info()

if __name__ == "__main__":
    app.run(port = 8080, debug = True, host = "localhost")