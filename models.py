from application import db
from datetime import datetime

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
	
class TempCurrent(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	tmax = db.Column(db.Float, nullable=False)
	tmin = db.Column(db.Float, nullable=False)
	tcurrent = db.Column(db.Float, nullable=False)
	location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
	locations = db.relationship('Locations', backref=db.backref('tempcurrent', lazy=True))
	
	def __init__(self, location_id, tmax, tmin, tcurrent):
		self.location_id = location_id
		self.tmax = tmax
		self.tmin = tmin
		self.tcurrent = tcurrent
		
	def __repr__(self):
		return '<Location ID: {} TMax: {} TMin: {} TCurrent: {}>'.format(self.location_id,self.tmax,self.tmin,self.tcurrent)
	