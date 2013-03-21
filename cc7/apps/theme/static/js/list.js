
$("#add_to_list").click(function(event){
    event.preventDefault()
    var data = JSON.stringify({
        "csrftoken": csrftoken,
        "title": $('#id_title').val(),
        "description": $('#id_description').val(),
        "item_list": '/list/api/v1/itemlist/'+ $('#id_item_list').val()+'/',
        "order": $('#id_order').val()
    });

    $.ajax({
        url: '/list/api/v1/listitem/',
        type: 'POST',
        contentType: 'application/json',
        data: data,
        dataType: 'json',
        processData: false,
        success: function(data, textStatus, jqXHR) {
            var newlistrow = row_templat(data);
            $('#id_title').val('')
            $('#id_description').val('');
            $('#list_table tr:last').after(newlistrow);
            },
            error: function(data, status, error){
                alert('Oooops!');
            }
    })

});

row_templat = function (data) {
    var newlistrow =
        "<tr><td> <strong> <a href=detail/\""+ data.id +"\">"+ data.title +"</a></strong></td>" +
        "<td>"+data.description+"</td>" +
        "<td><button class=\"edit\" id=\""+ data.id +"\"><i class=\"icon-edit\"></i></button></td>" +
        "<td><button class=\"remove\" id="+data.id+">" +
        "<i class=\"icon-minus-sign\"></i></button></td>";
    return newlistrow;
}

$(".edit").click(function(event){
    var id = this.id;

    var title = $(this).closest('td').siblings('.item_title').text();
    var description = $(this).closest('td').siblings('.item_description').text();

    insertform =
        "<tr class=\"now_editing\"><td><input id=\"id_title\" class=\"editing_title\" type=\"text\" value=" + title +" name=\"title\" maxlength=\"120\"></td>" +
        "<td><textarea id=\"id_description\"  name=\"description\" >" + description +"</textarea></td>" +
        "<td><a href=\"\"><button id="+id+" class=\"btn btn-primary editing\"><i class=\"icon-edit\"></i> Update</button></a></td>" +
        "<td><a href=\"\"><button class=\"btn btn-danger\"><i class=\"icon-remove\"></i></button></a></td>" +
        "<input id=\"id_item_list\" type=\"hidden\" name=\"item_list\" value=\""+id+"\">" +
        "<input id=\"id_order\" type=\"hidden\" name=\"order\" value=\"1\">"


    $('#'+id).parents('tr').after(insertform);
    $('#'+id).parents('tr').fadeOut();

    $('button.editing').click(function(event){
        var title = $(this).parents('tr').find('#id_title').val();
        var description = $(this).parents('tr').find('#id_description').val();
        var order = $(this).parents('tr').find('#id_order').val();

        var data = JSON.stringify({
            "csrftoken": csrftoken,
            "title": title,
            "description": description,
            "item_list": '/list/api/v1/itemlist/'+ $('.the_list_id').text()+'/',
            "order": order

        });
        $.ajax({
            url: '/list/api/v1/listitem/'+id +'/',
            type: 'Put',
            contentType: 'application/json',
            data: data,
            dataType: 'json',
            processData: false,
            success: function(data, textStatus, jqXHR) {
                var newlistrow = row_templat(data);
                //$('#list_table tr:last').after(newlistrow);
                $('.now_editing').after(newlistrow);
                $('.now_editing').fadeOut();
            },
            error: function(data, status, error){
            }
        });

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
