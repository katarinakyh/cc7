Posts.Models.Post = Backbone.Tastypie.Model.extend({
    defaults: {
        title: '>>'
    },
    shortText : function(e){
        var fullText = this.get('body');
        var shortText = fullText;
        if (fullText.length > 100) {
            shortText = jQuery.trim(fullText).substring(0, 100)
                .split(" ").slice(0, -1).join(" ") + "...";
        }
        this.set('trunc_text', shortText );
    }

    // validate
});
