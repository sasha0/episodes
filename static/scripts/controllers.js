'use strict';

var episodesControllers = angular.module('episodesControllers', []);

episodesControllers.controller('TVSeriesListCtrl', ['$scope', '$routeParams', 'TVSeriesList',
    function($scope, $routeParams, TVSeriesList) {
        var pageId = $routeParams['pageId'];
        TVSeriesList.query({pageId: pageId}, function(response) {
            $scope.items = response.items;
            $scope.pagination_items = response.pagination_items;
        });
        $scope.current_page = pageId;
    }]
);

episodesControllers.controller('TVSeriesItemCtrl', ['$scope', '$routeParams', 'TVSeriesDetail',
    function($scope, $routeParams, TVSeriesDetail) {
        var tvseriesId = $routeParams['tvseriesId'];
        $scope.item = TVSeriesDetail.get({tvseriesId: tvseriesId});
    }]
);

episodesControllers.controller('TVChannelListCtrl', ['$scope', '$routeParams', 'TVChannelList',
    function($scope, $routeParams, TVChannelList) {
        $scope.items = TVChannelList.query();
    }]
);