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

@app.route('/shelf')
def shelf():
	return render_template('shelf.html')

@app.route('/hotels', methods=['GET'])
def get_hotels():
	hotels = models.Hotel.query.all()
	result = []
	for h in hotels:
		result.append( {'name' : h.name ,
						'hotel_code': h.code,
						'url' : url_for('get_hotel', hotel_id=h.code, _external=True)
						}
			)
	return jsonify(  {'hotels' :   result } )

@app.route('/hotels/<string:hotel_id>', methods=['GET'])
def get_hotel(hotel_id):
	hotels = models.Hotel.query.all()
	hotel = [h for h in hotels if h.code == hotel_id]
	# if len(hotel)==0:
	# 	abort(404)
	result = []
	for h in hotel:
		result.append( { 'name' : h.name ,
						 'review_score': h.review_score,

			} )
	return jsonify(  result  )
