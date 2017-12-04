from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
import os.path

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///'+mkpath('../songs.db'))

app.config['SECRET_KEY'] = "bcc090e2-26b2-4c16-84ab-e766cc644320"

app.config['BOOTSTRAP_SERVE_LOCAL'] = True

db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = "login"

manager = Manager(app)
