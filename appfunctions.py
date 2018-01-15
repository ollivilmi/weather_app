from app import db
from datetime import datetime, timedelta
from models import *

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