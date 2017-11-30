from flask import Flask
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

manager = Manager(app)
