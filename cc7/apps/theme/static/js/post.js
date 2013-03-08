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
    },

    addComment : function(text){
        this.comments.create({text: text});
    }

});
// keep track for pages
Apps.Models.Pages = Backbone.Model.extend({
    defaults:
        {
            'limit' : 10,
            'offset' : 0,
            'item_count' : 10,
            'update_num' : 1,
            'next':'',
            'previous':''
        }
});

Apps.Models.Place = Backbone.Tastypie.Model.extend({
    urlRoot: 'api/v1/place/'
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

Apps.Collections.AllLoadedPosts = Backbone.Collection.extend({
    model:Apps.Models.Post
});

// Views
//a collection of all loaded posts
Apps.Views.AllLoadedPosts = Backbone.View.extend({
})

// the stream post view wapping postitems
Apps.Views.PostListView = Backbone.View.extend({

    tagName:'ul',

    initialize:function () {
        this.model.bind("reset", this.render, this);
        _.bindAll(this, "render");
        this.render();
    },

    events : {
        'click .more_post': 'more_posts'
    },
    more_posts:function () {
        this.PostList = new Apps.Collections.PostCollection();
        this.PostListView = new Apps.Views.PostListView({model : this.PostList});
        this.PostList.fetch({
            url: Apps.meta.next,
            success: function(coll){
                Apps.meta = coll.meta;
                i = 1; //allow scrolling again, code is in maps.js
            }
        });
        Apps.allLoadedPosts.fetch({
            url: Apps.meta.next,
            add:true
        }); //TODO is a double fetch necessary???
        $('#post-data').append(this.PostListView.render().el);

        //more_posts();
    },

    render:function (eventName) {
        _.each(this.model.models, function (Post) {
            $(this.el).append(new Apps.Views.PostListItemView({model:Post}).render().el);
        }, this);
        //this.infiniScroll = new Backbone.InfiniScroll(this.collection, {success: this.appendRender});
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

// same as above the stream post view wrappning single post-view
Apps.Views.PostView = Backbone.View.extend({

    template:_.template($('#single_post_template').html()),
    
    initialize : function(){
        //this.on('reset', this.getNotes, this);
    },

    events: {
        "click button.newcomment": "postcomment"
    },

    postcomment: function(){
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
        "click #new_post": "new_post",
        'click .add_from_camera' : 'togglefield',
        'click .add_from_file' : 'togglefield'
    },

    togglefield : function(e){
        if($(e.target).hasClass('add_from_camera')){
            if($('.get_from_file').css('display') == 'block'){    
                $('.get_from_file').hide();
            }
            $('.get_from_camera').show();        
        }else{
            if($('.get_from_camera').css('display') == 'block'){
                $('.get_from_camera').hide();
            }
            $('.get_from_file').show();
        };
    },
    add_local:function (eventName) {
      console.log("your trying to change your location")
    },

    new_post:function (e) {
        console.log(e.target);
        // post data
        var post_body = $('#new_post_body').val(),
            post_event_id = null;

        if($('#latitude').val() != ''){
            // place data
            var place_title = $('#place_name').val(),
                place_address = $('#adress').val(),
                place_latitude = $('#latitude').val(),
                place_longitude = $('#longitude').val();
            
            alert(place_latitude);

            var place = new Apps.Models.Place();
            place.save({title:place_title, latitude:place_latitude,  longitude: place_longitude, address:place_address},
                {success: function(data){
                    console.log(data)
                    post.save({author: '/mobile/api/v1/author/1/', body: post_body, event: null, title:null, place: data.id, is_public: true})
                },error: function(data){
                    console.log(data);
                }
            });    
        }
        var post = new Apps.Models.Post();
        // we save this right to the server
        
        post.save({author: '/mobile/api/v1/author/1/', body: post_body, event: null, title:null, place: null, is_public: true},
                    {success: function(data){
                        console.log('success');
                        console.log(data);
                    },error: function(data){
                        console.log('error');
                        console.log(data);
                    }
                });
        
        this.render();
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
        "" : "list",
        "postrange/:from-:to" : "range",
        "detail_id?:id" : "PostDetails",
        "add_post" : "AddPost"

    },
    initialize:function () {
        this.PageModel = new Apps.Models.Pages();
    },

    list:function () {
        this.PostList = new Apps.Collections.PostCollection();
        //Apps.allLoadedPosts = new Apps.Collections.PostCollection();
        this.PostListView = new Apps.Views.PostListView({model:this.PostList});

        this.PostList.fetch({
                success : function(coll){
                    Apps.meta = coll.meta;
                    console.log(Apps.meta.next);
                }
        });
        $('#post-data').html(this.PostListView.render().el);
        Apps.allLoadedPosts = this.PostList;
    },

    range:function (from, to) {
        var offset = from-1;
        var limit = (to - from)+1;
        // TODO move this validation to the model
        if (limit > 100) {limit = 100};
        if (offset > 100) {offset = 100};
        if (from > to) {limit = 20; offset = 0}
        this.PostList.fetch({data:{
            'limit': limit,
            'offset':offset
        }
        });
        $('#post-data').html(this.PostListView.render().el);
    },

    PostDetails:function (id) {

        if(Apps.allLoadedPosts != undefined){
            this.DetailPost = Apps.allLoadedPosts.get('/mobile/api/v1/post/'+ id +'/');
            this.PostView = new Apps.Views.PostView({model:this.DetailPost});
            $('#post-data').html(this.PostView.render().el);
        } else {
            this.PostList = new Apps.Collections.PostCollection();
            this.PostListView = new Apps.Views.PostListView({model : this.PostList});

            var _this = this;
            this.PostList.fetch({ url: '/mobile/api/v1/post/?id__exact='+ id}).then(function(){
                this.DetailPost = _this.PostList.get('/mobile/api/v1/post/'+ id +'/');
                this.PostView = new Apps.Views.PostView({model:this.DetailPost});
                $('#post-data').html(this.PostView.render().el);
            });
        }
    },

    AddPost: function() {
        this.NewPostView = new Apps.Views.NewPostView();
        $('#post-data').html(this.NewPostView.render().el);
        initmap();
    }

});

var app = new Apps.Routers.PostRouter();
Backbone.history.start();
