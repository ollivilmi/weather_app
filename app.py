from flask import Flask, flash, redirect, render_template, request, session, url_for, g, jsonify
from datetime import datetime, timedelta
import os
import re
from flask_sqlalchemy import SQLAlchemy
from flask_jsglue import JSGlue
from appfunctions import *

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
	
if __name__ == "__main__":
	app.run()
	
