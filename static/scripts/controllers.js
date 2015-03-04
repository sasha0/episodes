'use strict';

var episodesControllers = angular.module('episodesControllers', []);

episodesControllers.controller('TVSeriesListCtrl', ['$scope', '$rootScope', '$location', '$routeParams', 'TVSeriesList',
    function($scope, $rootScope, $location, $routeParams, TVSeriesList) {
        $rootScope.title = 'Popular TV series';
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

        $scope.next_page = function (page) {
            $location.path('/p/' + page);
        }
    }]
);

episodesControllers.controller('TVSeriesItemCtrl', ['$scope', '$rootScope', '$routeParams', 'TVSeriesDetail',
    function($scope, $rootScope, $routeParams, TVSeriesDetail) {
        var tvseriesId = $routeParams['tvseriesId'];
        TVSeriesDetail.get({tvseriesId: tvseriesId}, function(response) {
            $scope.item = response;
            $rootScope.title = 'TV series — ' + response.title;
        });
    }]
);

episodesControllers.controller('TVChannelListCtrl', ['$scope', '$rootScope', '$routeParams', 'TVChannelList',
    function($scope, $rootScope, $routeParams, TVChannelList) {
        $scope.items = TVChannelList.query();
        $rootScope.title = 'Popular TV channels.'
    }]
);

episodesControllers.controller('TVSeriesForChannelListCtrl', ['$scope', '$rootScope', '$routeParams', 'TVSeriesForChannelList',
    function($scope, $rootScope, $routeParams, TVSeriesForChannelList) {
        TVSeriesForChannelList.query({'tvchannelId': $routeParams['tvchannelId']}, function(response) {
            $scope.item = response;
            $rootScope.title = 'TV series of ' + response.title;
        });
    }]
);

episodesControllers.controller('UpcomingEpisodesListCtrl', ['$scope', '$rootScope', '$routeParams', 'UpcomingEpisodesList',
    function($scope, $rootScope, $routeParams, UpcomingEpisodesList) {
        $rootScope.title = 'Upcoming episodes';
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

episodesControllers.controller('EpisodesListCtrl', ['$scope', '$rootScope', '$routeParams', 'EpisodesList',
    function($scope, $rootScope, $routeParams, EpisodesList) {
        var pageId = $routeParams['pageId'];
        UpcomingEpisodesList.query({pageId: pageId}, function(response) {
            $scope.items = response.items;
            $scope.pagination_items = response.pagination_items;
            $rootScope.title = 'Episodes list for ' + response.title;
        });
        if (typeof(pageId) !== 'undefined') {
            $scope.current_page = pageId;
        }
        else {
            $scope.current_page = 1;
        }
    }]
);

episodesControllers.controller('EpisodesListCtrl', ['$scope', '$rootScope', '$routeParams', 'EpisodesList',
    function($scope, $rootScope, $routeParams, EpisodesList) {
        var tvseriesId = $routeParams['tvseriesId'];
        $scope.items = EpisodesList.query({tvseriesId: tvseriesId});
    }]
);