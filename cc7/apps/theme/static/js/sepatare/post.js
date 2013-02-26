(function() {

    window.Posts = {
        Models: {},
        Collections: {},
        Views: {},
        View:{},
        Router: {}
    };

    var vent = _.extend({}, Backbone.Events);

    window.template = function(id) {
        return _.template( $('#' + id).html() );
    };

})();

var vent = _.extend({}, Backbone.Events);
