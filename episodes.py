# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_from_directory
from flask.ext.restful import Api, Resource, fields, marshal_with

app = Flask(__name__)
app.config.from_object('config.Config')
api = Api(app)

resource_fields = {
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

    @marshal_with(resource_fields)
    def get(self, page_id=1):
        from models import TVSeries
        return TVSeries.query.paginate(page_id).items


class TVSeriesDetail(Resource):

    @marshal_with(resource_fields)
    def get(self, tvseries_id=1):
        from models import TVSeries
        return TVSeries.query.get(tvseries_id)


api.add_resource(TVSeriesList, '/series', '/series/<int:page_id>')
api.add_resource(TVSeriesDetail, '/series/i/<int:tvseries_id>')

if __name__ == "__main__":
    app.run()