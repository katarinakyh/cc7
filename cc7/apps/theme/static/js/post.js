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
    tagName : 'li',
    templateTest: $('#post_template').html(),

    initialize : function(){
        this.template = _.template(this.templateTest);
        this.render();
    },

    render : function(){
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },
    
    events: {
        click : 'console',
    },

    console : function(){
        console.log('click');
    }
})

PostView = Backbone.View.extend({
    el : '#post-data',
    templateHtml: '',

    initialize : function(){
        this.template = _.template(this.templateHtml);
        this.list = new PostCollection();
        var _this = this;
        this.list.bind('reset', function(){ //binder till event
            _this.onReset();
        });
        this.list.fetch();
    },

    onReset: function(){
        this.render();
    },
    
    render : function(){
        this.$el.append(this.template());
        var _this = this;
        _.each(this.list.models, function(elem){
            var Postview = new PostItemView({model:elem})
            _this.$el.append(Postview.$el);
        })
        this.template();
        return this;
    }

})


var postview = new PostView({model:PostModel});
//$('#post-data').html(postview.$el);
//$('#post-data').trigger('create');

