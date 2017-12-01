from .app import app, db
from flask import render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from .models import Author, get_sample, get_authors, get_author
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

app.config['BOOTSTRAP_SERVE_LOCAL'] = True

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




Bootstrap(app)
