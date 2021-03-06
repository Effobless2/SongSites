print("Version database")

from .app import db, login_manager
from flask_login import UserMixin

MUSICS_BY_PAGES = 20
AUTHOR_BY_PAGE  = 20

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
    title     = db.Column(db.String(100))
    img       = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author    = db.relationship("Author",
                                backref=db.backref("music", lazy="dynamic"))
    def __repr__(self):
        return "<Music (%d) %s>" % (self.id, self.title)

class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))

    def get_id(self):
        return self.username

association_Playlist_Music = db.Table("association_Playlist_Music",
                             db.metadata,
                             db.Column("music", db.Integer, db.ForeignKey("music.id"), primary_key=True),
                             db.Column("playlist", db.Integer, db.ForeignKey("playlist.id"), primary_key=True))

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    img = db.Column(db.String(100))
    musiclist = db.relationship("Music",
                             secondary= association_Playlist_Music, lazy="dynamic",
                             backref = db.backref("musics", lazy=True))
    def getMusicList(self):
        return self.musiclist


def get_number_of_pages_music():
    nbliste = Music.query.count()
    if nbliste%MUSICS_BY_PAGES != 0:
        return (nbliste//MUSICS_BY_PAGES)+1
    return nbliste//MUSICS_BY_PAGES

def get_sample_for_music():
    return Music.query.order_by(Music.title)

def get_sample_for_page_music(page):
    return get_sample_for_music()[(page-1)*MUSICS_BY_PAGES:page*MUSICS_BY_PAGES]

def get_number_of_pages_author():
    nbliste = Author.query.count()
    if nbliste%AUTHOR_BY_PAGE != 0:
        return (nbliste//AUTHOR_BY_PAGE)+1
    return nbliste//AUTHOR_BY_PAGE

def get_sample_for_author():
    return Author.query.order_by(Author.name)

def get_sample_for_page_authors(page):
    return get_sample_for_author()[(page-1)*AUTHOR_BY_PAGE:page*AUTHOR_BY_PAGE]

def get_author(id):
    return Author.query.get(id)

def get_music(id):
    return Music.query.get(id)

def get_playlists():
    return Playlist.query.all()

def get_playlist(id):
    return Playlist.query.get(id)

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
