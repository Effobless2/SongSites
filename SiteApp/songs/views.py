from .app import app, db
from flask import render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from hashlib import sha256
from .models import Author, get_sample, get_authors, get_author, User, Music, get_music
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    next = HiddenField()

    def get_authentificated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators = [DataRequired()])

class UserForm(FlaskForm):
    id = HiddenField("id")
    username = StringField("Username")
    password = PasswordField("Password")
    confirm  = PasswordField("Confirm Password")

    def passwordConfirmed(self):
        return self.password.data == self.confirm.data

class MusicForm(FlaskForm):
    id = HiddenField("id")
    musicName = StringField("Nom de votre musique")
    author = QuerySelectField("Autheur",query_factory = lambda : Author.query.all())

@app.route("/")
def home():
    return render_template(
        "home.html",
        title="Hello World!",
        names = ["Pierre", "Paul", "Corinne"])

@app.route("/musics")
def musics():
    return render_template(
        "musics.html",
        title = "Les musiques",
        musics = get_sample()
    )

@app.route("/authors")
def authors():
    return render_template(
        "authors.html",
        title = "Les Autheurs",
        authors = get_authors())

@app.route("/one-author/<int:id>")
def one_author(id):
    author = get_author(id)
    return render_template(
        "one-author.html",
        author = author)


@app.route("/edit/author/<int:id>")
@login_required
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id = a.id, name = a.name)
    return render_template(
        "edit-author.html",
        author = a,
        form = f)

@app.route("/save/author/", methods=("POST",))
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        a  = get_author(id)
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for('one_author', id = a.id))
    a = get_author(int(f.id.data))
    return render_template(
        "edit-author.html",
        author = id,
        form = f)

@app.route("/new/author/")
@login_required
def new_author():
    f = AuthorForm(id = None, name = None)
    return render_template(
        "create-author.html",
        form = f)

@app.route("/new/author/saving", methods=("POST",))
def save_new_author():
    f = AuthorForm()
    if f.validate_on_submit():
        o = Author(name=f.name.data)
        db.session.add(o)
        db.session.commit()
        return redirect(url_for('one_author', id = o.id))
    return render_template(
        "create-author.html",
        form = f)

@app.route("/login/", methods=("GET","POST",))
def login():
    f = LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authentificated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template(
        "login.html",
        form = f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/new/profile/")
def new_profile():
    f = UserForm()
    return render_template(
        "new-profile.html",
        form = f)

@app.route("/new/profile/saving", methods=("POST",))
def save_new_profile():
    f = UserForm()
    if f.validate_on_submit() and f.passwordConfirmed() and (User.query.get(f.username.data) == None):
        from hashlib import sha256
        m = sha256()
        m.update(f.password.data.encode())
        u = User(username = f.username.data, password = m.hexdigest())
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template(
        "new-profile.html",
        form = f)

@app.route("/new/music/")
@login_required
def new_music():
    f = MusicForm()
    return render_template(
        "new-music.html",
        form = f)

@app.route("/new/music/saving", methods = ("POST",))
@login_required
def new_music_saving():
    f = MusicForm()
    if f.validate_on_submit():
        m = Music(title = f.musicName.data, author_id = f.author.data.id)
        db.session.add(m)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template(
        "new-music.html")

@app.route("/one-music/<int:id>")
def one_music(id):
    m = Music.query.get(id)
    a = Author.query.get(m.author_id)
    return render_template(
        "one-music.html",
        music = m,
        author = a)

@app.route("/edit/music/<int:id>")
@login_required
def edit_music(id):
    m = Music.query.get(id)
    f = MusicForm(id= id, musicName = m.title, author = Author.query.get(m.author_id))
    return render_template(
        "edit-music.html",
        music = m,
        form = f)

@app.route("/save/music/", methods = ("POST",))
def save_music():
    f = MusicForm()
    if f.validate_on_submit():
        id = int(f.id.data)
        m = get_music(id)
        m.title = f.musicName.data
        m.author_id = f.author.data.id
        db.session.commit()
        return redirect(url_for('one_music', id = m.id))
    m = get_music(int(f.id.data))
    return render_template(
        "edit-music.html",
        music = m,
        form = f)


Bootstrap(app)
