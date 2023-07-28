from flask import Flask, render_template, jsonify, request, redirect, url_for, session, g
import os

app = Flask(__name__)
# python3 -c 'import secrets; print(secrets.token_hex())'
# app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") 
app.config["SECRET_KEY"] = "c73b781f2d9ed26c21ff91a1fad1012676fc5737d7af2c0269271b80fbb6539f"

# g - only test
@app.before_request
def load_user():
    g.user_name = {
        "orc": "orc",
    }
#
@app.route("/", methods=["GET", "POST"])
def home():
    if 'username' in request.form and 'password' in request.form:
        return redirect(url_for("sign_in"))
    return render_template("index.html")

@app.route("/signIn", methods=["POST"])
def sign_in():
        # username = request.args.get('username', 'unknown user')
    username = request.form.get("username")
    password = request.form.get("password")
    checkbox = request.form.get("checkbox")

    if (username in ["admin", "orc", "test"]) and password and checkbox:
        session["signed_in"] = True
        return redirect(url_for("member", username=username))
        # return "Sign in successful for user: {username}".format(username)
    elif not username or not password:
        return redirect(url_for("error", message="Please enter username and password"))
    else:
        return redirect(url_for("error", message="Wrong username or password"))

@app.route("/member/<string:username>")
def member(username): 
    if not session.get("signed_in"):
        return redirect(url_for("error", message="Please sign in first"))
    if session.get("signed_in"):
        USER_IMAGE_MAP = {
            "orc": "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/7c79cbea-6f74-4dd8-86a0-3d9870b26d9f/dd3o7up-a21bc4e7-41b9-4b73-b100-53fe549f38f3.png/v1/fill/w_1024,h_610,q_80,strp/dnd_characters_by_zetrystan_dd3o7up-fullview.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7ImhlaWdodCI6Ijw9NjEwIiwicGF0aCI6IlwvZlwvN2M3OWNiZWEtNmY3NC00ZGQ4LTg2YTAtM2Q5ODcwYjI2ZDlmXC9kZDNvN3VwLWEyMWJjNGU3LTQxYjktNGI3My1iMTAwLTUzZmU1NDlmMzhmMy5wbmciLCJ3aWR0aCI6Ijw9MTAyNCJ9XV0sImF1ZCI6WyJ1cm46c2VydmljZTppbWFnZS5vcGVyYXRpb25zIl19.a944xGWAwpZoUzt_7440RjUupOwoRidMfLEeErdNK1M",
            "admin": url_for("static", filename="rick.jpeg")
        }
        return render_template("member.html", username=username, user_image_map=USER_IMAGE_MAP)
    else:
        return redirect(url_for("home"))
    
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
    IMAGE_MAP = {
        "0": url_for('static', filename='--00.png'),
        "1": url_for('static', filename='--01.png'),
        "2": url_for('static', filename='--02.png'),
        "3": url_for('static', filename='--03.png'),
        "4": url_for('static', filename='--04.png'),
        "5": url_for('static', filename='--05.png'),
        "6": url_for('static', filename='--06.png'),
        "7": url_for('static', filename='--07.png'),
        "8": url_for('static', filename='--08.png'),
        "9": url_for('static', filename='--09.png')
    }
    integer = int(integer)
    squared = int(integer) *int(integer)
    image_urls = [IMAGE_MAP[digit] for digit in str(squared)]
    print(image_urls)
    return render_template("square.html", integer=integer, squared=squared, image_urls=image_urls)

@app.route("/error/")
def error(message):
    # message = request.args.get('message', 'unknown error')
    message = request.args.get('message', 'unknown error')
    return "Error: {}".format(message)

# json - only test
@app.route('/json')
def json():
    return jsonify({'key' : 'value', 'test' : [1, 2, 3]})
#

if __name__ == "__main__":
    app.run(debug=True, port=5000,threaded=True)
    