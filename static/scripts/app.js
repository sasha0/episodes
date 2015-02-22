'use strict';

var episodesApp = angular.module('episodesApp', ['ngRoute', 'episodesControllers', 'episodesServices']);

episodesApp.config(
  function($routeProvider, $locationProvider) {
    $routeProvider.
      when('/p/:pageId', {
            templateUrl: '/partials/tvseries.html',
            controller: 'TVSeriesListCtrl'
      })
      .when('/e/:tvseriesId', {
            templateUrl: '/partials/tvseries_item.html',
            controller: 'TVSeriesItemCtrl'
      })
      .when('/c/', {
            templateUrl: '/partials/tvchannels.html',
            controller: 'TVChannelListCtrl'
      }).otherwise({
        redirectTo: '/p/1'
      });
  });