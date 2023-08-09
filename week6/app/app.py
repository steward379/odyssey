#環境變數
import os 
from dotenv import load_dotenv
import pathlib
# 加密跟加鹽
import bcrypt 
# session
from flask import Flask, render_template, request, redirect, url_for, session, g
from datetime import datetime
# Oracle 官方 mysql-connector-python
# import mysql.connector

# 內建 sqlite3，但不能用 mysql
# import sqlite3 
# conn = sqlite3.connect('your_database.db') 

# SQLAlchemy 提供 ORM (Object-Relational Mapping) 層，可以使用 Python 物件來操作資料庫
from flask_sqlalchemy import SQLAlchemy #

app = Flask(__name__)

# 需要加密 ＋ 該從環境變數或配置文件

# URI（Uniform Resource Identifier）是一種用於識別任何資源的字符串。它是一個通用的方式來表示和定位資源

current_path = pathlib.Path(__file__).parent.absolute()

load_dotenv(dotenv_path = current_path.parent / ".env")
# load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = SECRET_KEY 

app.secret_key = "test_test"
db = SQLAlchemy(app)
class Member(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    follower_count = db.Column(db.Integer, nullable=False, default=0)
    time = db.Column(db.DateTime, default=datetime.utcnow) 
    comments = db.relationship('Comment', backref='member', lazy=True)
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    member_id = db.Column(db.BigInteger, db.ForeignKey('members.id'), nullable=False)

DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "rootroot",
    "database": "website"
}

# python3 -c 'import secrets; print(secrets.token_hex())'
# app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

@app.before_request
def load_user():
    g.user_name = {
        "orc": "orc",
    }
    g.IMAGE_MAP = {
        "0": url_for('static', filename='images/--00.png'),
        "1": url_for('static', filename='images/--01.png'),
        "2": url_for('static', filename='images/--02.png'),
        "3": url_for('static', filename='images/--03.png'),
        "4": url_for('static', filename='images/--04.png'),
        "5": url_for('static', filename='images/--05.png'),
        "6": url_for('static', filename='images/--06.png'),
        "7": url_for('static', filename='images/--07.png'),
        "8": url_for('static', filename='images/--08.png'),
        "9": url_for('static', filename='images/--09.png')
    }

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        return redirect(url_for("sign_in"))
    return render_template("index.html")

@app.route("/signIn", methods=["POST"])
def sign_in():
    # username = request.args.get('username', 'unknown user')
    username = request.form.get("username")
    password = request.form.get("password")

    old_member = Member.query.filter_by(username=username).first()

    if old_member:
        if bcrypt.checkpw(password.encode('utf-8'), old_member.password.encode('utf-8')):
            session["user_id"] = old_member.id
            session["username"] = old_member.username
            session["name"] = old_member.name
            session["follower_count"] = old_member.follower_count

            return redirect(url_for('member'))
             # return "Sign in successful for user: {username}".format(username)
        elif not username or not password:
            return redirect(url_for("error", message="1: Please enter username and password"))
         #  return redirect(url_for("error") + "?message=Please+enter+username+and+password")
        else:
            return redirect(url_for("error", message="2: 帳密錯誤 Wrong username or password"))
        
    # 若是 mysql-connector-python

    # conn = mysql.connector.connect(**DATABASE_CONFIG)
    # cursor = conn.cursor()

    # query = "SELECT id, name, username, password, follower_count FROM members WHERE username = %s"
    # cursor.execute(query, (username,))
    # user = cursor.fetchone()

    # cursor.close()
    # conn.close()
              
    # 硬編碼   

    # if (username in ["admin", "orc", "test"]) and password and checkbox:
    #     session["signed_in"] = True
    #     return redirect(url_for("member", username=username))
    #    

    # 若是 mysql-connector-python

    # if user and bcrypt.checkpw(password, result[0].encode('utf-8')):
    # if user and password == user[3]:
    #     session["signed_in"] = True
    #     session["user_id"] = user[0]
    #     session["username"] = user[1]
    #     session["name"] = user[2]
    #     session["follower_count"] = user[4]
    #     # return redirect(url_for("member", username=username))
          # return "Sign in successful for user: {username}".format(username)
        # return redirect(url_for('member'))

@app.route("/signUp", methods=["POST"])
def sign_up():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password") 

    existing_user = Member.query.filter_by(username=username).first()
    
    if existing_user:
        return redirect(url_for("error", message=" 99 帳號已經被註冊 Username already exists"))

    if not username or not password or not name:
        return redirect(url_for("error", message="Please fill all fields."))

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_member = Member(name=name, username=username, password=hashed_pw)
    db.session.add(new_member)
    db.session.commit()

    return redirect(url_for("home"))

    # conn = mysql.connector.connect(**DATABASE_CONFIG)
    # cursor = conn.cursor()

    # repeat_query = "SELECT COUNT(*) FROM members WHERE username = %s"
    # cursor.execute(repeat_query, (username,))
    # existing_user = cursor.fetchone()[0]

    # if existing_user:
    #     cursor.close()
    #     conn.close()
    #     return redirect(url_for("error", message=" 99 帳號已經被註冊 Username already exists"))

    # insert_query = "INSERT INTO members (name, username, password) VALUES (%s, %s, %s)"
    # cursor.execute(insert_query, (name, username, password))
    # conn.commit()

    # cursor.close()
    # conn.close()

    # return redirect(url_for("home"))

# @app.route("/member/<string:username>")
@app.route("/member/")
def member():
    if not session.get("signed_in"):
        return redirect(url_for("home"))
        # return redirect(url_for("error", message="3: Please sign in first"))
    USER_IMAGE_MAP = {
        "Orc": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/7c79cbea-6f74-4dd8-86a0-3d9870b26d9f/dd3o7up-a21bc4e7-41b9-4b73-b100-53fe549f38f3.png/v1/fill/w_1024,h_610,q_80,strp/dnd_characters_by_zetrystan_dd3o7up-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NjEwIiwicGF0aCI6IlwvZlwvN2M3OWNiZWEtNmY3NC00ZGQ4LTg2YTAtM2Q5ODcwYjI2ZDlmXC9kZDNvN3VwLWEyMWJjNGU3LTQxYjktNGI3My1iMTAwLTUzZmU1NDlmMzhmMy5wbmciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.a944xGWAwpZoUzt_7440RjUupOwoRidMfLEeErdNK1M",
        "Admin": url_for("static", filename="/images/rick.jpeg")
    }

    comments = Comment.query.order_by(Comment.time.desc()).all()

    username, name = session.get("username", "你是不是沒註冊啊"), session.get("name", "你還沒註冊吧哪有取名")

    # if 'name' in session:
    #     return render_template('member.html', name=session['name'])

    return render_template("member.html", username=username, name=name, comments=comments, user_image_map=USER_IMAGE_MAP)

@app.route("/createMessage", methods=["POST"])
def create_message():
    content = request.form.get("content")
    user_id = session.get("user_id")

    if content and user_id:
        comment = Comment(content=content, member_id=user_id, like_count = 0)
        db.session.add(comment)
        db.session.commit()

    return redirect(url_for("member"))


@app.route('/deleteMessage', methods=['POST'])
def delete_message():
    comment_id = request.form.get('comment_id')
    comment = Comment.query.get(comment_id)

    # 只有當該留言存在，且留言的作者是當前登入的用戶時，才允許刪除
    if comment and comment.member_id == session.get('user_id'):
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('member'))

@app.route("/signOut")
def sign_out():
    # session.clear()
    session["signed_in"] = False
    return redirect(url_for("home"))

# @app.route("/error/<string:message>")


@app.route("/error/")
# def error(message):
def error():
    message = request.args.get('message', '0 unknown error')
    message = message.replace('+', ' ')  # replace '+' with space
    messages = []
    buffer = ''  # 避免文字因為成為獨立元素而變成等距

    for char in message:
        if char.isdigit():
            if buffer:
                messages.append(('char', buffer))
            messages.append(('img', g.IMAGE_MAP[char]))
        else:
            buffer += char
    if buffer:
        messages.append(('char', buffer))

    return render_template("error.html", messages=messages, message=message)
    # return "Error: {}".format(message)


if __name__ == "__main__":
    app.run(debug=True, port=3000, threaded=True)

# 平方作業

# @app.route("/squared/<string:integer>")
# def square(integer):
#     integer = int(integer)
#     squared = int(integer) * int(integer)
#     image_urls = [g.IMAGE_MAP[digit] for digit in str(squared)]
#     print(image_urls)
#     return render_template("square.html", integer=integer, squared=squared, image_urls=image_urls)

# @app.route("/calc", methods=["POST"])
# def calculate():

    # square_num = request.form.get("square-num")
    # try:
    # square_integer = int(square_num)
    # except ValueError:
    # return redirect(url_for("error", message="Please enter a positive number"))

    # return redirect(url_for("square", integer=square_integer)) if square_integer > 0 else redirect(url_for("error", message="Not a positive integer"))
