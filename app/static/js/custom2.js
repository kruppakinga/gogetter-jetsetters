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

	loadView2();

});

function loadView2() {
    var self = this;

    getHotels();
    compareHotels();

    console.log('inside loadView');
};

function compareHotels() {
	console.log('inside click handler');

	//GET all hotels
    var url = "/compare?1=10004&2=10064&3=10023&checkin=2017-12-05&checkout=2017-12-06";
    var settings = {
        cache: true
        , contentType: "application/json; charset=utf-8" 
        , dataType: "json"
        , success: compareHotelsOnSuccess 
        , error: compareHotelsOnError
        , type: "GET"
    };
    $.ajax(url, settings);
};

function compareHotelsOnSuccess(data) {
	console.log('inside compareHotelsOnSuccess. hotels: ', data);

	var hotelsArray = data;

	//column-
	//img-carousel-
	//img-
	//description-
	//pro-
	//con-

	for(var i = 0; i < hotelsArray.length; i++){
		$("#img-" + i).attr('id', "#img-" + hotelsArray[i].name);
		getHotelPhotosById(hotelsArray[i].photos_url);
	};

	// for(var i = 0; i < hotelsArray.length; i++){
	// 	$("#column-" + i).find('h4').text(hotelsArray[i].name);
	// 	getHotelPhotosById(hotelsArray[i].photos_url);
	// 	console.log('currentIndex');
	// };

};

function compareHotelsOnError() {
	console.log('inside getHotelsOnError');
};

function getHotels() {

	//GET all hotels
    var url = "/hotels";
    var settings = {
        cache: true
        , contentType: "application/json; charset=utf-8" 
        , dataType: "json"
        , success: getHotelsOnSuccess 
        , error: getHotelsOnError
        , type: "GET"
    };
    $.ajax(url, settings);
};

function getHotelsOnSuccess(data) {
	//console.log('inside getHotelsOnSuccess. hotels: ', data);

	//$('.test').text(data[0].name);
};

function getHotelsOnError() {
	console.log('inside getHotelsOnError');
};

function getHotelById() {

	var id = "10004";
	//"10007"
	//"10008"

	//GET all hotels
    var url = "/hotels/" + id;
    var settings = {
        cache: true
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
	// console.log(data[0]);
	// console.log(data[0].photos_url);
	$("#column-0").find('h4').text(data[0].name);

	var photosUrl = data[0].photos_url;
	var reviewsUrl = data[0].reviews_url;

	getHotelPhotosById(photosUrl);
	getHotelReviewsById(reviewsUrl);

	var description = data[0].description;
	var descriptionArray = description.split(".");
	var descriptionFirstSentence = descriptionArray[0]; 

	//console.log('descriptionArray[0]', descriptionArray[0]);

	$('#description-0').html(descriptionFirstSentence);
};

function getHotelByIdOnError() {
	console.log('inside getHotelByIdOnError');
};

function getHotelPhotosById(photosUrl, i) {

	//var id = "10004";
	//"10007"
	//"10008"

	console.log(photosUrl);

	//GET photos
    var url = photosUrl;
    var settings = {
        cache: true
        , contentType: "application/json; charset=utf-8" 
        , dataType: "json"
        , success: getHotelPhotosByIdOnSuccess 
        , error: getHotelPhotosByIdOnError
        , type: "GET"
    };
    $.ajax(url, settings);
};

function getHotelPhotosByIdOnSuccess(data) {
	// console.log('inside getHotelPhotosByIdOnSuccess. hotel photos: ', data);
	// console.log(data);
	// console.log('photo url', data[0].url);

	$('.img-carousel-' + currentIndex).find("#img-" + currentIndex).attr('src', data[0].url);
};

function getHotelPhotosByIdOnError() {
	console.log('inside getHotelPhotosByIdOnError');
};

function getHotelReviewsById(reviewsUrl) {

	//GET reviews
    var url = reviewsUrl;
    var settings = {
        cache: true
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

	$("#pro-0").html('"' + data[0].pro + '"');
	$("#con-0").html('"' + data[0].con + '"');
};

function getHotelReviewsByIdOnError() {
	console.log('inside get reviews - error');
};


