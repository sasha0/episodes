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
      .when('/e/:tvseriesId/e', {
            templateUrl: '/partials/episodes.html',
            controller: 'EpisodesListCtrl'
      })
      .when('/c/', {
            templateUrl: '/partials/tvchannels.html',
            controller: 'TVChannelListCtrl'
      })
      .when('/c/:tvchannelId/tvseries', {
            templateUrl: '/partials/tvseries_for_channel.html',
            controller: 'TVSeriesForChannelListCtrl'
      })
      .when('/u/', {
            templateUrl: '/partials/upcoming_episodes.html',
            controller: 'UpcomingEpisodesListCtrl'
      })
      .when('/u/:pageId', {
            templateUrl: '/partials/upcoming_episodes.html',
            controller: 'UpcomingEpisodesListCtrl'
      })
      .otherwise({
        redirectTo: '/p/1'
      });
  });