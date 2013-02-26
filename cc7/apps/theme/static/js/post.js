
// Models
window.Post = Backbone.Tastypie.Model.extend({
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

window.PostView = Backbone.View.extend({

    template:_.template($('#singel_post_template').html()),

    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }

});

// Router
var AppRouter = Backbone.Router.extend({

    routes:{
        "":"list",
        "detail_id?:id":"PostDetails"
    },

    list:function () {
        this.PostList = new PostCollection();
        this.PostListView = new PostListView({model:this.PostList});
        this.PostList.fetch();
        $('#post-data').html(this.PostListView.render().el);
    },

    PostDetails:function (id) {
        this.Post = this.PostList.models[12];
        this.PostView = new PostView({model:this.Post});
        $('#post-data').html(this.PostView.render().el);
    }
});

var app = new AppRouter();
Backbone.history.start();


