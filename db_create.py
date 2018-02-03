from app import db
from models import Locations, TempHistory
from datetime import datetime

#create
db.create_all()

#insert
db.session.add_all([Locations('Tokio', 35.6584421, 139.7328635), Locations('Helsinki', 60.1697530,24.9490830),
Locations('New York', 40.7406905,-73.9938438), Locations('Amsterdam', 52.3650691,4.9040238), Locations('Dubai', 25.092535,55.1562243)])

db.session.add_all([TempHistory(1,0),TempHistory(2,0),TempHistory(3,0),TempHistory(4,0),TempHistory(5,0)])

#commit
db.session.commit()