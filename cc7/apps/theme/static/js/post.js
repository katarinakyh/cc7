
// Models
window.Post = Backbone.Tastypie.Model.extend({
    initialize: function(){
        this.comments = new CommentCollection([], {post:this});
    },
    addComment : function(text){
        this.comments.create({text: text});
    }    
});
window.Comment = Backbone.Tastypie.Model.extend({});

//Collections
window.PostCollection = Backbone.Tastypie.Collection.extend({
    model:Post,
    urlRoot: 'api/v1/comment/'
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
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }

});


window.PostView = Backbone.View.extend({

    template:_.template($('#singel_post_template').html()),
    
    initialize : function(){
        this.on('reset', this.getNotes, this)
        console.log('initializing');
        console.log(this.model);
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
        //console.log(this.model.toJSON());
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }

});

// Router
var AppRouter = Backbone.Router.extend({

    routes:{
        '':'list',
        'detail_id?:id':'PostDetails'
    },
    list:function () {
        this.PostList = new window.PostCollection();
        this.PostListView = new window.PostListView({model:this.PostList});
        this.PostList.fetch(/*{
            success: function(coll, resp) {
              console.log(coll);
              console.log((coll.first()).id);
              console.log(coll.last());
            }
        }*/);  
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


