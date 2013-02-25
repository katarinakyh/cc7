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
        this.template = _.template(this.templateTest); //make a template out of that code
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
        this.$el.html(this.template(this.model.toJSON())); //inserts an object of data, which is available to the template
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

//view for all posts
Posts.View.Posts = Backbone.View.extend({
    tagName :'ul',
        id : 'main',
    initialize : function(){
//        console.log(this.collection);
        this.template = _.template(this.templateHtml);
        this.ready = function(){
            //('#post-data').trigger('create');
            $('a').click(function(e){
                var thediv = $(this).attr('href');
                console.log(thediv);
                $.mobile.changePage($(thediv));
                //console.log($(thediv).html());
            });            
        };

        this.posts = new Posts.Collections.Post();
        var _this = this;
        this.posts.bind('reset', function(){ //binder till event
            _this.onReset();
        });
        this.posts.fetch();
        console.log(this.posts)
    },

    events: {
        //'click': 'console'
    },

    console: function() {
        //alert($(this).attr('href'));
    },

    onReset: function(){
        this.render();
    },
    
    render : function(){
        //filter through all items in a collection
        console.log(this.collection);

        this.collection.each(function(post){
            var postView = new Posts.Views.Post({ model:post });
            this.$el.append(postView.render().el)
        }, this)
/*
         this.$el.attr({"id":"post-data", "data-role":"listview", "data-inset":"true", "data-theme":"c", "data-filter":"true"});
         this.$el.append(this.template());
        
        _.each(this.posts.models, function(post){
            var postView = new Posts.Views.Post({model:post})
            _this.$el.append(postView.$el);

        })
  */
        this.template()
        this.ready();

    }

})

//$('#post-data').html(postview.$el);
//$('#post-data').trigger('create');

})();
