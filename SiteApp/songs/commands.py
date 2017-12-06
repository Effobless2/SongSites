from .app import manager, db

@manager.command
def loaddb(filename):
    '''Creates the tables and populates them with data.'''

    #création de toutes les tables
    db.create_all()

    #chargement du jeu de notre base de données
    import yaml
    musics = yaml.load(open(filename))


    #import des modèles
    from .models import Author, Music

    #première passe : créationdes autheurs
    authors = {}
    for m in musics:
        a = m["author"]
        if a not in authors :
            o = Author(name=a)
            db.session.add(o)
            authors[a] = o
    db.session.commit()

    #deuxième passe : création de tous les Livres
    for m in musics:
        a = authors[m["author"]]
        o = Music(title      = m["title"],
                  img        = m["img"]  ,
                  author_id  = a.id      )
        db.session.add(o)
    db.session.commit()


@manager.command
def syncdb():
    """
    Creates all missing tables
    """
    db.create_all()


@manager.command
def newuser(username, password):
    """
    Adds a new user
    """
    from .models import User
    if User.query.get(username)!=None:
        return "User already exist"
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = User(username = username, password = m.hexdigest())
    db.session.add(u)
    db.session.commit()

@manager.command
def passwd(username,newPassword):
    """
    Change the password of username in database
    if he exists in
    """
    from .app import db
    from .models import User
    from hashlib import sha256
    u = User.query.get(username)
    if u!=None:
        m = sha256()
        m.update(newPassword.encode())
        u.password = m.hexdigest()
        db.session.commit()
    else:
        return "User doesn't exist. Verify your username and try again."
