# -*- coding: utf-8 -*-
import json
from flask import Flask, render_template, send_from_directory
from flask.ext.restful import Api, Resource, fields, marshal_with, marshal

app = Flask(__name__)
app.config.from_object('config.Config')
api = Api(app)

class NestedItem(fields.Raw):
    def format(self, value):
        print value
        print [{'id': s.id, 'title': s.title} for s in value.tvseries]
        print 123

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
}

tvchannel_resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'logo': fields.String,
    'logo_thumbnail': fields.String,
    'popular_tvseries': fields.Nested(tvseries_resource_fields)
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

    @marshal_with(tvseries_resource_fields)
    def get(self, tvseries_id):
        from models import TVSeries
        return TVSeries.query.get(tvseries_id)


class TVChannelsList(Resource):

    @marshal_with(tvchannel_resource_fields)
    def get(self):
        from models import TVChannel
        return TVChannel.query.all()


api.add_resource(TVSeriesList, '/series', '/series/<int:page_id>')
api.add_resource(TVSeriesDetail, '/series/i/<int:tvseries_id>')
api.add_resource(TVChannelsList, '/channels/')

if __name__ == "__main__":
    app.run()