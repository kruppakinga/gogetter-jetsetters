$(function(){

	$('.compare').on('click', function(e){
		var hotelsArray = $(this).data('hotels');
		compareHotels(hotelsArray);
		console.log(hotelsArray);
	});

	loadView2();

});

//hoist global variables:
var reviewBreakdown = {
	value: [0.0],
	clean: [0.0],
	comfort: [0.0],
	location: [0.0],
	staff: [0.0],
	wifi: [0.0]
};

function loadView2() {
    var self = this;

    getHotels();
    var hotelsArray = ["10082", "10074", "10024"];
    compareHotels(hotelsArray);

};

function initMap(location, num) {
    var hotelLoc = {lat: location.latitude, lng: location.longitude};
    var map = new google.maps.Map(document.getElementById('map-' + num), {
      zoom: 15,
      center: hotelLoc
    });
    var marker = new google.maps.Marker({
      position: hotelLoc,
      map: map
    });
}

function compareHotels(hotels) {
	console.log('inside click handler');

	//GET all hotels
    var url = "/compare?1=" + hotels[0] + "&2=" + hotels[1]+ "&3=" + hotels[2] + "&checkin=2017-12-05&checkout=2017-12-06";
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

	for(var i = 0; i < hotelsArray.length; i++){

		var hotelId = hotelsArray[i].hotel_id;
		$("#name-" + i).text(data[i].name);
		$("#img-carousel-" + i).attr('id', "img-carousel-" + hotelId);
		$('#rating-' + i).text("Very Good " + hotelsArray[i].review_score);
		$('#price-' + i).text(hotelsArray[i].room_min_price + " " + hotelsArray[i].currency);
		$("#pro-" + i).attr('id', "pro-" + hotelId);
		$("#con-" + i).attr('id', "con-" + hotelId);
		$("#book-" + i).attr('href', data[i].hotel_url);

		initMap(data[i].location, i);

		$("#value-" + i).attr('id', "value-" + hotelId);
		$("#clean-" + i).attr('id', "clean-" + hotelId);
		$("#comfort-" + i).attr('id', "comfort-" + hotelId);
		$("#customer-type-" + i).attr('id', "customer-type-" + hotelId);
		$("#location-" + i).attr('id', "location-" + hotelId);
		$("#staff-" + i).attr('id', "staff-" + hotelId);
		$("#wifi-" + i).attr('id', "wifi-" + hotelId);

		$("#value-star-" + i).attr('id', "value-star-" + hotelId);
		$("#clean-star-" + i).attr('id', "clean-star-" + hotelId);
		$("#comfort-star-" + i).attr('id', "comfort-star-" + hotelId);
		//$("#customer-type-star" + i).attr('id', "customer-type-" + hotelId);
		$("#location-star-" + i).attr('id', "location-star-" + hotelId);
		$("#staff-star-" + i).attr('id', "staff-star-" + hotelId);
		$("#wifi-star-" + i).attr('id', "wifi-star-" + hotelId);

		var description = data[i].description;
		var descriptionArray = description.split(".");
		var descriptionFirstSentence = descriptionArray[0]; 
		$('#description-' + i).html(descriptionFirstSentence);

		getHotelReviewsBreakdown(hotelsArray[i].reviews_breakdown);
		getHotelReviewsById(hotelsArray[i].reviews_url);
		getHotelPhotosById(hotelsArray[i].photos_url);
	};

};

function compareHotelsOnError() {
	console.log('inside getHotelsOnError');
};

function getHotelPhotosById(photosUrl, i) {

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

	for (var i = 0; i < 3; i++) {
		$('#img-carousel-' + data[i].hotel_id).find(".img-" + i).attr('src', data[i].url);
	}
	
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

	//harcoded review for now:

	if (data[1].pro && data[1].pro.length > 0) {
		$("#pro-" + data[0].hotel_id).html('"' + data[1].pro + '"');
	} else {
		$("#pro-" + data[0].hotel_id).text("None");
	}

	if (data[1].con && data[1].con.length > 0) {
		$("#con-" + data[0].hotel_id).html('"' + data[1].con + '"');
	} else {
		$("#con-" + data[0].hotel_id).text("None");
	}

};

function getHotelReviewsByIdOnError() {
	console.log('inside get reviews - error');
};

function getHotelReviewsBreakdown(breakdownUrl) {

	//GET reviews
    var url = breakdownUrl;
    var settings = {
        cache: true
        , contentType: "application/json; charset=utf-8" 
        , dataType: "json"
        , success: getHotelReviewsBreakdownOnSuccess 
        , error: getHotelReviewsBreakdownOnError
        , type: "GET"
    };
    $.ajax(url, settings);
};

function getHotelReviewsBreakdownOnSuccess(data) {

	var hotel_id = data[7].hotel_id;

	$("#value-" + hotel_id).text(data[0].value);
	highlightHighestRating("value", data, hotel_id);

	$("#clean-" + hotel_id).text(data[0].clean);
	highlightHighestRating("clean", data, hotel_id);

	$("#comfort-" + hotel_id).text(data[0].comfort);
	highlightHighestRating("comfort", data, hotel_id);

	$("#location-" + hotel_id).text(data[0].location);
	highlightHighestRating("location", data, hotel_id);

	$("#staff-" + hotel_id).text(data[0].staff);
	//highlightHighestRating("staff", data, hotel_id);

	// if (data[0].staff == reviewBreakdown.staff[0]){
	// 	//$("#staff-" + hotel_id).css('background-color', '#FFDF00');
	// 	$("#staff-star-" + hotel_id).css('display', 'inline');
	// 	reviewBreakdown.staff[0] = data[0].staff;
	// 	reviewBreakdown.staff[1] = hotel_id;
	// }

	$("#wifi-" + hotel_id).text(data[0].wifi);
	highlightHighestRating("wifi", data, hotel_id);

};

function highlightHighestRating(prop, data, hotel_id){
	console.log(prop, data);
	if (data[0][prop] > reviewBreakdown[prop][0]){
		if (reviewBreakdown[prop][1]) {
			//$("#" + prop + "-" + reviewBreakdown[prop][1]).css('background-color', 'transparent');
			$("#" + prop + "-star-" + reviewBreakdown[prop][1]).toggle();
			//fa-star-o
		}
		//$("#" + prop + "-" + hotel_id).css('background-color', '#FFDF00');
		$("#" + prop + "-star-" + hotel_id).find(".fa-star").toggle();
		reviewBreakdown[prop][0] = data[0][prop];
		reviewBreakdown[prop][1] = hotel_id;
	}
};

function getHotelReviewsBreakdownOnError() {
	console.log('inside get reviews breakdown - error');
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
	console.log('inside getHotelsOnSuccess. hotels: ', data);

	//$('.test').text(data[0].name);
};

function getHotelsOnError() {
	console.log('inside getHotelsOnError');
};

// function getHotelById() {

// 	var id = "10004";
// 	//"10007"
// 	//"10008"

// 	//GET all hotels
//     var url = "/hotels/" + id;
//     var settings = {
//         cache: true
//         , contentType: "application/json; charset=utf-8" 
//         , dataType: "json"
//         , success: getHotelByIdOnSuccess 
//         , error: getHotelByIdOnError
//         , type: "GET"
//     };
//     $.ajax(url, settings);
// };

// function getHotelByIdOnSuccess(data) {
// 	console.log('inside getHotelByIdOnSuccess. hotel data.name: ', data[0].name);
// 	// console.log(data[0]);
// 	// console.log(data[0].photos_url);
// 	$("#column-0").find('h4').text(data[0].name);

// 	var photosUrl = data[0].photos_url;
// 	var reviewsUrl = data[0].reviews_url;

// 	getHotelPhotosById(photosUrl);
// 	getHotelReviewsById(reviewsUrl);

// 	var description = data[0].description;
// 	var descriptionArray = description.split(".");
// 	var descriptionFirstSentence = descriptionArray[0]; 

// 	//console.log('descriptionArray[0]', descriptionArray[0]);

// 	$('#description-0').html(descriptionFirstSentence);
// };

// function getHotelByIdOnError() {
// 	console.log('inside getHotelByIdOnError');
// };

