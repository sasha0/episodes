# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.restful import Api
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.social import Social, SQLAlchemyConnectionDatastore, login_failed
from flask.ext.social.utils import get_connection_values_from_oauth_response
from flask.ext.social.views import connect_handler
from flask.ext.security.utils import login_user
from flask_sqlalchemy import SQLAlchemy
from pyes import *


app = Flask(__name__)
app.config.from_object('app.config.Config')
api = Api(app)
db = SQLAlchemy(app)
es = ES('127.0.0.1:9200')

import api_views
import views
import models

security_ds = SQLAlchemyUserDatastore(db, models.User, models.UserRole)
social_ds = SQLAlchemyConnectionDatastore(db, models.Connection)

app.security = Security(app, security_ds)
app.social = Social(app, social_ds)


@login_failed.connect_via(app)
def on_login_failed(sender, provider, oauth_response):
    connection_values = get_connection_values_from_oauth_response(provider, oauth_response)
    ds = app.security.datastore
    email = connection_values.pop('email', None)
    user = ds.create_user(email=email)
    ds.commit()
    connection_values['user_id'] = user.id
    connect_handler(connection_values, provider)
    login_user(user)
    db.session.commit()