Posts.View.PostListView = Backbone.View.extend({

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

Posts.View.PostListItemView = Backbone.View.extend({

    tagName:"li",

    template:_.template($('#post_list_template').html()),

    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }

});

Posts.View.PostView = Backbone.View.extend({

    template:_.template($('#singel_post_template').html()),

    render:function (eventName) {
        $(this.el).html(this.template(this.model.toJSON()));
        return this;
    }

});

