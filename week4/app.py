from flask import Flask, render_template, jsonify, request, redirect, url_for, session, g

app = Flask(__name__)
# python3 -c 'import secrets; print(secrets.token_hex())'
app.config["SECRET_KEY"] = "cb79f46dcedb0ac7c48fe7cd07aa2e0295585da21b6dfb479d4728bef2507559"

@app.before_request
def load_user():
    g.user_name = {
        "orc": "orc",
    }

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        return redirect(url_for("sign_in", username=username))
    
    return render_template("index.html")

@app.route("/signIn", methods=["GET", "POST"])
def sign_in():
    username = request.form.get("username")
    # username = request.args.get('username', 'unknown user')
    password = request.form.get("password")
    checkbox = request.form.get("checkbox")

    if (username in ["admin", "orc", "test"]) and password and checkbox:
        session["signed_in"] = True
        return redirect(url_for("member", username=username))
        # return "Sign in successful for user: {username}".format(username)
    else:
        return redirect(url_for("error", message="Wrong username or password"))
    
@app.route("/calc", methods=["GET", "POST"])
def calculate():
    square_num = request.form.get("square-num")
    try:
        square_integer = int(square_num)
    except ValueError:
        return redirect(url_for("error", message="Please enter a positive number"))

    return redirect(url_for("square", integer=square_integer)) if square_integer > 0 else redirect(url_for("error", message="Not a positive integer"))
        
@app.route("/square/<string:integer>")
def square(integer):
    integer = int(integer)
    return render_template("square.html", integer=integer)

@app.route("/member/<string:username>")
def member(username): 
    if not session.get("signed_in"):
        return redirect(url_for("error", message="Please sign in first"))
    if "signed_in" in session and session["signed_in"]:
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

@app.route("/error/<string:message>")
def error(message):
    # message = request.args.get('message', 'unknown error')
    return "Error: {}".format(message)

@app.route('/json')
def json():
    return jsonify({'key' : 'value', 'test' : [1, 2, 3]})

if __name__ == "__main__":
    app.run(debug=True, port=5000,threaded=True)
    