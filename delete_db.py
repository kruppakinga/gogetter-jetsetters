#!venv/bin/python

from app import db, models

def deleteEntry(entries):
	for e in entries:
		db.session.delete(e)
	db.session.commit()

cities = models.City.query.all()
deleteEntry(cities)

hotels = models.Hotel.query.all()
deleteEntry(hotels)


reviews = models.Review.query.all()
deleteEntry(reviews)

pictures = models.Picture.query.all()
deleteEntry(pictures)


