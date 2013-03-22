
$(".edit").click(function(event){
    var id = this.id;
    var list =  $(this).attr('value');


    var title = $(this).closest('td').siblings('.item_title').text();
    var description = $(this).closest('td').siblings('.item_description').text();

    var top = event.pageY-30;

    var overlay = $(insertform =
    '<div id="overlay" style="position: fixed; top: '+ top +'px; left: 4%;">' +
        '<form action="" method="post" class="update_form" >'+
        '<table class="table table-striped table-bordered">' +
        '<tr class="now_editing">' +
            '<td>' +
            '<input id="id_title" class="editing_title" type="text" value="' + title + '" name="title" maxlength="120">' +
            '</td>' +
            '<td>' +
                '<textarea id="id_description" name="description" >' + description +'</textarea>' +
            '</td>' +
            '<td class="small_icon_td">' +
                '<a href=""><button id="+id+" class="btn btn-primary editing">Update</button></a>' +
            '</td>' +
            '<td class="small_icon_td">' +
                '<a href=""><button class="btn btn-danger">Cancel</button></a>' +
            '</td>' +
            '<td>' +
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

    //var overlay = $('<div id=\"overlay\"> </div>')
    overlay.appendTo(document.body);

    //$('#'+id).parents('tr').after(insertform);
    //$('#'+id).parents('tr').fadeOut();

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



$(".remove").click(function(event){
    id = this.id;


$.ajax({
    url: '/list/api/v1/listitem/'+ id + '/',
    type: 'DELETE',
    contentType: 'application/json',
    dataType: 'json',
    processData: false,
    success: function(data, textStatus, jqXHR) {
    $('#'+id).parents('tr').fadeOut();
    },
error: function(data, status, error){
    alert('Oooops!');
    }

});

});
