Posts.Router = Backbone.Router.extend({
    routes: {
        '': 'index',
        'detail_id?:postid': 'detail',
        'search?:query':'query',
        '*other':'other'
    },


    index: function(DetailId) {
        var postViews = new Posts.Views.Posts({model:Posts.Models.Post});
        this.postsCollection = new Posts.Collections.Post();
        this.postViews = new Posts.Views.Posts({model:this.postsCollection });
        this.postsCollection.fetch();
        $('#post_list_template').html(this.postViews.render().el);
    },

    detail: function(DetailId) {
         this.post =  this.postsCollection.get(DetailId);
         this.postView = new Posts.Views.Posts({model:this.post});
         $('#singel_post_template').html(this.postView.render().el);
        //vent.trigger('postDetail:show', DetailId);
    },

    search: function(query) {
        console.log(query)
    },

    other: function(other) {
        alert('hmm..' + other + 'not sure what you mean')
    }
});

