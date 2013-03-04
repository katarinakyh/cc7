// Namespaceing
(function() {

    window.Apps = {
        Models: {},
        Collections: {},
        Views: {},
        Routers: {}
    };

})();


// Models
// change  window.Post to Apps.Models.Post - 1
Apps.Models.Post  = Backbone.Tastypie.Model.extend({
    urlRoot: 'api/v1/post/',

    // TODO validate the data for each model
    validate: function (attrs) {
        if (attrs.id < 0) {
            return "id cannot be less then 0"
        }
        if (attrs.id === "") {
            return "id cannot be blank"
        }

    },

    initialize: function(){
        this.comments = new CommentCollection([], {post:this});
    },

    addComment : function(text){
        this.comments.create({text: text});
    }

});

// change  window.Comment to Apps.Models.Comment - 2
Apps.Models.Comment = Backbone.Tastypie.Model.extend({
    urlRoot: 'api/v1/comment/'
});

// Collections
// change  window.PostCollection to Apps.Collections.PostCollection - 2
Apps.Collections.PostCollection = Backbone.Tastypie.Collection.extend({
    model:Post,
    urlRoot: 'api/v1/post/'
});

// change  window.CommentCollection to Apps.Collections.CommentCollection - 1
Apps.Collections.CommentCollection = Backbone.Tastypie.Collection.extend({
    model:Comment,
    urlRoot: 'api/v1/comment/',
    inititalize : function(models, options){
        this.post = options.post;
    }

});

// Views
// change  window.PostListView to Apps.Views.PostListView - 1
Apps.Views.PostListView = Backbone.View.extend({

    tagName:'ul',

    initialize:function () {
        this.model.bind("reset", this.render, this);
    },

    render:function (eventName) {
        _.each(this.model.models, function (Post) {
            $(this.el).append(new PostListItemView({model:Post}).render().el);
        }, this);
        return this;
    }
});

// change  window.PostListItemView to Apps.Views.PostListItemView - 1
Apps.Views.PostListItemView = Backbone.View.extend({
    tagName:"li",

    template:_.template($('#post_list_template').html()),

    render:function (eventName) {
        $(this.el).html(this.template( this.model.toJSON() ));
        return this;
    }

});

// change  window.PostView to Apps.Views.PostView - 1
Apps.Views.PostView = Backbone.View.extend({

    template:_.template($('#singel_post_template').html()),
    
    initialize : function(){
        this.on('reset', this.getNotes, this);
    },

    events: {
        "click button.newcomment": "postcomment"
    },

    postcomment: function(){
        console.log(this.model.toJSON());
        var comment_body = $('#commentbody').val();
        var post_uri = '/mobile/api/v1/post/'+ this.model.get('id') +'/';
        var event_id = null
        // this is not the right id fixing later
        var author = this.model.get('author')
        var author_id = author.id;
        var author_uri = '/mobile/api/v1/author/'+ author_id +'/';
        var comment = new Apps.Models.Comment();
        // we save this right to the server
        comment.save({author:author_uri, body:comment_body, post:post_uri, event: event_id});
        this.render();

    },


    getNotes : function(){
        for(var i = 0; i < this.comments.length; i++){
            console.log(this.comments[i].body)
        }
        /*this.each(function(post){
            post.comments = new CommentCollection([], { post:post });
            post.comments.fetch();
        })*/
    },
    
    render:function (model) {
        $(this.el).html(this.template( this.model.toJSON() ));
        return this;
    }

});

// Router
// change var AppRouter  to Apps.Routers.PostRouter - 1
Apps.Routers.PostRouter = Backbone.Router.extend({

    routes:{
        "":"list",
        "postrange/:from-:to":"range",
        "detail_id?:id":"PostDetails"
    },
    list:function () {
        this.PostList = new Apps.Collections.PostCollection();
        this.PostListView = new window.PostListView({model:this.PostList});
        this.PostList.fetch({
                data:{ 'limit':10 }
            //success: function(coll, resp) {
            //    console.log(coll);
            //    console.log((coll.first()).id);
            //     console.log(coll.last());
        });
        $('#post-data').html(this.PostListView.render().el);
    },

    range:function (from, to) {
        var offset = from-1;
        var limit = (to - from)+1;
        if (limit > 100) {limit = 100};
        if (offset > 100) {offset = 100};
        if (from > to) {limit = 20; offset = 0}
        this.PostList = new PostCollection();
        //console.log(this.PostList);
        this.PostListView = new PostListView({model:this.PostList});
        this.PostList.fetch({data:{
            'limit': limit,
            'offset':offset
        }
        });
        $('#post-data').html(this.PostListView.render().el);
    },

    PostDetails:function (id) {
        this.Post = this.PostList.get('/mobile/api/v1/post/'+ id +'/');
        this.PostView = new PostView({model:this.Post});
        $('#post-data').html(this.PostView.render().el);
    }

});

var app = new Apps.Routers.PostRouter();
Backbone.history.start();
