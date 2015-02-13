'use strict';

var episodesControllers = angular.module('episodesControllers', []);

episodesControllers.controller('TVSeriesListCtrl', ['$scope', '$routeParams', 'TVSeries',
    function($scope, $routeParams, TVSeries) {
        $scope.hideOriginalList = false;
        var pageId = $routeParams['pageId'];
        $scope.items = TVSeries.query({pageId: pageId});
    }]
);
