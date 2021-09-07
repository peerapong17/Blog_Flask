import os
from flask import Flask
from datetime import timedelta
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

login_manager = LoginManager()

app = Flask(__name__)
CORS(app)
app.permanent_session_lifetime = timedelta(days=30)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.sqlite')
app.config["SECRET_KEY"] = "little secret"
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/uploads/')
# app.register_blueprint(blog, url_prefix="/blog")

db = SQLAlchemy(app)

login_manager.init_app(app)

login_manager.login_view = "login"

