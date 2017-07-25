import requests
import json
from flask import jsonify
from flask import render_template, flash, redirect, session, url_for, request, g
from app import models, db


from app import app

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


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
					 'reviews_url' : url_for('get_hotel_reviews', hotel_id=h.code, _external=True),
					 'photos_url' : url_for('get_hotel_photos', hotel_id=h.code, _external=True),

	} )
	return jsonify(  result  )


@app.route('/hotels/reviews/<string:hotel_id>', methods=['GET'])
def get_hotel_reviews(hotel_id):
	hotel = models.Hotel.query.filter(models.Hotel.code == hotel_id).first()
	rev_result = []
	for r in hotel.reviews:
		rev_result.append ( { 'headline' : r.headline ,
							  'pro' : r.pro,
							  'con' : r.con
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

@app.route('/compare', methods=['GET'])
def compare():
	result = []
	hotels = request.args.to_dict()
	for key, hotel_id in hotels.items():
		hotel = models.Hotel.query.filter(models.Hotel.code == hotel_id).first()
		result.append ( json.loads(get_hotel(hotel_id).data)[0] )
	print ( result )
	return jsonify( result )


