from flask import Flask, flash, redirect, render_template, request, session, url_for, g, jsonify
from datetime import datetime, timedelta
import os
import re
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_jsglue import JSGlue
from statistics import mean

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
	null_check(loc, "location")
		
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
	null_check(loc, "location")
		
	data = db.session.query(TempHistory).filter(TempHistory.location_id == loc).order_by(TempHistory.date.desc()).limit(10).all()
	temps = [dict(temp=row.temp, date=row.date) for row in data]
	
	return jsonify(temps)

@app.route("/getrecords")
def getrecords():
	loc = request.args.get("loc")
	null_check(loc, "location")

	temps = db.session.query(
	func.max(TempHistory.temp),
	func.min(TempHistory.temp),
	func.avg(TempHistory.temp)).filter(TempHistory.location_id == loc).all()
	
	records = {"max":temps[0][0], "min":temps[0][1], "avg":temps[0][2]}

	return jsonify(records)

	
@app.route("/add", methods=["GET", "POST"])
def add():
	if request.method == "GET":
		return render_template("add.html", loc=get_locations())
	else:
		temp = request.form.get("temp")
		loc = request.form.get("location")
		null_check(temp, "temperature")
		null_check(loc, "location")
		
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

def null_check(argument, name):
	if argument == None:
		raise RunTimeError(name + " missing")

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
	
