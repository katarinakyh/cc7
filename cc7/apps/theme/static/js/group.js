
$(".add_me").click(function(event){
    event.preventDefault()
    var group_id = this.id;
    var user_id = this.name

    var data = JSON.stringify({
        "member": '/group/api/v1/myprofile/'+user_id+'/',
        "group": '/group/api/v1/group/'+group_id+'/',
        "is_member": 1
    });


    $.ajax({
        url: '/group/api/v1/active_members/',
        type: 'POST',
        contentType: 'application/json',
        data: data,
        dataType: 'json',
        processData: false,
        success: function(data, textStatus, jqXHR) {
            window.location.reload(true);
        },
        error: function(data, status, error){
            alert('Oooops!');
        }
    })

});

$(".add_member").click(function(event){
    var user_id = this.id;
    var group_id = this.name;
    var key = $('span#group_id').html();

    var data = JSON.stringify({
        "member": '/group/api/v1/myprofile/'+user_id+'/',
        "group": '/group/api/v1/group/'+group_id+'/',
        "is_member": 1
    });

    $.ajax({
        url: '/group/api/v1/active_members/'+key+'/',
        type: 'PUT',
        contentType: 'application/json',
        data: data,
        dataType: 'json',
        processData: false,
        success: function(data, textStatus, jqXHR) {
            window.location.reload(true);
        },
        error: function(data, status, error){
        }
    });


});



$(".remove").click(function(event){
    var group_id = this.id;
    var user_id = this.name

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
