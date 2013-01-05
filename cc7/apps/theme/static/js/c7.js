
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
});
