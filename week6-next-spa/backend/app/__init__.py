from flask import Flask, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# Allow cross-origin requests, but in production, limit this to just the domain of your Next.js app.
from .config import DATABASE_URI, SECRET_KEY

# Flask-Login

# app = Flask(__name__)
# CORS(app)

# app.config.from_object('path_to_config_module.Config')
db = SQLAlchemy()

def create_app():

    app = Flask(__name__)
    
    # Allow cross-origin requests, but in production, limit this to just the domain of your Next.js app.
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config["SECRET_KEY"] = SECRET_KEY 

    db.init_app(app)

    from .routes import auth, comments, errors
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(comments.bp)
    app.register_blueprint(errors.bp)

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
    return app