
$(document).ready(function() {
    $(".addtitle").click(function(e){
        e.preventDefault();
        $(".titlefield").toggle(200,function(){
            if($(".addtitle").text()=='Hide title'){
                $(".addtitle").text('Show title')
            }else{
                $(".addtitle").text('Hide title');
            }
        });
    });


    $('#id_username').blur(function(e){
        e.stopPropagation();
        var v = $('#id_username').val()
        if( v == '.' || v == '..'||v == '...'||v == '....'||v == '.....'||v == '......'||v == '.......'||v == '........') {
            alert('Please enter a valid username');
            $('#id_username').focus();
        }
    
    });
});
