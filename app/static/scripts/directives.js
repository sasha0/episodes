'use strict';

var episodesDirectives = angular.module('episodesDirectives', []);

episodesDirectives.directive('tabswitcher', function() {
    return {
        link: function(scope, element, attrs) {
            element.tab();
        }
    };
});