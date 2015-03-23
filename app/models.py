import os.path
from flask.ext.security import UserMixin, RoleMixin

from . import db


genre_association_table = db.Table('genre_association', db.Model.metadata,
    db.Column('tvseries_id', db.Integer, db.ForeignKey('tvseries.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('userroles.id')))


class TVChannel(db.Model):
    __tablename__ = 'tvchannel'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    logo = db.Column(db.String)
    tvseries = db.relationship("TVSeries", order_by='desc(TVSeries.rating)', lazy='dynamic')

    def __unicode__(self):
        return self.title

    @property
    def logo_thumbnail(self):
        path, ext = os.path.splitext(self.logo)
        return '%s_thumbnail%s' % (path, ext)

    @property
    def popular_tvseries(self):
        return list(self.tvseries.limit(5))


class Episode(db.Model):
    __tablename__ = 'episode'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    episode_number = db.Column(db.Integer)
    season_number = db.Column(db.Integer)
    showed_at = db.Column(db.Date)
    tvseries_id = db.Column(db.Integer, db.ForeignKey('tvseries.id'))
    tvseries = db.relationship("TVSeries")


class TVSeries(db.Model):
    __tablename__ = 'tvseries'

    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    rating = db.Column(db.String)
    short_description = db.Column(db.String)
    description = db.Column(db.Text)
    genres = db.relationship("Genre", secondary=genre_association_table, backref='genres')
    cover = db.Column(db.String)
    tvchannel_id = db.Column(db.Integer, db.ForeignKey('tvchannel.id'))
    tvchannel = db.relationship("TVChannel")
    episodes = db.relationship("Episode")
    roles = db.relationship("Role", lazy='dynamic')

    def __unicode__(self):
        return self.title

    @property
    def cover_thumbnail(self):
        path, ext = os.path.splitext(self.cover)
        return '%s_thumbnail%s' % (path, ext)

    @property
    def short_credits(self):
        return [r.actor for r in self.roles.limit(10)]


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column('id', db.Integer, primary_key=True)
    role = db.Column(db.String(255))    # character etc
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'))
    actor = db.relationship("Actor")
    tvseries_id = db.Column(db.Integer, db.ForeignKey('tvseries.id'))
    tvseries = db.relationship("TVSeries")

    def __unicode__(self):
        return self.full_name


class Actor(db.Model):
    __tablename__ = 'actor'

    id = db.Column('id', db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))
    roles = db.relationship("Role")

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


class UserRole(db.Model, RoleMixin):

    __tablename__ = "userroles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    login_count = db.Column(db.Integer)
    roles = db.relationship('UserRole', secondary=roles_users,
            backref=db.backref('users', lazy='dynamic'))
    connections = db.relationship('Connection',
            backref=db.backref('user', lazy='joined'), cascade="all")


class Connection(db.Model):

    __tablename__ = "connections"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    provider_id = db.Column(db.String(255))
    provider_user_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    full_name = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    rank = db.Column(db.Integer)


class TVSeriesFeed(db.Model):

    __tablename__ = "tvseries_feeds"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tvseries_id = db.Column(db.Integer, db.ForeignKey('tvseries.id'))
    tvseries = db.relationship("TVSeries")
    notify_by_email = db.Column(db.Boolean)