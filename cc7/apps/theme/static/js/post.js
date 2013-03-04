// Namespacing
(function() {

    window.Apps = {
        Models: {},
        Collections: {},
        Views: {},
        Routers: {}
    };

})();

// Models

// the Post model is all the post of the stream
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
        this.comments = new Apps.Collections.CommentCollection([], {post:this});
    },

    addComment : function(text){
        this.comments.create({text: text});
    }

});

// comments per post, not used at this moment
Apps.Models.Comment = Backbone.Tastypie.Model.extend({
    urlRoot: 'api/v1/comment/'
});

// Collections

// the collection of posts of the stream
Apps.Collections.PostCollection = Backbone.Tastypie.Collection.extend({
    model:Apps.Models.Post,
    urlRoot: 'api/v1/post/'
});

// comments collection per post, not used at this moment
Apps.Collections.CommentCollection = Backbone.Tastypie.Collection.extend({
    model:Comment,
    urlRoot: 'api/v1/comment/',
    inititalize : function(models, options){
        this.post = options.post;
    }

});

// Views
// the stream post view wapping postitems
Apps.Views.PostListView = Backbone.View.extend({

    tagName:'ul',

    initialize:function () {
        this.model.bind("reset", this.render, this);
    },

    render:function (eventName) {
        _.each(this.model.models, function (Post) {
            $(this.el).append(new Apps.Views.PostListItemView({model:Post}).render().el);
        }, this);
        return this;
    }
});

// view for individual post items call for each item in the post list
Apps.Views.PostListItemView = Backbone.View.extend({
    tagName:"li",

    template:_.template($('#post_list_template').html()),

    render:function (eventName) {
        $(this.el).html(this.template( this.model.toJSON() ));
        return this;
    }

});

// same as above the stream post view wapping postitems - TODO check - the one in use
Apps.Views.PostView = Backbone.View.extend({

    template:_.template($('#singel_post_template').html()),
    
    initialize : function(){
        this.on('reset', this.getNotes, this);
    },

    events: {
        "click button.newcomment": "postcomment",
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

Apps.Views.NewPostView = Backbone.View.extend({

    template:_.template($('#new_post_template').html()),

    events: {
        "click #add_local": "add_local",
        "click button.post_new": "new_post",

    },

    add_local:function (eventName) {
      console.log("your trying to change your location")
    },

    new_post:function (eventName) {
        console.log("you are trying to post")
    },


    render:function (eventName) {
        $(this.el).html(this.template);
        return this;
    }

});
// Router
// Routers for stream range and detail view
Apps.Routers.PostRouter = Backbone.Router.extend({

    routes:{
        "":"list",
        "postrange/:from-:to":"range",
        "detail_id?:id":"PostDetails",
        "add_post":"AddPost"

    },
    list:function () {
        this.PostList = new Apps.Collections.PostCollection();
        this.PostListView = new Apps.Views.PostListView({model:this.PostList});
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
        // TODO move this validation to the model
        if (limit > 100) {limit = 100};
        if (offset > 100) {offset = 100};
        if (from > to) {limit = 20; offset = 0}

        this.PostList = new Apps.Collections.PostCollection();
        this.PostListView = new Apps.Views.PostListView({model:this.PostList});
        this.PostList.fetch({data:{
            'limit': limit,
            'offset':offset
        }
        });
        $('#post-data').html(this.PostListView.render().el);
    },

    PostDetails:function (id) {
        this.Post = this.PostList.get('/mobile/api/v1/post/'+ id +'/');
        this.PostView = new Apps.Views.PostView({model:this.Post});
        $('#post-data').html(this.PostView.render().el);
    },

    AddPost: function() {
        this.NewPostView = new Apps.Views.NewPostView();
        $('#post-data').html(this.NewPostView.render().el);
    }

});

var app = new Apps.Routers.PostRouter();
Backbone.history.start();
