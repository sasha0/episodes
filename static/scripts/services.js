'use strict';

var episodesServices = angular.module('episodesServices', ['ngResource']);

episodesServices.factory('TVSeriesList', ['$resource',
  function($resource){
    return $resource('series/:pageId', {pageId: '@id'}, {
      query: {method:'GET', params:{}, isArray: true}
    });
  }]);

episodesServices.factory('TVSeriesDetail', ['$resource',
  function($resource){
    return $resource('series/i/:tvseriesId', {pageId: '@id'}, {
      query: {method:'GET', params:{}, isArray: true}
    });
  }]);