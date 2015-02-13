'use strict';

var episodesServices = angular.module('episodesServices', ['ngResource']);

episodesServices.factory('TVSeries', ['$resource',
  function($resource){
    return $resource('series/:pageId', {pageId: '@id'}, {
      query: {method:'GET', params:{}, isArray: true}
    });
  }]);