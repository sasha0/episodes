'use strict';

var episodesControllers = angular.module('episodesControllers', []);

episodesControllers.controller('TVSeriesListCtrl', ['$scope', '$rootScope', '$routeParams', 'TVSeriesList',
    function($scope, $rootScope, $routeParams, TVSeriesList) {
        $scope.hideOriginalList = false;
        var pageId = $routeParams['pageId'];
        $scope.items = TVSeriesList.query({pageId: pageId});
        $rootScope.hide_pagination = false;
    }]
);

episodesControllers.controller('TVSeriesItemCtrl', ['$scope', '$rootScope', '$routeParams', 'TVSeriesDetail',
    function($scope, $rootScope, $routeParams, TVSeriesDetail) {
        var tvseriesId = $routeParams['tvseriesId'];
        $scope.item = TVSeriesDetail.get({tvseriesId: tvseriesId});
        $rootScope.hide_pagination = true;
    }]
);