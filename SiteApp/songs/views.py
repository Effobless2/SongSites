from .app import app, db
from flask import render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_login import current_user, login_user, logout_user
from flask_wtf import FlaskForm
from hashlib import sha256
from .models import Author, get_sample, get_authors, get_author, User
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")

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

@app.route("/one-author/<int:a>")
def one_author(a):
    author = get_author(a)
    return render_template(
        "one-author.html",
        author = author)


@app.route("/edit/author/<int:id>")
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
        return redirect(url_for('one_author', a = a.id))
    a = get_author(int(f.id.data))
    return render_template(
        "edit-author.html",
        author = a,
        form = f)

@app.route("/new/author/")
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
        return redirect(url_for('one_author', a = o.id))
    return render_template(
        "create-author.html",
        form = f)

@app.route("/login/", methods=("GET","POST",))
def login():
    f = LoginForm()
    if f.validate_on_submit():
        user = f.get_authentificated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template(
        "login.html",
        form = f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))

Bootstrap(app)
