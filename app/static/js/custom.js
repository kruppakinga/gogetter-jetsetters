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
};

function clickHandler() {
	console.log('inside click handler');
};

