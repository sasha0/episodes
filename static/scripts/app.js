'use strict';

var episodesApp = angular.module('episodesApp', ['ngRoute', 'episodesControllers', 'episodesServices']);

episodesApp.config(
  function($routeProvider, $locationProvider) {
    $routeProvider.
      when('/p/:pageId', {
            templateUrl: '/partials/tvseries.html',
            controller: 'TVSeriesListCtrl'
      }).otherwise({
        redirectTo: '/p/1'
      });;
  });