
// Models
window.Post = Backbone.Tastypie.Model.extend({
    idAttribute : '_id',
    validate: function (attrs) {
        if (attrs.id < 0) {
            return "id cannot be less then 0"
        }
        if (attrs.id === "") {
            return "id cannot be blank"
        }

    }

});

window.PostCollection = Backbone.Tastypie.Collection.extend({
    model:Post,
    urlRoot: 'api/v1/post/'
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

var AppRouter = Backbone.Router.extend({

    routes:{
        "":"list",
        "postrange/:from-:to":"range",
        "detail_id?:id":"PostDetails"
    },
    list:function () {
        this.PostList = new PostCollection();
        //console.log(this.PostList);
        this.PostListView = new PostListView({model:this.PostList});
        this.PostList.fetch({data:{'limit':10}});
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