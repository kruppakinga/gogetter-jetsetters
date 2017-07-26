import requests
import json
from flask import jsonify
from flask import render_template, flash, redirect, session, url_for, request, make_response, abort
from app import models, db
from flask_bootstrap import Bootstrap

from secret import user, pwd

from app import app

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/shelf')
def shelf():
	return render_template('shelf.html')

@app.route('/hotels', methods=['GET'])
def get_hotels():
	hotels = models.Hotel.query.all()
	result = []
	for h in hotels:
		result.append( {'name' : h.name ,
						'code' : h.code ,
						'url' : url_for('get_hotel', hotel_id=h.code, _external=True)
						}
			)
	return jsonify(  result )

@app.route('/hotels/<string:hotel_id>', methods=['GET'])
def get_hotel(hotel_id):
	h = models.Hotel.query.filter(models.Hotel.code == hotel_id).first()
	if h == None:
		abort(404)
	result = []
	result.append( { 'name' : h.name ,
					 'review_score': h.review_score,
					 'location' : { 'latitude'  : h.latitude, 'longitude'  : h.longitude },
					 'description' : h.desc,
					 'reviews_url' : url_for('get_hotel_reviews', hotel_id=h.code, _external=True),
					 'photos_url' : url_for('get_hotel_photos', hotel_id=h.code, _external=True),
					 'reviews_breakdown' : url_for('get_hotel_review_breakdown', hotel_id=h.code, _external=True),
					 'main_photo' : h.main_pic,
					 'hotel_url' : h.booking_url,
					 'hotel_id' : h.code

	} )
	return jsonify(  result  )


@app.route('/hotels/reviews/<string:hotel_id>', methods=['GET'])
def get_hotel_reviews(hotel_id):
	hotel = models.Hotel.query.filter(models.Hotel.code == hotel_id).first()
	rev_result = []
	for r in hotel.reviews:
		rev_result.append ( { 'headline' : r.headline ,
							  'pro' : r.pro,
							  'con' : r.con,
							  'avg_score' : r.avg_score,
							  'hotel_id' : hotel_id
							} )

	return jsonify(  rev_result  )

@app.route('/hotels/photos/<string:hotel_id>', methods=['GET'])
def get_hotel_photos(hotel_id):
	hotel = models.Hotel.query.filter(models.Hotel.code == hotel_id).first()
	pics_result = []
	for pic in hotel.pics:
		pics_result.append ( { 'url' : pic.url ,
							   'url_max_300' : pic.url_max_300,
							   'hotel_id' : hotel_id
							} )

	return jsonify(  pics_result  )


@app.route('/hotels/review_breakdown/<string:hotel_id>', methods=['GET'])
def get_hotel_review_breakdown(hotel_id):
	hotel = models.Hotel.query.filter(models.Hotel.code == hotel_id).first()
	rev_result = []
	for r in hotel.review_breakdowns:
		rev_result.append ( { 'customer_type' : r.customer_type ,
							  'total' : r.total,
							  'clean' : r.clean,
							  'comfort' : r.comfort,
							  'location' : r.location,
							  'staff' : r.staff,
							  'value' : r.value,
							  'wifi' : r.wifi,
							  'hotel_id' : hotel_id
							} )
	return jsonify(  rev_result  )

@app.route('/compare', methods=['GET'])
def compare():
	result = []
	hotels = request.args.to_dict()
	checkin = '2017-12-05'
	checkout = '2017-12-06'
	for key, value in hotels.items():
		if key == 'checkin':
			checkin = value
		elif key == 'checkout':
			checkin = value
		else:
			hotel = models.Hotel.query.filter(models.Hotel.code == value).first()
			hotel_data = json.loads(get_hotel(value).data)
			if len(hotel_data) < 1:
				abort(500)

			static_data = json.loads(get_hotel(value).data)[0]

			price = get_available_hotel(checkin, checkout, hotel.code) 
			static_data.update(price)
			result.append ( static_data )
	return jsonify( result )


def get_available_hotel( checkin, checkout, hotel_id):
	url = 'https://distribution-xml.booking.com/json/getHotelAvailabilityV2?checkin={}&checkout={}&room1=A,A&output=room_details,hotel_details&hotel_ids={}'.format(checkin, checkout,  hotel_id)
	print (url)
	hotel = requests.get(url, auth=(user, pwd)).json()
	if len(hotel['hotels']) == 0:
	 	abort(500)

	return {'booking_url' : hotel['hotels'][0]['hotel_url'], 
			'room_min_price' : hotel['hotels'][0]['price'], 
			'breakfast_included' : hotel['hotels'][0]['room_min_price']['breakfast_included'],
			'currency' : hotel['hotels'][0]['hotel_currency_code']
			}	


@app.errorhandler(500)
def not_found(error):
	return make_response(jsonify({'error': 'Hotel is not available in that time interval'}), 500)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Hotel does not exist'}), 404)

