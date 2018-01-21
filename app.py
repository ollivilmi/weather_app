from flask import Flask, flash, redirect, render_template, request, session, url_for, g, jsonify
from datetime import datetime, timedelta
import os
import re
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_jsglue import JSGlue
import psycopg2

app = Flask(__name__)
JSGlue(app)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *

# Opening the main page updates and shows a table of min/max temperatures during the last 24 hours
@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "GET":
		update_temprecords(24)
	else:
		for i in range (1, 6):
			for j in range (0, 10):
				add_temperature(round(random.uniform(-25, 35), 2), i)
			
	loc = db.session.query(Locations.name, TempCurrent.tmin, TempCurrent.tmax,\
	TempCurrent.tcurrent, TempCurrent.date).join(TempCurrent, Locations.id == TempCurrent.location_id).all()
	return render_template("index.html", loc=loc)
	
@app.route("/about")
def about():
		return render_template("about.html", loc=get_locations())
    
@app.route("/history")
def history():
	return render_template("history.html", loc=get_locations())
		
# Returns temp history for a location filtered by amount of days
@app.route("/gethistory")
def gethistory():
	loc = request.args.get("loc")
	null_check(loc, "location")	
	days = request.args.get("days")
	null_check(days, "days")

	days = int(days)
	
	timespan = datetime.utcnow() - timedelta(days=days)
		
	data = db.session.query(TempHistory).filter(TempHistory.location_id == loc, TempHistory.date > timespan).all()
	history = [dict(temp=row.temp,date=row.date) for row in data]
	
	return jsonify(history)

# Gets up to 10 of the latest temperatures for a given location. Script uses this to build a temperature graph
@app.route("/getlocation")
def getlocation():
	loc = request.args.get("loc")
	null_check(loc, "location")
	lim = request.args.get("lim")
	null_check(lim, "limit")
		
	data = db.session.query(TempHistory).filter(TempHistory.location_id == loc).order_by(TempHistory.date.desc()).limit(lim).all()
	temps = [dict(temp=row.temp, date=row.date) for row in data]
	
	return jsonify(temps)

# From the 24 hrs max, min and avg for a location.
@app.route("/getrecords")
def getrecords():
	loc = request.args.get("loc")
	null_check(loc, "location")

	timespan = datetime.utcnow() - timedelta(hours=24)

	temps = db.session.query(
	func.max(TempHistory.temp),
	func.min(TempHistory.temp),
	func.avg(TempHistory.temp)).filter(TempHistory.location_id == loc,
	TempHistory.date > timespan).all()

	ctemp = db.session.query(TempCurrent.tcurrent).filter(TempCurrent.location_id == loc).all()
	
	records = {"max":temps[0][0], "min":temps[0][1], "avg":temps[0][2], "new":ctemp}

	return jsonify(records)

# User can add new temperatures via the POST method
@app.route("/add", methods=["GET", "POST"])
def add():
	if request.method == "POST":
		temp = request.form.get("temp")
		loc = request.form.get("location")
		null_check(temp, "temperature")
		null_check(loc, "location")
		add_temperature(temp, loc)
		
	return render_template("add.html", loc=get_locations())
		
# Used for building the drop down menus for locations
def get_locations():
	return db.session.query(Locations.id, Locations.name).all()

def null_check(argument, name):
	if argument == None:
		raise RunTimeError(name + " missing")

# Checks the database for the records during the last 24 hours and updates them to the CurrentTemps table.
# This is called when the index page is opened.
def update_temprecords(h):
	
	timespan = datetime.utcnow() - timedelta(hours=h)
	
	# Update max/min temps from last 24 hours
	for i in range(1,6):
		loc = db.session.query(TempHistory.temp)\
		.filter(TempHistory.location_id == i, (TempHistory.date > timespan)).all()
		
		cur = db.session.query(TempCurrent).filter(TempCurrent.location_id == i).first()
		
		if loc:
			cur.tmax = max(loc)
			cur.tmin = min(loc)
		else:
			cur.tmax = cur.tcurrent
			cur.tmin = cur.tcurrent
		db.session.commit()

def add_temperature(temp, loc):
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
	
if __name__ == "__main__":
	app.run()
	
