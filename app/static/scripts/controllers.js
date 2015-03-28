'use strict';

var episodesControllers = angular.module('episodesControllers', []);

episodesControllers.controller('TVSeriesListCtrl', ['$scope', '$rootScope', '$location', '$routeParams', 'TVSeriesList',
                                                    'Subscription',
    function($scope, $rootScope, $location, $routeParams, TVSeriesList, Subscription) {
        $rootScope.hideMainContent = false;
        $rootScope.hideSearchResults = true;
        $rootScope.title = 'Popular TV series';
        var pageId = $routeParams['pageId'];
        TVSeriesList.query({pageId: pageId}, function(response) {
            $scope.items = response.items;
            $scope.pagination_items = response.pagination_items;
            $scope.user_id = response.user_id;
        });
        if (typeof(pageId) !== 'undefined') {
            $scope.current_page = pageId;
        }
        else {
            $scope.current_page = 1;
        }

        $scope.next_page = function(page) {
            $location.path('/p/' + page);
        }

        $scope.subscribe = function(item_id) {
            Subscription.save({'tvseries_id': item_id}, function(response) {
               if (response.success) {
                   $scope.message = 'Successfully subscribed to "' + $scope.items[item_id].title + '" updates.';
               }
               else {
                   $scope.message = 'Already subscribed to "' + $scope.items[item_id].title + '".';
               }
            });
        }

        $scope.hide_message = function() {
            $scope.message = '';
        }
    }]
);

episodesControllers.controller('TVSeriesItemCtrl', ['$scope', '$rootScope', '$routeParams', 'TVSeriesDetail', 'Subscription',
    function($scope, $rootScope, $routeParams, TVSeriesDetail, Subscription) {
        var tvseriesId = $routeParams['tvseriesId'];
        $rootScope.hideMainContent = false;
        $rootScope.hideSearchResults = true;
        TVSeriesDetail.get({tvseriesId: tvseriesId}, function(response) {
            $scope.item = response;
            $scope.user_id = response.user_id;
            $rootScope.title = 'TV series — ' + response.title;
        });
        this.tab = 1;

    this.setTab = function(newValue){
      this.tab = newValue;
    };

    this.isSet = function(tabName){
      return this.tab === tabName;
    };

    $scope.subscribe = function(item_id) {
        Subscription.save({'tvseries_id': item_id}, function(response) {
            if (response.success) {
                $scope.message = 'Successfully subscribed to "' + $scope.item.title + '" updates.';
            }
            else {
                $scope.message = 'Already subscribed to "' + $scope.item.title + '".';
            }
        });
    }

    $scope.hide_message = function() {
        $scope.message = '';
    }

    }]
);

episodesControllers.controller('TVChannelListCtrl', ['$scope', '$rootScope', '$routeParams', 'TVChannelList',
    function($scope, $rootScope, $routeParams, TVChannelList) {
        $rootScope.hideMainContent = false;
        $rootScope.hideSearchResults = true;
        $scope.items = TVChannelList.query();
        $rootScope.title = 'Popular TV channels.'
    }]
);

episodesControllers.controller('TVSeriesForChannelListCtrl', ['$scope', '$rootScope', '$routeParams', 'TVSeriesForChannelList',
    function($scope, $rootScope, $routeParams, TVSeriesForChannelList) {
        $rootScope.hideMainContent = false;
        $rootScope.hideSearchResults = true;
        TVSeriesForChannelList.query({'tvchannelId': $routeParams['tvchannelId']}, function(response) {
            $scope.item = response;
            $rootScope.title = 'TV series of ' + response.title;
        });
    }]
);

episodesControllers.controller('UpcomingEpisodesListCtrl', ['$scope', '$rootScope', '$routeParams', 'UpcomingEpisodesList',
    function($scope, $rootScope, $routeParams, UpcomingEpisodesList) {
        $rootScope.hideMainContent = false;
        $rootScope.hideSearchResults = true;
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
        $rootScope.hideMainContent = false;
        $rootScope.hideSearchResults = true;
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
        $rootScope.hideMainContent = false;
        $rootScope.hideSearchResults = true;
        $scope.items = EpisodesList.query({tvseriesId: tvseriesId});
    }]
);

episodesControllers.controller('SearchTVSeriesCtrl', ['$scope', '$rootScope', '$routeParams', 'SearchTVSeriesList',
    function($scope, $rootScope, $routeParams, SearchTVSeriesList) {
        $rootScope.hideMainContent = false;
        $rootScope.hideSearchResults = true;
        $scope.SearchTVSeries = function() {
            $rootScope.result = SearchTVSeriesList.query({q: $scope.q});
            $rootScope.hideMainContent = true;
            $rootScope.hideSearchResults = false;
        }
    }]
);

episodesControllers.controller('SubscriptionsCtrl', ['$scope', '$rootScope', '$routeParams', 'Subscription',
    function($scope, $rootScope, $routeParams, Subscription) {
        $rootScope.hideMainContent = false;
        $rootScope.hideSearchResults = true;
        $rootScope.title = 'My Episodes';
        var pageId = $routeParams['pageId'];
        Subscription.query({pageId: pageId}, function(response) {
           $scope.items = response.items;

        });
    }]
);