function scrollLink(){
    var t=100;

    $(".scroll-link").click(function(l){
        l.preventDefault(),$("html, body").animate({
        scrollTop:$($(this).attr("href")).offset().top-t},500)
    }
)}