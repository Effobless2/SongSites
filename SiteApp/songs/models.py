print("Version database")

from .app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

class Author(db.Model):
    """
    Create an instance of author
    """
    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    def __repr__(self):
        return "<Author (%d) %s>" % (self.id, self.name)


class Music(db.Model):
    """
    Create an instance of Music
    """
    id        = db.Column(db.Integer, primary_key=True)
    price     = db.Column(db.Float)
    title     = db.Column(db.String(100))
    url       = db.Column(db.String(100))
    img       = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author    = db.relationship("Author",
                                backref=db.backref("music", lazy="dynamic"))
    def __repr(self):
        return "<Music (%d) %s>" % (self.id, self.title)

class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))

    def get_id(self):
        return self.username

def get_sample():
    return Music.query.limit(10).all()

def get_authors():
    return Author.query.limit(10).all()

def get_author(id):
    return Author.query.get(id)
# print("Version YAML")

# import yaml, os.path
# Books = yaml.load(
#     open(
#         os.path.join(
#             os.path.dirname(os.path.dirname(__file__)),
#             "data.yml"
#         )
#     )
# )
#
# def get_sample():
#     return Books[0:10]
