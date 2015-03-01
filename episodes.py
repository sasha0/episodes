# -*- coding: utf-8 -*-
import datetime
from flask import Flask, render_template, send_from_directory
from flask.ext.restful import Api, Resource, fields, marshal_with, marshal

app = Flask(__name__)
app.config.from_object('config.Config')
api = Api(app)

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

@app.route('/')
@app.route('/p/<int:page_id>')
def main(page_id=1):
    from models import TVSeries
    pagination = TVSeries.query.paginate(page_id)
    return render_template('index.html', pagination=pagination)


@app.route('/partials/<template_name>')
def output_partial(template_name):
    return send_from_directory('templates/partials', template_name)


class TVSeriesList(Resource):

    def get(self, page_id=1):
        from models import TVSeries
        pagination = TVSeries.query.paginate(page_id)
        data = dict(marshal(pagination.items, tvseries_resource_fields, envelope='items'))
        data['pagination_items'] = list(pagination.iter_pages())
        return data


class TVSeriesDetail(Resource):

    def get(self, tvseries_id):
        from models import TVSeries
        tvseries = TVSeries.query.get(tvseries_id)
        data = dict(marshal(tvseries, tvseries_resource_fields))
        data['roles'] = marshal(tvseries.roles.all(), role_resource_fields)
        return data


class TVChannelsList(Resource):

    @marshal_with(tvchannel_resource_fields)
    def get(self):
        from models import TVChannel
        return TVChannel.query.all()


class TVSeriesForChannelList(Resource):

    def get(self, tvchannel_id):
        from models import TVSeries, TVChannel
        tvchannel = TVChannel.query.get(tvchannel_id)
        tvseries_for_channel_resource_fields = tvchannel_resource_fields
        tvseries_for_channel_resource_fields.pop('popular_tvseries', None)
        tvseries = list(tvchannel.tvseries.all())
        data = dict(marshal(tvchannel, tvseries_for_channel_resource_fields))
        data['tvseries'] = marshal(tvseries, tvseries_resource_fields)
        return data


class UpcomingEpisodesList(Resource):

    def get(self, page_id=1):
        from models import Episode, db
        pagination = Episode.query.filter(Episode.showed_at >= datetime.date.today())\
                                  .order_by(db.desc(Episode.showed_at))\
                                  .paginate(page_id)
        data = dict(marshal(pagination.items, upcoming_episode_resource_fields, envelope='items'))
        data['pagination_items'] = list(pagination.iter_pages())
        return data


class EpisodesList(Resource):

    @marshal_with(episode_resource_fields)
    def get(self, tvseries_id):
        from models import Episode, db
        return list(Episode.query.filter(Episode.tvseries_id == tvseries_id)\
                                 .order_by(Episode.season_number, Episode.episode_number, ))


api.add_resource(TVSeriesList, '/series', '/series/<int:page_id>')
api.add_resource(TVSeriesDetail, '/series/i/<int:tvseries_id>')
api.add_resource(TVChannelsList, '/channels/')
api.add_resource(TVSeriesForChannelList, '/channels/<int:tvchannel_id>/tvseries')
api.add_resource(EpisodesList, '/series/i/<int:tvseries_id>/episodes')
api.add_resource(UpcomingEpisodesList, '/episodes/upcoming/', '/episodes/upcoming/<int:page_id>')

if __name__ == "__main__":
    app.run()