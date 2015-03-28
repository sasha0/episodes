# -*- coding: utf-8 -*-
"""REST API controllers, powered by flask-restful."""

from flask.ext.restful import Api, Resource, fields, marshal_with, marshal
from flask.ext.restful import reqparse
from flask.ext.security import current_user

from app import api, es, QueryStringQuery, MultiMatchQuery, TermQuery
from app.resource_fields import *
from models import db, Episode, TVChannel, TVSeries, TVSeriesFeed


parser = reqparse.RequestParser()


class TVSeriesList(Resource):
    """Paginated list of available TV shows, including indication if current user subscribed to given TV shows."""

    def get(self, page_id=1):
        pagination = TVSeries.query.paginate(page_id)
        user_id = getattr(current_user, 'id', None)
        data = dict(marshal(pagination.items, tvseries_resource_fields, envelope='items'))
        data['pagination_items'] = list(pagination.iter_pages())
        data['user_id'] = user_id
        if user_id:
            feed = TVSeriesFeed.query.filter(TVSeriesFeed.user_id == user_id)
            for tvseries in data['items']:
                if tvseries['id'] in [f.tvseries_id for f in feed]:
                    tvseries['is_subscribed'] = True
                else:
                    tvseries['is_subscribed'] = False
        return data


class TVSeriesDetail(Resource):
    """Page with detailed information about single TV show."""

    def get(self, tvseries_id):
        tvseries = TVSeries.query.get(tvseries_id)
        user_id = getattr(current_user, 'id', None)
        data = dict(marshal(tvseries, tvseries_resource_fields))
        data['roles'] = marshal(tvseries.roles.all(), role_resource_fields)
        data['episodes'] = marshal(tvseries.episodes, episode_resource_fields)
        data['user_id'] = user_id
        if user_id:
            feed = TVSeriesFeed.query.filter(TVSeriesFeed.user_id == user_id)
            if data['id'] in [f.tvseries_id for f in feed]:
                data['is_subscribed'] = True
            else:
                data['is_subscribed'] = False
        return data


class TVChannelsList(Resource):
    """List of available TV channels."""

    @marshal_with(tvchannel_resource_fields)
    def get(self):
        return TVChannel.query.all()


class TVSeriesForChannelList(Resource):
    """List of TV series, produced by given TV channel."""

    def get(self, tvchannel_id):
        tvchannel = TVChannel.query.get(tvchannel_id)
        tvseries_for_channel_resource_fields = tvchannel_resource_fields
        tvseries_for_channel_resource_fields.pop('popular_tvseries', None)
        tvseries = list(tvchannel.tvseries.all())
        data = dict(marshal(tvchannel, tvseries_for_channel_resource_fields))
        data['tvseries'] = marshal(tvseries, tvseries_resource_fields)
        return data


class UpcomingEpisodesList(Resource):
    """List of episodes, to be aired in the nearest future."""

    def get(self, page_id=1):
        pagination = Episode.query.filter(Episode.showed_at >= datetime.date.today())\
                                  .order_by(db.desc(Episode.showed_at))\
                                  .paginate(page_id)
        data = dict(marshal(pagination.items, upcoming_episode_resource_fields, envelope='items'))
        data['pagination_items'] = list(pagination.iter_pages())
        return data


class EpisodesList(Resource):
    """List of all available episodes for the given TV show."""

    @marshal_with(episode_resource_fields)
    def get(self, tvseries_id):
        return list(Episode.query.filter(Episode.tvseries_id == tvseries_id)\
                                 .order_by(Episode.season_number, Episode.episode_number, ))


class TVSeriesSearch(Resource):
    """Full-text search of TV series, powered by Elasticsearch."""

    @marshal_with(tvseries_resource_fields)
    def get(self):
        parser.add_argument('q', type=str)
        params = parser.parse_args()
        q = MultiMatchQuery(['title', 'description'], params['q'])
        r = es.search(query=q)
        return list(r)


class Subscriptions(Resource):
    """List of TV shows, user subscribed to. Ability to subscribe to given TV show to get updates."""

    def post(self):
        success = False
        parser.add_argument('tvseries_id', type=int)
        params = parser.parse_args()
        if TVSeriesFeed.query.filter(TVSeriesFeed.user_id == current_user.id,
                                     TVSeriesFeed.tvseries_id == params['tvseries_id']).count() == 0:
            feed = TVSeriesFeed(user_id=current_user.id, tvseries_id=params['tvseries_id'])
            db.session.add(feed)
            db.session.commit()
            success = True
        return {'success': success}

    def get(self, page_id=1):
        user_id = getattr(current_user, 'id', None)
        if user_id:
            feed = TVSeriesFeed.query.filter(TVSeriesFeed.user_id == user_id)
            tvseries_ids = [f.tvseries_id for f in feed]
            pagination = Episode.query.filter(Episode.showed_at >= datetime.date.today(),
                                              Episode.tvseries_id.in_(tvseries_ids))\
                                      .order_by(db.desc(Episode.showed_at))\
                                      .paginate(page_id)
            data = dict(marshal(pagination.items, upcoming_episode_resource_fields, envelope='items'))
            data['pagination_items'] = list(pagination.iter_pages())
            return data
        return {}

api.add_resource(TVSeriesList, '/series', '/series/<int:page_id>')
api.add_resource(TVSeriesDetail, '/series/i/<int:tvseries_id>')
api.add_resource(TVChannelsList, '/channels/')
api.add_resource(TVSeriesForChannelList, '/channels/<int:tvchannel_id>/tvseries')
api.add_resource(EpisodesList, '/series/i/<int:tvseries_id>/episodes')
api.add_resource(UpcomingEpisodesList, '/episodes/upcoming/', '/episodes/upcoming/<int:page_id>')
api.add_resource(TVSeriesSearch, '/series/search')
api.add_resource(Subscriptions, '/subscriptions', '/subscriptions/<int:page_id>')