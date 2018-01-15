from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from datetime import datetime, timedelta
import os
from flask_sqlalchemy import SQLAlchemy

import psycopg2

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *

@app.route("/")
def index():
	update_temprecords()
	loc = db.session.query(Locations.name, TempCurrent.tmin, TempCurrent.tmax,\
	TempCurrent.tcurrent, TempCurrent.date).join(TempCurrent, Locations.id == TempCurrent.location_id).all()
	return render_template("index.html", loc=loc)
	
@app.route("/about")
def about():
    return "TODO"
    
@app.route("/more", methods=["GET", "POST"])
def more():
	if request.method == "GET":
		return render_template("more.html", loc=get_locations())
	else:
		loc = request.form.get("location")
		if loc == None:
			return "ERROR, no location"
		days = request.form.get("days")
		if days == None:
			return "ERROR, no days"
		days = int(days)
		
		timespan = datetime.utcnow() - timedelta(days=days)
			
		data = db.session.query(TempHistory).filter(TempHistory.location_id == loc, TempHistory.date > timespan).all()
		return render_template("more.html", loc=get_locations(), data=data)
    
@app.route("/add", methods=["GET", "POST"])
def add():
	if request.method == "GET":
		return render_template("add.html", loc=get_locations())
	else:
		temp = request.form.get("temp")
		loc = request.form.get("location")
		if temp == None:
			return "ERROR, no temperature"
		elif loc == None:
			return "ERROR, no location"
		
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
	app.run(debug=True)
	
