PostModel = Backbone.Tastypie.Model.extend({
    urlRoot: 'api/v1/post/',
    defaults: {
    }
});

PostCollection = Backbone.Tastypie.Collection.extend({
    urlRoot: 'api/v1/post/',
    model: PostModel
})


PostItemView = Backbone.View.extend({
    tagName : 'div',
    templateTest:   '(<%= id %>) <%= title %> ',

    initialize : function(){
        this.template = _.template(this.templateTest);
        this.render();
    },

    render : function(){
        this.$el.html(this.template(this.model.toJSON()));
    }

})

PostView = Backbone.View.extend({
    tagName : 'div',
    templateHtml:   'Posts',

    initialize : function(){
        this.template = _.template(this.templateHtml)
        this.list = new PostCollection()
        var _this = this;
        this.list.bind('reset', function(){ //binder till event
            _this.onReset()
        });
        this.list.fetch()
    },

    onReset: function(){
        this.render();
    },

    render : function(){
        this.$el.append(this.template())
        _.each(this.list.models, function(elem){
            var Postview = new PostItemView({model:elem})
            $('#post-data').append(Postview.$el);
        })
        this.template();
    }

})

var postview = new PostView();
$('#post-data').html(postview.$el);