from flask import Flask, flash, redirect, render_template, request, session, url_for, g, jsonify
from datetime import datetime, timedelta
import os
import re
from flask_sqlalchemy import SQLAlchemy
from flask_jsglue import JSGlue

import psycopg2

app = Flask(__name__)
JSGlue(app)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *

@app.route("/")
def index():
	update_temprecords()
	loc = db.session.query(Locations.name, TempCurrent.tmin, TempCurrent.tmax,\
	TempCurrent.tcurrent, TempCurrent.date).join(TempCurrent, Locations.id == TempCurrent.location_id).all()
	return render_template("index.html", loc=loc)
	
@app.route("/about", methods=["GET", "POST"])
def about():
	if request.method == "GET":
		return render_template("about.html", loc=get_locations())
    
@app.route("/history", methods=["GET", "POST"])
def history():
	if request.method == "GET":
		return render_template("history.html", loc=get_locations())
		
@app.route("/gethistory")
def gethistory():
	loc = request.args.get("loc")
	if loc == None:
		raise RunTimeError("missing location")
		
	days = request.args.get("days")
	if days == None:
		raise RunTimeError("missing amount of days")
	days = int(days)
	
	timespan = datetime.utcnow() - timedelta(days=days)
		
	data = db.session.query(TempHistory).filter(TempHistory.location_id == loc, TempHistory.date > timespan).all()
	history = [dict(temp=row.temp,date=row.date) for row in data]
	
	return jsonify(history)
	
@app.route("/getlocation")
def getlocation():
	loc = request.args.get("loc")
	if loc == None:
		raise RunTimeError("missing location")
		
	data = db.session.query(TempHistory).filter(TempHistory.location_id == loc).order_by(TempHistory.date.desc()).limit(10).all()
	temps = [dict(temp=row.temp, date=row.date) for row in data]
	
	return jsonify(temps)
	
@app.route("/add", methods=["GET", "POST"])
def add():
	if request.method == "GET":
		return render_template("add.html", loc=get_locations())
	else:
		temp = request.form.get("temp")
		loc = request.form.get("location")
		if temp == None:
			raise RunTimeError("no temperature to add")
		elif loc == None:
			raise RunTimeError("no location to add to")
		
		# Add temp to history table
		db.session.add(TempHistory(loc, temp))
		
		# Add temp to current and check if the temp is a new record
		cur = db.session.query(TempCurrent).filter(TempCurrent.location_id == loc).first()
		cur.tcurrent = temp
		cur.date = datetime.utcnow()
		
		if float(temp) > float(cur.tmax):
			cur.tmax = temp
		elif float(temp) < float(cur.tmin):
			cur.tmin = temp
			
		db.session.commit()
		
		return render_template("add.html", loc=get_locations())
		
def get_locations():
	return db.session.query(Locations.id, Locations.name).all()

def update_temprecords():
	
	timespan = datetime.utcnow() - timedelta(hours=24)
	
	# Update max/min temps from last 24 hours
	for i in range(1,6):
		loc = db.session.query(TempHistory.temp)\
		.filter(TempHistory.location_id == i, (TempHistory.date > timespan)).all()
		
		cur = db.session.query(TempCurrent).filter(TempCurrent.location_id == i).first()
		
		if loc:
			cur.tmax = max(loc)
			cur.tmin = min(loc)
			db.session.commit()
		else:
			cur.tmax = cur.tcurrent
			cur.tmin = cur.tcurrent
			db.session.commit()
	
if __name__ == "__main__":
	app.run()
	
