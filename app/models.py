from app import db
from sqlalchemy.orm import object_session
from sqlalchemy import select, func

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), index=True)
    area = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    cities = db.relationship('City', backref = 'country', lazy='dynamic')

    def __repr__(self):
        return '<Country %r>' % (self.name)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    code = db.Column(db.String(64), index=True, unique=True)
    hotels = db.relationship('Hotel', backref = 'city', lazy='dynamic')
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    country_id = db.Column(db.Integer, db.ForeignKey('country.code'))


    def __repr__(self):
        return '<City %r>' % (self.name)

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    code = db.Column(db.String(64), index=True, unique=True)
    address = db.Column(db.String(256))
    city_id = db.Column(db.Integer, db.ForeignKey('city.code'))
    url = db.Column(db.String(256))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    reviews = db.relationship('Review', backref = 'hotel', lazy='dynamic')
    pics = db.relationship('Picture', backref = 'hotel', lazy='dynamic')
    review_score = db.Column(db.Float)


    def __repr__(self):
        return '<Hotel %r>' % (self.name)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pro =  db.Column(db.Text)
    con =  db.Column(db.Text)
    headline =  db.Column(db.Text)
    date = db.Column(db.DateTime)
    avg_score = db.Column(db.Float)

    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.code'))

    def __repr__(self):
        return '<Review %r>: %r %r %r' % (self.avg_score, self.headline, self.pro, self.con)


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    url_max_300 = db.Column(db.String(256))   
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.code'))
    code = db.Column(db.String(64))

    def __repr__(self):
        return (self.url)


