'use strict';

var episodesServices = angular.module('episodesServices', ['ngResource']);

episodesServices.factory('TVSeriesList', ['$resource',
  function($resource){
    return $resource('series/:pageId', {pageId: '@id'}, {
      query: {method:'GET', isArray:false}
    });
  }]);

episodesServices.factory('TVSeriesDetail', ['$resource',
  function($resource){
    return $resource('series/i/:tvseriesId', {pageId: '@id'}, {
      query: {method:'GET', isArray: true}
    });
  }]);

episodesServices.factory('TVChannelList', ['$resource',
  function($resource){
    return $resource('channels/', {}, {
      query: {method:'GET', isArray: true}
    });
  }]);

episodesServices.factory('TVSeriesForChannelList', ['$resource',
  function($resource){
    return $resource('channels/:tvchannelId/tvseries', {}, {
      query: {method:'GET', isArray: false}
    });
  }]);

episodesServices.factory('UpcomingEpisodesList', ['$resource',
  function($resource){
    return $resource('episodes/upcoming/:pageId', {pageId: '@id'}, {
      query: {method:'GET', isArray:false}
    });
  }]);

episodesServices.factory('EpisodesList', ['$resource',
  function($resource){
    return $resource('series/i/:tvseriesId/episodes', {pageId: '@id'}, {
      query: {method:'GET', isArray: true}
    });
  }]);

episodesServices.factory('SearchTVSeriesList', ['$resource',
  function($resource){
    return $resource('series/search/', {}, {
      query: {method:'GET', isArray: true, params: {'q': '@q'}}
    });
  }]);

episodesServices.factory('Subscription', ['$resource',
  function($resource){
    return $resource('subscriptions/:pageId', {}, {
      save: {method:'POST'},
      query: {method: 'GET', isArray: false, pageId: '@id'}
    });
  }]);