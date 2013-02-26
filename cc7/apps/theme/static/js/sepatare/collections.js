Posts.Collections.Post = Backbone.Tastypie.Collection.extend({
    urlRoot: 'api/v1/post/',
    // the model for this collation is post
    model: Posts.Models.Post
})

