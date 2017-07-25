import requests
import json
from flask import jsonify
from flask import render_template, flash, redirect, session, url_for, request, g
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
	result = []
	result.append( { 'name' : h.name ,
					 'review_score': h.review_score,
					 'location' : { 'latitude'  : h.latitude, 'longitude'  : h.longitude },
					 'description' : h.desc,
					 'reviews_url' : url_for('get_hotel_reviews', hotel_id=h.code, _external=True),
					 'photos_url' : url_for('get_hotel_photos', hotel_id=h.code, _external=True),
					 'reviews_breakdown' : url_for('get_hotel_review_breakdown', hotel_id=h.code, _external=True),
					 'main_photo' : h.main_pic,
					 'hotel_url' : h.booking_url

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
							  'avg_score' : r.avg_score
							} )
	
	return jsonify(  rev_result  )

@app.route('/hotels/photos/<string:hotel_id>', methods=['GET'])
def get_hotel_photos(hotel_id):
	hotel = models.Hotel.query.filter(models.Hotel.code == hotel_id).first()
	pics_result = []
	for pic in hotel.pics:
		pics_result.append ( { 'url' : pic.url ,
							   'url_max_300' : pic.url_max_300
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
							  'wifi' : r.wifi
							} )
	return jsonify(  rev_result  )

@app.route('/compare', methods=['GET'])
def compare():
	result = []
	hotels = request.args.to_dict()
	for key, hotel_id in hotels.items():
		hotel = models.Hotel.query.filter(models.Hotel.code == hotel_id).first()
		static_data = json.loads(get_hotel(hotel_id).data)[0] 

		price = get_available_hotel(hotel.code) 
		static_data.update(price)
		result.append ( static_data )
	print ( result )
	return jsonify( result )


def get_available_hotel(hotel_id):
	url = 'https://distribution-xml.booking.com/json/getHotelAvailabilityV2?checkin=2017-10-22&checkout=2017-10-23&room1=A,A&output=room_details,hotel_details&hotel_ids={}'.format(hotel_id)
	hotel = requests.get(url, auth=(user, pwd)).json()
	return {'booking_url' : hotel['hotels'][0]['hotel_url'], 
			'room_min_price' : hotel['hotels'][0]['price'], 
			'breakfast_included' : hotel['hotels'][0]['room_min_price']['breakfast_included'],
			'currency' : hotel['hotels'][0]['hotel_currency_code']
			}	
