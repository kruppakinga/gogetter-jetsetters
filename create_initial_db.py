#!venv/bin/python
import requests
import json
import time

from app import db, models


#INSERT YOUR BOOKING API USERNAME AND PWD HERE
user = 'USER'
pwd = 'PWD'

def get_cities():
	limit_rows = '1000'
	base_url = 'https://distribution-xml.booking.com/json/bookings.getCities?countrycodes=nl&languagecodes=en&rows=' + limit_rows + '&offset='
	url = base_url
	result = []
	i = 0
	cities = requests.get(url + '0&city_ids=-2140479', auth=(user, pwd)).json()
	
	for city in cities:
		c = models.City(name=city['name'], code = city['city_id'])
		db.session.add(c)
		db.session.commit()

		ts = time.time()
		url = 'https://distribution-xml.booking.com/json/bookings.getHotels?city_ids={}&languagecode=en&rows=10'.format(city['city_id'])
		hotels = requests.get(url, auth=(user, pwd)).json()
		for hotel in hotels:
			h = models.Hotel(name=hotel['name'], code = hotel['hotel_id'], address = hotel['address'], url = hotel['url'],  latitude = hotel['location']['latitude'], longitude = hotel['location']['longitude'], review_score=hotel['review_score'], city = c)
			db.session.add(h)

			url = 'https://distribution-xml.booking.com/json/bookings.getHotelDescriptionPhotos?hotel_ids={}'.format(hotel['hotel_id'])
			pics = requests.get(url, auth=(user, pwd)).json()
			for pic in pics:
				p = models.Picture(url=pic['url_original'], url_max_300 = pic['url_max300'], code=pic['photo_id'], hotel = h)
				db.session.add(p)

			url = 'https://distribution-xml.booking.com/json/bookings.getBookingcomReviews?hotel_ids={}'.format(hotel['hotel_id'])
			reviews = requests.get(url, auth=(user, pwd)).json()
			for review in reviews:
				r = models.Review(pro=review['pros'], con = review['cons'], headline=review['headline'], avg_score=review['average_score'], hotel = h)
				db.session.add(r)

			url = 'https://distribution-xml.booking.com/json/bookings.getHotelPhotos?hotel_ids={}'.format(hotel['hotel_id'])
			main_pic = requests.get(url, auth=(user, pwd)).json()
			h.main_pic = pic['url_max300']

			url = 'https://distribution-xml.booking.com/json/bookings.getBookingcomReviewScores?hotel_ids={}'.format(hotel['hotel_id'])
			scores = requests.get(url, auth=(user, pwd)).json()
			for sc in scores:
				breakdown = sc['score_breakdown']
				for s in breakdown:
					cust_type = s['customer_type']
					print(cust_type)
					for q in s['question']:
						if q['question'] == 'total':
							wifi = total = q['score']
							print(total)
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
						comfort = comfort, location = location, staff = staff, value = value_money, wifi = wifi)
					db.session.add(sc_bdown)
			
			db.session.add(h)

		db.session.add(c)
		db.session.commit()
		print (time.time() - ts)

	

get_cities()
