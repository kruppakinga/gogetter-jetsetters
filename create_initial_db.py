#!venv/bin/python
import requests
import json
import time
from secret import user, pwd

from app import db, models


def get_data():
	limit_rows = '1000'
	baseurl = 'https://distribution-xml.booking.com/json/bookings.'
	url = baseurl + 'getCities?countrycodes=nl&languagecodes=en&city_ids=-2140479'
	result = []
	cities = requests.get(url, auth=(user, pwd)).json()
	
	for city in cities:
		c = models.City(name=city['name'], code = city['city_id'])
		db.session.add(c)
		db.session.commit()

		ts = time.time()
		url = baseurl + 'getHotels?city_ids={}&languagecodes=en&rows=15'.format(city['city_id'])
		hotels = requests.get(url, auth=(user, pwd)).json()
		for hotel in hotels:
			h = models.Hotel(name=hotel['name'], code = hotel['hotel_id'], address = hotel['address'], url = hotel['url'],  
				latitude = hotel['location']['latitude'], longitude = hotel['location']['longitude'], review_score=hotel['review_score'],
				booking_url = hotel['url'],
				 city = c)
			db.session.add(h)

			url = baseurl + 'getHotelDescriptionPhotos?hotel_ids={}'.format(hotel['hotel_id'])
			pics = requests.get(url, auth=(user, pwd)).json()
			for pic in pics:
				p = models.Picture(url=pic['url_original'], url_max_300 = pic['url_max300'], code=pic['photo_id'], hotel = h)
				db.session.add(p)

			url = baseurl + 'getBookingcomReviews?hotel_ids={}&languagecodes=en'.format(hotel['hotel_id'])
			reviews = requests.get(url, auth=(user, pwd)).json()
			for review in reviews:
				r = models.Review(pro=review['pros'], con = review['cons'], headline=review['headline'], avg_score=review['average_score'], hotel = h)
				db.session.add(r)

			url = baseurl + 'getHotelPhotos?hotel_ids={}'.format(hotel['hotel_id'])
			main_pic = requests.get(url, auth=(user, pwd)).json()
			h.main_pic = pic['url_max300']

			url = baseurl + 'getHotelDescriptionTranslations?hotel_ids={}&languagecodes=en'.format(hotel['hotel_id'])
			descr = requests.get(url, auth=(user, pwd)).json()
			h.desc = descr[0]['description']

			url = baseurl + 'getBookingcomReviewScores?hotel_ids={}'.format(hotel['hotel_id'])
			scores = requests.get(url, auth=(user, pwd)).json()
			for sc in scores:
				breakdown = sc['score_breakdown']
				for s in breakdown:
					cust_type = s['customer_type']
					for q in s['question']:
						if q['question'] == 'total':
							wifi = total = q['score']
						if q['question'] == 'hotel_clean':
							clean = q['score']
						if q['question'] == 'hotel_comfort':
							comfort = q['score']
						if q['question'] == 'hotel_location':
							location = q['score']
						if q['question'] == 'hotel_services':
							services = q['score']
						if q['question'] == 'hotel_staff':
							staff = q['score']
						if q['question'] == 'hotel_value':
							value_money = q['score']
						if q['question'] == 'hotel_clean':
							clean = q['score']
					sc_bdown = models.ReviewBreakdown(customer_type=cust_type, total = total, clean = clean, 
						comfort = comfort, location = location, staff = staff, value = value_money, wifi = wifi,
						hotel = h)
					db.session.add(sc_bdown)
			
			db.session.add(h)

		db.session.add(c)
		db.session.commit()
		print (time.time() - ts)

	

get_data()
