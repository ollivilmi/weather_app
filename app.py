from flask import Flask, flash, redirect, render_template, request, session, url_for, g, jsonify
from datetime import datetime, timedelta
import os
import re
import random
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_jsglue import JSGlue
import psycopg2
from statistics import mean

app = Flask(__name__)
JSGlue(app)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *

# Opening the main page updates and shows a table of min/max temperatures during the last 24 hours
@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		for i in range (1, 6):
			for j in range (0, 10):
				add_temperature(round(random.uniform(-25, 35), 2), i)
			
	return render_template("index.html")
	
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
	history = []
	i = 1
	
	while True:
		previous_day = datetime.today() - timedelta(days=i)
		current_day = previous_day + timedelta(days=1)

		records = db.session.query(
			func.max(TempHistory.temp),
			func.min(TempHistory.temp),
			func.avg(TempHistory.temp)).filter(
				TempHistory.location_id == loc,
				TempHistory.date > previous_day, 
				TempHistory.date < current_day).all()

		if records[0][0] != None:
			history.append({"max":records[0][0], "min":records[0][1], "avg":records[0][2],
			"date":current_day.isoformat()[0:10]})

		if i == days:
			break
		else:
			i+=1

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

# From the amount of recent tempereratures, get records (min, max, newest) for a location
@app.route("/getrecords")
def getrecords():
	loc = request.args.get("loc")
	null_check(loc, "location")
	lim = request.args.get("lim")
	null_check(lim, "limit")

	timespan = datetime.utcnow() - timedelta(hours=24)

	temps = db.session.query(TempHistory.temp).filter(
		TempHistory.location_id == loc).order_by(
			TempHistory.date.desc()).limit(lim).all()

	ctemp = db.session.query(TempHistory.temp, TempHistory.date).filter(
		TempHistory.location_id == loc).order_by(
		TempHistory.date.desc()).first()

	records = {"max":max(temps), "min":min(temps), "new":ctemp.temp, "date":ctemp.date}

	return jsonify(records)

# Gets temperature records (min, max, avg, newest) for all locations to build a table
@app.route("/getallrecords")
def getallrecords():
	h = request.args.get("hours")
	null_check(h, "hours")

	timespan = datetime.utcnow() - timedelta(hours=int(h))

	records = []
	for i in range(1, 6):
		records.append(db.session.query(
		func.max(TempHistory.temp),
		func.min(TempHistory.temp),
		func.avg(TempHistory.temp)).filter(
		TempHistory.date > timespan, 
		TempHistory.location_id == i).all())

	ctemps = []
	for i in range(1, 6):
		ctemps.append(db.session.query(TempHistory.temp, TempHistory.date)
		.filter(TempHistory.location_id == i)
		.order_by(TempHistory.date.desc()).first())
	
	loc = get_locations()

	table = []
	for i in range(0, 5):
		table.append({"max":records[i][0][0], "min":records[i][0][1], "avg":records[i][0][2], 
		"cur":ctemps[i][0], "date":ctemps[i][1], "loc":loc[i].name})

	return jsonify(table)

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
		raise RuntimeError(name + " missing")

def add_temperature(temp, loc):
	# Check that the temperature is within reasonable limits
	try:
		ftemp = float(temp)
		if (ftemp > 70 or ftemp <-100):
			return
	except:
		return
	db.session.add(TempHistory(loc, temp))
		
	db.session.commit()
	
if __name__ == "__main__":
	app.run()
	
