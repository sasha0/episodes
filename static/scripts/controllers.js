'use strict';

var episodesControllers = angular.module('episodesControllers', []);

episodesControllers.controller('TVSeriesListCtrl', ['$scope', '$routeParams', 'TVSeriesList',
    function($scope, $routeParams, TVSeriesList) {
        var pageId = $routeParams['pageId'];
        TVSeriesList.query({pageId: pageId}, function(response) {
            $scope.items = response.items;
            $scope.pagination_items = response.pagination_items;
        });
        if (typeof(pageId) !== 'undefined') {
            $scope.current_page = pageId;
        }
        else {
            $scope.current_page = 1;
        }
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

episodesControllers.controller('UpcomingEpisodesListCtrl', ['$scope', '$routeParams', 'UpcomingEpisodesList',
    function($scope, $routeParams, UpcomingEpisodesList) {
        var pageId = $routeParams['pageId'];
        UpcomingEpisodesList.query({pageId: pageId}, function(response) {
            $scope.items = response.items;
            $scope.pagination_items = response.pagination_items;
        });
        if (typeof(pageId) !== 'undefined') {
            $scope.current_page = pageId;
        }
        else {
            $scope.current_page = 1;
        }
    }]
);

episodesControllers.controller('EpisodesListCtrl', ['$scope', '$routeParams', 'EpisodesList',
    function($scope, $routeParams, EpisodesList) {
        var pageId = $routeParams['pageId'];
        UpcomingEpisodesList.query({pageId: pageId}, function(response) {
            $scope.items = response.items;
            $scope.pagination_items = response.pagination_items;
        });
        if (typeof(pageId) !== 'undefined') {
            $scope.current_page = pageId;
        }
        else {
            $scope.current_page = 1;
        }
    }]
);

episodesControllers.controller('EpisodesListCtrl', ['$scope', '$routeParams', 'EpisodesList',
    function($scope, $routeParams, EpisodesList) {
        var tvseriesId = $routeParams['tvseriesId'];
        $scope.items = EpisodesList.query({tvseriesId: tvseriesId});
    }]
);