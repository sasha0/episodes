# -*- coding: utf-8 -*-
import datetime
from flask.ext.restful import fields


class Date(fields.Raw):

    def format(self, value):
        return datetime.datetime.strftime(value, '%d.%m.%Y')

role_resource_fields = {
    'role': fields.String,
    'actor': fields.String
}

tvseries_resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'rating': fields.String,
    'short_description': fields.String,
    'description': fields.String,
    'genres': fields.List(fields.String),
    'actors': fields.List(fields.String),
    'cover_thumbnail': fields.String,
    'tvchannel': fields.String,
    'short_credits': fields.List(fields.String)
}

tvchannel_resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'logo': fields.String,
    'logo_thumbnail': fields.String,
    'popular_tvseries': fields.Nested(tvseries_resource_fields)
}

upcoming_episode_resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'episode_number': fields.Integer,
    'season_number': fields.Integer,
    'showed_at': Date,
    'tvseries': fields.Nested(tvseries_resource_fields)
}

episode_resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'episode_number': fields.Integer,
    'season_number': fields.Integer,
}