
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

    preparePage();

});


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