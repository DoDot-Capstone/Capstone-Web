from flask import Flask, render_template, request
from db.models.article import Article
from db.models.user import User
from user.register import get_register
from user.login_session import login_get_info
from flask_login import LoginManager, logout_user
from user.user import User

HOST = 'localhost'
PORT = 8080
DEBUG = True
print('실행')
login_manager=LoginManager()
app = Flask(__name__, template_folder='../web', static_folder='../web/static')
login_manager.init_app(app)
app.secret_key = 'super_secret_key'

@app.route("/")
def home():
    return render_template("initial.html")

@app.route("/board")
def board():
    parameter_dict = request.args.to_dict()
    page = 1
    if "page" in parameter_dict.keys():
        page = int(parameter_dict["page"])

    if "search" in parameter_dict.keys():
        search_value = parameter_dict["search"]
        return render_template("board.html", posts = Article.search_article(search_value, page), 
                               search_value = search_value, 
                               page = page, 
                               max_page = Article.get_max_page(search_value))

    else:
        return render_template("board.html", posts=Article.get_all_article(page), 
                               search_value = "", 
                               page = page, 
                               max_page = Article.get_max_page())

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

@app.route("/logout",methods=['GET'])
def logout():
    logout_user()
    return render_template('initial.html')

@app.route("/register", methods=['POST', 'GET'])
def do_reg():
    return get_register()
@app.route("/Introduction")
def Introduction():
    return render_template("Introduction.html")
@app.route("/function")
def function():
    return render_template("function.html")
@login_manager.user_loader
def load_user(user_id):
	return User(user_id)



if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)