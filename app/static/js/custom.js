$(function(){

	// function scrollLink(){
	//     var t=100;

	//     $(".scroll-link").click(function(l){
	//         l.preventDefault(),$("html, body").animate({
	//         scrollTop:$($(this).attr("href")).offset().top-t},500)
	//     }
	// )}

	$('.tagline').on('click', function(e){
		clickHandler(e);
	});

	loadView();


});

function loadView() {
    var self = this;

    console.log('inside loadView');
    $('[data-toggle="tooltip"]').tooltip();

    //Navigation Menu Slider
    $('#nav-expander').on('click',function(e){
      e.preventDefault();
      $('body').toggleClass('nav-expanded');
    });
    $('#nav-close').on('click',function(e){
      e.preventDefault();
      $('body').removeClass('nav-expanded');
    });


    // Initialize navgoco with default options
    $(".panel").navgoco({
        accordion: false,
        openClass: 'open',
        save: true,
        cookie: {
            name: 'navgoco',
            expires: false,
            path: '/'
        },
        slide: {
            duration: 300,
            easing: 'swing'
        }
    });
};

function clickHandler() {
	console.log('inside click handler');
};

