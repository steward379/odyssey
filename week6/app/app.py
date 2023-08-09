#環境變數
import os 
from dotenv import load_dotenv
import pathlib
# 加密跟加鹽
import bcrypt 
# session
from flask import Flask, render_template, request, redirect, url_for, session, g
from datetime import datetime

current_path = pathlib.Path(__file__).parent.absolute()

load_dotenv(dotenv_path = current_path.parent / ".env")
# load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
SECRET_KEY = os.environ.get("SECRET_KEY")

# SQLAlchemy 提供 ORM (Object-Relational Mapping) 層，可以使用 Python 物件來操作資料庫
from flask_sqlalchemy import SQLAlchemy

# Oracle 官方 mysql-connector-python

import mysql.connector

# DATABASE_CONFIG = {
#     "host": os.environ.get("DB_HOST", "localhost"),
#     "user": os.environ.get("DB_USER"),
#     "password": os.environ.get("DB_PASS"),
#     "database": os.environ.get("DB_NAME")
# }

# def get_db():
#     return mysql.connector.connect(
#         host=DATABASE_CONFIG['host'],
#         user=DATABASE_CONFIG['user'],
#         password=DATABASE_CONFIG['password'],
#         database=DATABASE_CONFIG['database']
# )

# 內建 sqlite3，但不能用 mysql
# import sqlite3 
# conn = sqlite3.connect('your_database.db') 

app = Flask(__name__)

# 需要加密 ＋ 該從環境變數或配置文件
# URI（Uniform Resource Identifier）是一種用於識別任何資源的字符串。它是一個通用的方式來表示和定位資源
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# python3 -c 'import secrets; print(secrets.token_hex())'
app.secret_key = SECRET_KEY 
# 方法與上相同
# app.config["SECRET_KEY"] = SECRET_KEY 

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

@app.before_request
def load_user():
    g.USER_IMAGE_MAP = {
        "orc": "https://pse.is/56z3by", 
        "admin": url_for("static", filename="images/rick.jpeg")
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
    print(g.USER_IMAGE_MAP)

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
            session["signed_in"] = True
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
    # cursor = conn.cursor(dictionary=True)

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
    # if user and password == user['password']:
    #     session["signed_in"] = True
    #     session["user_id"] = user['id']
    #     session["username"] = user['username']
    #     session["name"] = user['name']
    #     session["follower_count"] = user['follower_count']
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

    # 若是 mysql-connector-python

    # conn = mysql.connector.connect(**DATABASE_CONFIG)
    # cursor = conn.cursor()

    # repeat_query = "SELECT COUNT(*) FROM members WHERE username = %s"
    # cursor.execute(repeat_query, (username,))
    # existing_user = cursor.fetchone()['count']

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
    # USER_IMAGE_MAP = getattr(g, "USER_IMAGE_MAP", None)

    # if not USER_IMAGE_MAP:
    #     return redirect(url_for("error", message="7 No User Image Connected"))

    if not session.get("signed_in"):
        return redirect(url_for("home"))
        # return redirect(url_for("error", message="3: Please sign in first"))

    comments = Comment.query.order_by(Comment.time.desc()).all()

    # conn = mysql.connector.connect(**DATABASE_CONFIG)
    # cursor = conn.cursor(dictionary=True)

    # query = "SELECT * FROM Comment ORDER BY time DESC"
    # cursor.execute(query, ())
    # comments = cursor.fetchall()

    # cursor.close()
    # conn.close()

    username, name = session.get("username", "你是不是沒註冊啊"), session.get("name", "你還沒註冊吧哪有取名")

    # if 'name' in session:
    #     return render_template('member.html', name=session['name'])
    return render_template("member.html", username=username, name=name, comments=comments, user_image_map=g.USER_IMAGE_MAP)

@app.route("/createMessage", methods=["POST"])
def create_message():
    content = request.form.get("content")
    user_id = session.get("user_id")

    if not content or content.strip() == "":
        return redirect(url_for("error", message="10 Please enter content"))
    elif content and user_id:
        comment = Comment(content=content, member_id=user_id, like_count = 0)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("member"))
    elif not user_id:
        return redirect(url_for("error", message="3: Please sign in first"))
    else:
        return redirect(url_for("error", message="0 unknown error"))
    # 若是 mysql-connector-python
    
    # if content and user_id:
    #     conn = get_db()
    #     cursor = conn.cursor()
    #     query = "INSERT INTO comments (content, member_id, like_count) VALUES (%s, %s, 0)"
    #     cursor.execute(query, (content, user_id))
    #     conn.commit()
    #     cursor.close()
    #     conn.close()
    # return redirect(url_for("member"))


@app.route('/deleteMessage', methods=['POST'])
def delete_message():
    comment_id = request.form.get('comment_id')
    comment = Comment.query.get(comment_id)
    user_id = session.get('user_id')

    # 只有當該留言存在，且留言的作者是當前登入的用戶時，才允許刪除
    if comment and comment.member_id == user_id :
        db.session.delete(comment)
        db.session.commit()
    elif not user_id:
        return redirect(url_for("error", message="3: Please sign in first"))
    elif not comment:
        return redirect(url_for("error", message="11: Comment not found"))


    # conn = get_db()
    # cursor = conn.cursor(dictionary=True)

    # cursor.execute("SELECT member_id FROM comments WHERE id = %s", (comment_id,))
    # result = cursor.fetchone()

    # if result and result[0] == user_id:
    #     cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
    #     conn.commit()

    # cursor.close()
    # conn.close()

    return redirect(url_for('member'))

@app.route("/signOut")
def sign_out():
    session.clear()
    # session["signed_in"] = False
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

@app.route("/squared/<string:integer>")
def square(integer):
    try:
        integer = int(integer)
    except ValueError:
        return  redirect(url_for("error", message=" 90 Please enter a positive number"))
    
    squared = integer ** 2
    image_urls = [g.IMAGE_MAP[digit] for digit in str(squared)]

    return render_template("square.html", integer=integer, squared=squared, image_urls=image_urls)

# @app.route("/calc", methods=["POST"])
# def calculate():
#     square_num = request.form.get("square-num")
#     try:
#         square_integer = int(square_num)
#     except ValueError:
#         return redirect(url_for("error", message="Please enter a positive number"))

#     return redirect(url_for("square", integer=square_integer)) if square_integer > 0 else redirect(url_for("error", message="Not a positive integer"))