$(function() {
    
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

    var setCommentHeight = function(){
        $('.commentbody').each(function(){
            true_height = $(this).children('p').height
            if(true_height > '250'){
                $('p').html('<a class="toggleMe" > ... </a>')
                .css({'position':'relative','height':'50px', 'backgrounColor':'red'})
                .appendTo($(this))
                $('.toggleMe').click(function(){
                    $(this).parent('div').toggle(function(){$(this).css('height','true_height')});
                });
                $(this).css('height','250px').
                $('.commentbody')
            }
        });    
    }
    $('.confirm').click(function(e){
        if(confirm('Delete this comment?')) return true;
    });

    //preparePage();
    
/* Katten: 130310 This function sends js into an infinity loop, not sure why
    $('body').html(function(i, html) {
        return html.replace(/(?:http:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?(.+)/g,
        '<iframe width="420" height="345" src="http://www.youtube.com/embed/$1" frameborder="0" allowfullscreen></iframe>');
    });
*/
});


/*

function preparePage() {
    var submittedMsg = false;

    document.getElementById('msgForm').onsubmit = function () {
        // prevent form from submitting if no msg
        if (document.getElementById('msgField').value === '' ) {
            document.getElementById('errorMsg').innerHTML = "please type a message";
            // stop the form
            return false;
        } else {
            // reset and allow submit
            document.getElementById('errorMsg').innerHTML = "";
            // and disable the submit button to prevent dubble submits
            document.getElementById("submitMsg").disabled = true;
            document.getElementById("errorMsg").innerHTML = "processing...";
            submittedMsg = true;
            return true;
        }
    };

}
 */

