from .app import app
from flask import render_template
from .models import get_sample, get_authors

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
        authors = get_authors()
    )


from flask_bootstrap import Bootstrap

app.config['BOOTSTRAP_SERVE_LOCAL'] = True

Bootstrap(app)
