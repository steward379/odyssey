from flask import Flask, render_template, request, redirect, url_for, session, g
import os
import mysql.connector
import bcrypt

app = Flask(__name__)

app.secret_key = "test_test"

DATABASE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "rootroot",
    "database": "website"
}

# python3 -c 'import secrets; print(secrets.token_hex())'
# app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = "c73b781f2d9ed26c21ff91a1fad1012676fc5737d7af2c0269271b80fbb6539f"


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
    # checkbox = request.form.get("checkbox")

    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    query = "SELECT id, name, username, password, follower_count FROM members WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    # if (username in ["admin", "orc", "test"]) and password and checkbox:
    #     session["signed_in"] = True
    #     return redirect(url_for("member", username=username))
    #     # return "Sign in successful for user: {username}".format(username)

    # if user and bcrypt.checkpw(password, result[0].encode('utf-8')):
    if user and password == user[3]:
        session["signed_in"] = True
        session["user_id"] = user[0]
        session["username"] = user[1]
        session["name"] = user[2]
        session["follower_count"] = user[4]
        # return redirect(url_for("member", username=username))
        return redirect(url_for('member'))
    elif not username or not password:
        return redirect(url_for("error", message="1: Please enter username and password"))
        #  return redirect(url_for("error") + "?message=Please+enter+username+and+password")
    else:
        return redirect(url_for("error", message="2: 帳密錯誤 Wrong username or password"))


@app.route("/signUp", methods=["POST"])
def sign_up():
    name = request.form.get("name")
    username = request.form.get("username")
    password = request.form.get("password")
    # password = request.form.get("password").encode('utf-8')

    if not username or not password or not name:
        return redirect(url_for("error", message="Please fill all fields."))

    # hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

    conn = mysql.connector.connect(**DATABASE_CONFIG)
    cursor = conn.cursor()

    repeat_query = "SELECT COUNT(*) FROM members WHERE username = %s"
    cursor.execute(repeat_query, (username,))
    existing_user = cursor.fetchone()[0]

    if existing_user:
        cursor.close()
        conn.close()
        return redirect(url_for("error", message=" 99 帳號已經被註冊 Username already exists"))

    insert_query = "INSERT INTO members (name, username, password) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (name, username, password))
    conn.commit()

    cursor.close()
    conn.close()

    # 註冊成功，導向首頁
    return redirect(url_for("home"))


# @app.route("/member/<string:username>")
@app.route("/member/")
def member():
    if not session.get("signed_in"):
        return redirect(url_for("home"))
        # return redirect(url_for("error", message="3: Please sign in first"))
    USER_IMAGE_MAP = {
        "orc": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/7c79cbea-6f74-4dd8-86a0-3d9870b26d9f/dd3o7up-a21bc4e7-41b9-4b73-b100-53fe549f38f3.png/v1/fill/w_1024,h_610,q_80,strp/dnd_characters_by_zetrystan_dd3o7up-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NjEwIiwicGF0aCI6IlwvZlwvN2M3OWNiZWEtNmY3NC00ZGQ4LTg2YTAtM2Q5ODcwYjI2ZDlmXC9kZDNvN3VwLWEyMWJjNGU3LTQxYjktNGI3My1iMTAwLTUzZmU1NDlmMzhmMy5wbmciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.a944xGWAwpZoUzt_7440RjUupOwoRidMfLEeErdNK1M",
        "admin": url_for("static", filename="/images/rick.jpeg")
    }

    username, name = session.get(
        "username", "你是不是沒註冊啊"), session.get("name", "你還沒註冊吧哪有取名")

    # if 'name' in session:
    #     return render_template('member.html', name=session['name'])

    return render_template("member.html", username=username, name=name, user_image_map=USER_IMAGE_MAP)


@app.route("/signOut")
def sign_out():
    session["signed_in"] = False
    return redirect(url_for("home"))

# @app.route("/calc", methods=["POST"])
# def calculate():

    # square_num = request.form.get("square-num")
    # try:
    # square_integer = int(square_num)
    # except ValueError:
    # return redirect(url_for("error", message="Please enter a positive number"))

    # return redirect(url_for("square", integer=square_integer)) if square_integer > 0 else redirect(url_for("error", message="Not a positive integer"))


@app.route("/squared/<string:integer>")
def square(integer):
    integer = int(integer)
    squared = int(integer) * int(integer)
    image_urls = [g.IMAGE_MAP[digit] for digit in str(squared)]
    print(image_urls)
    return render_template("square.html", integer=integer, squared=squared, image_urls=image_urls)

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
