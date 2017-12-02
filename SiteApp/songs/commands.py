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
        o = Music(price     = m["price"],
                 title      = m["title"],
                 url        = m["url"]  ,
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
