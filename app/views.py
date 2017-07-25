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
						'url' : url_for('get_hotel', hotel_id=h.code, _external=True),
						'review_url' : url_for('get_hotel_reviews', hotel_id=h.code, _external=True),
						'photos_url' : url_for('get_hotel_photos', hotel_id=h.code, _external=True),

						}
			)
	return jsonify(  result )

@app.route('/hotels/<string:hotel_id>', methods=['GET'])
def get_hotel(hotel_id):
	hotels = models.Hotel.query.all()
	hotel = [h for h in hotels if h.code == hotel_id]
	if len(hotel)!=1:
		abort(404)
	h = hotel[0]
	result = []
	result.append( { 'name' : h.name ,
					 'review_score': h.review_score,
	} )
	return jsonify(  result  )


@app.route('/hotels/reviews/<string:hotel_id>', methods=['GET'])
def get_hotel_reviews(hotel_id):
	hotels = models.Hotel.query.all()
	hotel = [h for h in hotels if h.code == hotel_id]
	if len(hotel)!=1:
		abort(404)
	rev_result = []
	for r in hotel[0].reviews:
		rev_result.append ( { 'headline' : r.headline ,
							  'pro' : r.pro,
							  'con' : r.con
							} )
	
	return jsonify(  rev_result  )

@app.route('/hotels/photos/<string:hotel_id>', methods=['GET'])
def get_hotel_photos(hotel_id):
	hotels = models.Hotel.query.all()
	hotel = [h for h in hotels if h.code == hotel_id]
	if len(hotel)!=1:
		abort(404)
	pics_result = []
	for pic in hotel[0].pics:
		pics_result.append ( { 'url' : pic.url ,
							  'url_max_300' : pic.url_max_300
							} )
	
	return jsonify(  pics_result  )
