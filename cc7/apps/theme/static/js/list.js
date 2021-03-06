$(".edit").click(function(event){
    var id = this.id;
    var list =  $(this).attr('value');


    var title = $(this).closest('td').siblings('.item_title').text();
    var description = $(this).closest('td').siblings('.item_description').text();

    var top = event.pageY-30;

    var overlay = $(insertform =
    '<div id="overlay" style="position: fixed; top: '+ top +'px; left: 4%;">' +
        '<form action="" method="post" class="update_form" >'+
        '<table class="table table-striped table-bordered overlay_table">' +
        '<tr>' +
            '<th class="small_icon_td">Title</th>' +
                '<td>' +
                '<input id="id_title" class="editing_title" type="text" value="' + title + '" name="title" maxlength="120">' +
                '</td>' +

        '</tr>' +
        '<tr>' +
            '<th>Body</th>' +
                '<td class="textarea_edit_td">' +
                    '<textarea contenteditable="true" id="id_description" name="description" style="overflow: hidden; word-wrap: break-word; resize: both; height: 120px;">' + description +'</textarea>' +
                '</td>' +
        '</tr>' +
        '<tr>' +
            '<th>Edit</th>' +
            '<td >' +
                '<a href=""><button id="+id+" class="btn btn-primary editing">Update</button></a>' +
            '</td>' +
        '</tr>' +
        '<tr>' +
            '<th>Cancel</th>' +
            '<td class="small_icon_td">' +
                '<a href=""><button class="btn btn-danger">Cancel</button></a>' +
                '<input id="id_item_list" type="hidden" name="item_list" value="'+list+'">' +
                '<input id="id_list_item" type="hidden" name="list_item" value="'+id+'">' +
                '<input type="hidden" value="'+csrftoken +'" name="csrfmiddlewaretoken">' +
                '<input id="id_order" type="hidden" name="order" value="1">' +
                '<input id="extra" type="hidden" name="order" value="1">' +
                '<input id="update_item" type="hidden" name="update_item" value="post" >' +
            '</td>' +
        '</tr>' +
    '</table>' +
    '</form>' +
    '</div>');

    overlay.appendTo(document.body);


    $('button.editing').click(function(event){
        $('.update_form').submit(
            {
                success: function(data) {
                    var newlistrow = row_templat(data);
                    $('.now_editing').after(newlistrow);
                    $('.now_editing').fadeOut();
                },
                error: function(data, status, error){
                }
            }
        );
    });
});
