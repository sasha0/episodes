# -*- coding: utf-8 -*-
from flask import Flask
from flask.ext.restful import Api
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
