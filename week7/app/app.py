import os 
import re
from dotenv import load_dotenv
import pathlib
import bcrypt 
from flask import Flask, render_template, request, redirect, url_for, session, g, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

current_path = pathlib.Path(__file__).parent.absolute()

load_dotenv(dotenv_path = current_path.parent / ".env")

# production

# import pymysql

# pymysql.install_as_MySQLdb()

# connection = pymysql.connect(
#   host=os.getenv("HOST"),
#   user=os.getenv("USERNAME"),
#   passwd=os.getenv("PASSWORD"),
#   db=os.getenv("DATABASE"),
#   autocommit=True,
#   ssl={
#     "ca": "/etc/ssl/cert.pem"
#   }
# )

DATABASE_URL = os.environ.get("DATABASE_URL")
# DATABASE_CONFIG = {
#     "host": os.environ.get("DB_HOST", "localhost"),
#     "user": os.environ.get("DB_USER"),
#     "password": os.environ.get("DB_PASS"),
#     "database": os.environ.get("DB_NAME")
# }
SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = SECRET_KEY 

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

# @app.route("/", methods=["GET", "POST"])
@app.route("/")
def home():
    # if request.method == "POST" and 'username' in request.form and 'password' in request.form:
    #     return redirect(url_for("sign_in"))
    return render_template("index.html")

@app.route("/signIn", methods=["POST"])
def sign_in():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not username or not password:
        return redirect(url_for("error", message="1: Please enter username and password"))

    old_member = Member.query.filter_by(username=username).first()

    if old_member:
        if bcrypt.checkpw(password.encode('utf-8'), old_member.password.encode('utf-8')):
            session["signed_in"] = True
            session["user_id"] = old_member.id
            session["username"] = old_member.username
            session["name"] = old_member.name
            session["follower_count"] = old_member.follower_count

            return redirect(url_for('member'))
        else:
            return redirect(url_for("error", message="2: 帳密錯誤 Wrong username or password"))
    else:
        return redirect(url_for("error", message="3: 帳密錯誤 Wrong username or password"))

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

@app.route("/member/")
def member():
    # USER_IMAGE_MAP = getattr(g, "USER_IMAGE_MAP", None)

    if not session.get("signed_in"):
        return redirect(url_for("home"))

    comments = Comment.query.order_by(Comment.time.desc()).all()
    
    username, name, user_id = session.get("username", "你是不是沒註冊啊"), session.get("name", "你還沒註冊吧哪有取名"), session.get("user_id", "id error")
    
    return render_template("member.html", username=username, name=name, comments=comments, user_image_map=g.USER_IMAGE_MAP, user_id=user_id)

@app.route("/createMessage", methods=["POST"])
def create_message():
    # content = request.form.get("content")
    content = request.json.get("content")
    user_id = session.get("user_id")

    if not content or content.strip() == "":
        # return redirect(url_for("error", message="10 Please enter content"))
          return jsonify({"error": "Please enter content"}), 400
    elif content and user_id:
        comment = Comment(content=content, member_id=user_id, like_count = 0)
        db.session.add(comment)
        db.session.commit()
        # return redirect(url_for("member"))
        return jsonify({
            "message": "Comment added", 
            "comment": {
                "id": comment.id,
                "member_name": comment.member.name,
                "content": comment.content,
                "member_id": comment.member_id,
                "time": comment.time.strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    # elif not user_id:
    #     return redirect(url_for("error", message="3: Please sign in first"))
    else:
        # return redirect(url_for("error", message="0 unknown error"))
        return jsonify({"error": "unknown error"}), 400

@app.route('/deleteMessage', methods=['POST'])
def delete_message():
    # comment_id = request.form.get('comment_id')
    comment_id = request.json.get('comment_id') 
    comment = Comment.query.get(comment_id)
    user_id = session.get('user_id')

    if comment and comment.member_id == user_id :
        db.session.delete(comment)
        db.session.commit()
        # 
        return jsonify({"message": "Comment deleted"})
    elif not user_id:
        # return redirect(url_for("error", message="3: Please sign in first"))
        return jsonify({"error": "Please sign in first"}), 401
    elif not comment:
        # return redirect(url_for("error", message="11: Comment not found"))
        return jsonify({"error": "Comment not found"}), 404
    
    # return redirect(url_for('member'))
    return jsonify({"error": "unknown error"}), 400

@app.route("/signOut")
def sign_out():
    session.clear()
    return redirect(url_for("home"))

@app.route("/error/")
def error():
    message = request.args.get('message', '0 unknown error')
    message = message.replace('+', ' ')  # replace '+' with space
    messages = []
    buffer = '' 

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

@app.route("/api/member", methods=["GET"])
def api_member():
    username = request.args.get("username")

    if not username:
        return jsonify(data = None), 400  

    member = Member.query.filter_by(username = username).first()

    if member:
        response_data = {
            "data": {
                "id": member.id,
                "name": member.name,
                "username": member.username
            }
        }
        return jsonify(response_data)
    else:
        return jsonify(data = None), 404  
    
@app.route("/api/getUserId", methods=["GET"])
def get_user_id():
    # 从 session 中获取 user_id
    user_id = session.get("user_id")
    if user_id:
        return jsonify({"user_id": user_id})
    else:
        return jsonify({"error": "User not signed in."}), 401  # 401 Unauthorized
    


@app.route("/api/getComments", methods=["GET"])
def get_comments():
    page = int(request.args.get("page", 1))
    items_per_page = 30

    # comments = Comment.query.order_by(Comment.time.desc()).all()
    pagination = Comment.query.order_by(Comment.time.desc()).paginate(page=page, per_page=items_per_page, error_out=False)
    comments = pagination.items
    
    comments_data = [{
        "id": comment.id,
        "content": comment.content,
        "time": comment.time.strftime('%Y-%m-%d %H:%M:%S'),
        "member_id": comment.member_id,
        "member_name": comment.member.name
    } for comment in comments]

    pagination_data = {
        "current_page": pagination.page,
        "total_pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
        "comments": comments_data
    }
    # return jsonify(comments_data)  
    return jsonify(pagination_data)
    
@app.route("/api/member", methods=["PATCH"])
def patch_member_name():
    if not session.get("signed_in"):
        return jsonify(error=True), 403

    data = request.json

    new_name = data.get("name", "").strip()
    print(new_name)
    # if not new_name or not valid_name(new_name):
    if not new_name:
        return jsonify(error=True), 400

    current_member = Member.query.get(session.get("user_id"))

    if current_member:
        current_member.name = new_name
        session["name"] = new_name
        db.session.commit()
        return jsonify(ok=True)
    else:
        return jsonify(error=True), 404
    
    
    
# @app.route("/api/createMessage", methods=["POST"])
# def create_message():
#     content = request.form.get("content")
#     user_id = session.get("user_id")

#     if not content or content.strip() == "":
#         return jsonify(status="error", message="Please enter content"), 400
#     elif content and user_id:
#         comment = Comment(content=content, member_id=user_id, like_count=0)
#         db.session.add(comment)
#         db.session.commit()
#         return jsonify(status="success", message="Comment added successfully", comment_id=comment.id), 200
#     elif not user_id:
#         return jsonify(status="error", message="Please sign in first"), 400
#     else:
#         return jsonify(status="error", message="Unknown error"), 400


if __name__ == "__main__":
    app.run(debug=True, port=3000, threaded=True)

# def valid_name(name):
#     # return re.match("^[A-Za-z0-9 ]+$", name) is not None
#     if not name.strip():
#         return False
        
#     allowed_pattern = re.compile(r'^[a-zA-Z\u4e00-\u9fa5\s\U00010000-\U0010ffff]+$')
#     if not allowed_pattern.match(name):
#         return False
    
#     # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
#     if name.strip() in string.punctuation:
#         return False

#     forbidden_chars = [">", "<", ";", ":", "=", "'", "\"", "/", "\\", "{", "}", "[" ,"]" ]
#     for char in forbidden_chars:
#         if char in name:
#             return False
#     return True