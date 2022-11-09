$(document).ready(function(){
    function getActiveLabel(){
        return $("#mainCard7 .btn-group input:checked").attr("id");
    }

    $("#mainCard7 .btn-group label").click(function(){
        $(this).addClass("text-white").removeClass("text-dark");
        $("label").not($(this)).addClass("text-dark").removeClass("text-white");
    });

    idActiveLabel = getActiveLabel();
    $("[for="+idActiveLabel+"]").toggleClass("text-dark text-white");
});