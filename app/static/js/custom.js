$(function(){

	// function scrollLink(){
	//     var t=100;

	//     $(".scroll-link").click(function(l){
	//         l.preventDefault(),$("html, body").animate({
	//         scrollTop:$($(this).attr("href")).offset().top-t},500)
	//     }
	// )}

	// $('#comparison-header').on('click', function(e){
	// 	clickHandler(e);
	// });

	$('#comparison-header').on('click', function(e){
		getHotelById(e);
	});

    $('.external-link').on('click', function(e){
        console.log('inside link square click');
        //e.stopPropogation();
        //goToFullView(e);
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

function goToFullView(){
    event.cancelBubble = true;
    if(event.stopPropagation) {
     event.stopPropagation();
    }
    window.open('/shelf','_blank');
};

function clickHandler() {
	console.log('inside click handler');

	//GET all hotels
    var url = "/hotels";
    var settings = {
        cache: false
        , contentType: "application/json; charset=utf-8" 
        , dataType: "json"
        , success: getHotelsOnSuccess 
        , error: getHotelsOnError
        , type: "GET"
    };
    $.ajax(url, settings);
};

function getHotelsOnSuccess(data) {
	console.log('inside getHotelsOnSuccess. hotels: ', data);

	$('.test').text(data[0].name);
};

function getHotelsOnError() {
	console.log('inside getHotelsOnError');
};

function getHotelById() {
	console.log('inside getHotelById');

	var id = "10004";
	//"10007"
	//"10008"

	//GET all hotels
    var url = "/hotels/" + id;
    var settings = {
        cache: false
        , contentType: "application/json; charset=utf-8" 
        , dataType: "json"
        , success: getHotelByIdOnSuccess 
        , error: getHotelByIdOnError
        , type: "GET"
    };
    $.ajax(url, settings);
};

function getHotelByIdOnSuccess(data) {
	console.log('inside getHotelByIdOnSuccess. hotel data.name: ', data[0].name);
	console.log(data[0]);
	console.log(data[0].photos_url);
	$("#column-0").find('h4').text(data[0].name);

	var photosUrl = data[0].photos_url;
	var reviewsUrl = data[0].reviews_url;

	getHotelPhotosById(photosUrl);
	getHotelReviewsById(reviewsUrl);
};

function getHotelByIdOnError() {
	console.log('inside getHotelByIdOnError');
};

function getHotelPhotosById(photosUrl) {
	console.log('inside getHotelById');

	var id = "10004";
	//"10007"
	//"10008"

	//GET photos
    var url = photosUrl;
    var settings = {
        cache: false
        , contentType: "application/json; charset=utf-8" 
        , dataType: "json"
        , success: getHotelPhotosByIdOnSuccess 
        , error: getHotelPhotosByIdOnError
        , type: "GET"
    };
    $.ajax(url, settings);
};

function getHotelPhotosByIdOnSuccess(data) {
	console.log('inside getHotelPhotosByIdOnSuccess. hotel photos: ', data);
	console.log(data);
	console.log('photo url', data[0].url);

	$("#img-1").attr('src', data[0].url);
};

function getHotelPhotosByIdOnError() {
	console.log('inside getHotelPhotosByIdOnError');
};

function getHotelReviewsById(reviewsUrl) {
	console.log('inside getHotelById');

	//GET reviews
    var url = reviewsUrl;
    var settings = {
        cache: false
        , contentType: "application/json; charset=utf-8" 
        , dataType: "json"
        , success: getHotelReviewsByIdOnSuccess 
        , error: getHotelReviewsByIdOnError
        , type: "GET"
    };
    $.ajax(url, settings);
};

function getHotelReviewsByIdOnSuccess(data) {
	console.log('inside get reviews - success. hotel reviews: ', data);

	$("#pro-1").html('"' + data[0].pro + '"');
	$("#con-1").html('"' + data[0].con + '"');
};

function getHotelReviewsByIdOnError() {
	console.log('inside get reviews - error');
};


