
// Models
window.Post = Backbone.Tastypie.Model.extend({
    urlRoot: 'api/v1/post/',
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
window.Comment = Backbone.Tastypie.Model.extend({
    urlRoot: 'api/v1/comment/'
});

// Collection
window.PostCollection = Backbone.Tastypie.Collection.extend({
    model:Post,
    urlRoot: 'api/v1/post/'
});

window.CommentCollection = Backbone.Tastypie.Collection.extend({
    model:Comment,
    urlRoot: 'api/v1/comment/',
    inititalize : function(models, options){
        this.post = options.post;
    }

});

// Views
window.PostListView = Backbone.View.extend({

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

window.PostListItemView = Backbone.View.extend({
    tagName:"li",

    template:_.template($('#post_list_template').html()),

    render:function (eventName) {
        $(this.el).html(this.template( this.model.toJSON() ));
        return this;
    }

});


window.PostView = Backbone.View.extend({

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
        var comment = new window.Comment();
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
var AppRouter = Backbone.Router.extend({

    routes:{
        "":"list",
        "postrange/:from-:to":"range",
        "detail_id?:id":"PostDetails"
    },
    list:function () {
        this.PostList = new window.PostCollection();
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

var app = new AppRouter();
Backbone.history.start();
