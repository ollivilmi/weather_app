from app import db
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Locations(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), nullable=False)
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)
	
	def __init__(self, name, latitude, longitude):
		self.name = name
		self.latitude = latitude
		self.longitude = longitude
		
	def __repr__(self):
		return '<{}: {},{}>'.format(self.name,self.latitude,self.longitude)
		
class TempHistory(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	temp = db.Column(db.Float, nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
	locations = db.relationship('Locations', backref=db.backref('temphistory', lazy=True))
	
	def __init__(self, location_id, temp):
		self.location_id = location_id
		self.temp = temp
		
	def __repr__(self):
		return '<Location ID: {} Temperature: {} Date: {}>'.format(self.location_id,self.temp,self.date)