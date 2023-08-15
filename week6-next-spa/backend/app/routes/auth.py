from flask import request, redirect, url_for, session, jsonify, Blueprint, render_template
from app.models.member import Member
from app import db
import bcrypt

bp = Blueprint('auth', __name__)

@bp.route("/signIn", methods=["POST"])
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

            # return redirect(url_for('member'))
            return jsonify({"status": "success", "message": "Logged in successfully!"})
        else:
            # return redirect(url_for("error", message="2: 帳密錯誤 Wrong username or password"))
            return jsonify({"status": "error", "message": "Wrong username or password"}), 401

@bp.route("/signUp", methods=["POST"])
def sign_up():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password") 

    existing_user = Member.query.filter_by(username=username).first()
    
    if existing_user:
        # return redirect(url_for("error", message=" 99 帳號已經被註冊 Username already exists"))
        return jsonify({"status": "error", "message": "Username already exists"}), 409

    if not username or not password or not name:
        # return redirect(url_for("error", message="Please fill all fields."))
        return jsonify({"status": "error", "message": "Please fill all fields."}), 400

    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_member = Member(name=name, username=username, password=hashed_pw)
    db.session.add(new_member)
    db.session.commit()

    return jsonify({"status": "success", "message": "User registered successfully!"})

@bp.route("/signOut")
def sign_out():
    session.clear()
    # why not use pop?
    return jsonify({"status": "success", "message": "Logged out successfully!"})

@bp.route("/member/")
def member():
    if not session.get("signed_in"):
        return jsonify({"status": "error", "message": "User not signed in"}), 401

    member_id = session.get("user_id") 
    comments = Comment.query.filter_by(member_id=member_id).order_by(Comment.time.desc()).all()
    
    # 假設Comment模型有一個與成員關聯的屬性，如member, 可以通過這個屬性獲取成員的名稱或其他屬性。
    comments_list = [{"content": c.content, "like_count": c.like_count, "time": c.time} for c in comments]

    username = session.get("username", "你是不是沒註冊啊")
    name = session.get("name", "你還沒註冊吧哪有取名")

    response_data = {
        "status": "success",
        "username": username,
        "name": name,
        "comments": comments_list,
        "user_image_map": g.USER_IMAGE_MAP  # 如果g.USER_IMAGE_MAP是全局可用的，這樣就行。否則，需要確保它已被正確設置。
    }

    return jsonify(response_data)