(function() {

    window.Posts = {
        Models: {},
        Collections: {},
        Views: {},
        View: {}

    };

    window.template = function(id) {
        return _.template( $('#' + id).html() );
    };


Posts.Models.Post = Backbone.Tastypie.Model.extend({
    urlRoot: 'api/v1/post/',
    defaults: {
        title: '>>'
    }
});

Posts.Collections.Post = Backbone.Tastypie.Collection.extend({
    urlRoot: 'api/v1/post/',
    model: Posts.Models.Post
})

Posts.Views.Post = Backbone.View.extend({
    tagName : 'li',
    templateTest: $('#post_template').html(),

    initialize : function(){
        this.template = _.template(this.templateTest);
        this.render();
    },


    render : function(){
        body = this.model.toJSON().body;
        var fullText = this.model.get('body');
        var shortText = fullText;
        if (fullText.length > 100) {
            shortText = jQuery.trim(fullText).substring(0, 100)
            .split(" ").slice(0, -1).join(" ") + "...";
        }

        this.model.set('trunc_text', shortText );
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },
    
    events: {
        'click .postbody_trunctext': 'fulltext'
    },

    fulltext : function(e){
        $(e.target).html(this.model.get('body'));
        console.log(e.target);
    }
})

Posts.View.Posts = Backbone.View.extend({
    el : '#post-data',
    templateHtml: '',

    initialize : function(){
        this.template = _.template(this.templateHtml);
        this.posts = new Posts.Collections.Post();
        var _this = this;
        this.posts.bind('reset', function(){ //binder till event
            _this.onReset();
        });
        this.posts.fetch();
    },

    events: {
        'click': 'console'
    },

    console: function() {
        console.log("click");
    },

    onReset: function(){
        this.render();
    },
    
    render : function(){
         this.$el.append(this.template());
        _.each(this.posts.models, function(post){
            var postView = new Posts.Views.Post({model:post})
            $('#post-data').append(postView.$el);

        })
        this.template();

    }

})


var postview = new Posts.View.Posts({model:Posts.Models.Post});

//$('#post-data').html(postview.$el);
//$('#post-data').trigger('create');

})();
