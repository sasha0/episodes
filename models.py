import os.path
from flask_sqlalchemy import SQLAlchemy
from jinja2.filters import do_truncate

from episodes import app

db = SQLAlchemy(app)


genre_association_table = db.Table('genre_association', db.Model.metadata,
    db.Column('tvseries_id', db.Integer, db.ForeignKey('tvseries.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)


actor_association_table = db.Table('actor_association', db.Model.metadata,
    db.Column('tvseries_id', db.Integer, db.ForeignKey('tvseries.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
)


class TVChannel(db.Model):
    __tablename__ = 'tvchannel'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    logo = db.Column(db.String)
    shows = db.relationship("TVSeries")

    def __unicode__(self):
        return self.title


class TVSeries(db.Model):
    __tablename__ = 'tvseries'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    rating = db.Column(db.String)
    short_description = db.Column(db.String)
    description = db.Column(db.Text)
    genres = db.relationship("Genre", secondary=genre_association_table, backref='genres')
    actors = db.relationship("Actor", secondary=actor_association_table, backref='actors')
    cover = db.Column(db.String)
    tvchannel_id = db.Column(db.Integer, db.ForeignKey('tvchannel.id'))
    tvchannel = db.relationship("TVChannel")

    def __unicode__(self):
        return self.title

    @property
    def cover_thumbnail(self):
        path, ext = os.path.splitext(self.cover)
        return '%s_thumbnail%s' % (path, ext)


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column('id', db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))

    def __init__(self, full_name):
        self.full_name = full_name

    def __unicode__(self):
        return self.full_name

class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(255))

    def __init__(self, title):
        self.title = title

    def __unicode__(self):
        return self.title