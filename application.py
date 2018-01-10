from flask import Flask, flash, redirect, render_template, request, session, url_for, g
import os
import sqlite3

app = Flask(__name__)
app.database = "website.db"
app.secret_key = "topsecret"

@app.route("/")
def index():
	try:
		g.db = connect_db()
		cur = g.db.execute("""SELECT name, tmin, tmax, tcurrent FROM Location 
		JOIN CurrentTemperatures ON Location.id = location_id""")
		loc = [dict(name=row[0], tmin=row[1], tmax=row[2], tcur=row[3]) for row in cur.fetchall()]
		g.db.close()
		return render_template("index.html", loc=loc)
	except:
		return "Database not working"
	
@app.route("/about")
def about():
    return "TODO"
    
@app.route("/more", methods=["GET", "POST"])
def more():
	if request.method == "GET":
		return render_template("more.html", loc=list_countries())
	else:
		loc = request.form.get("location")
		if loc == None:
			return "ERROR, no location"
			
		g.db = connect_db()
		cur = g.db.execute("""SELECT * FROM Temperatures WHERE location_id = ?""", loc)
		data = [dict(temp=row[2],date=row[3]) for row in cur.fetchall()]
		g.db.close()
		return render_template("more.html", loc=list_countries(), data=data)
    
@app.route("/add", methods=["GET", "POST"])
def add():
	if request.method == "GET":
		return render_template("add.html", loc=list_countries())
	else:
		temp = request.form.get("temp")
		loc = request.form.get("location")
		if temp == None:
			return "ERROR, no temperature"
		elif loc == None:
			return "ERROR, no location"
		
		g.db = connect_db()
		g.db.execute("""INSERT INTO Temperatures (location_id, temperature) VALUES (?,?)""", (temp, loc))
		g.db.execute("""UPDATE CurrentTemperatures SET tcurrent = ? WHERE location_id = ?""",(temp, loc)) 
		
		cur = g.db.execute("""SELECT tmax, tmin FROM CurrentTemperatures WHERE location_id = ?""", loc)
		records = cur.fetchall()
		
		if float(temp) > float(records[0][0]):
			g.db.execute("""UPDATE CurrentTemperatures SET tmax = ? WHERE location_id = ?""", (temp, loc))
		elif float(temp) < float(records[0][1]):
			g.db.execute("""UPDATE CurrentTemperatures SET tmin = ? WHERE location_id = ?""", (temp, loc))
		return render_template("add.html", loc=list_countries())
	
def connect_db():
	return sqlite3.connect(app.database, isolation_level=None)
	
def list_countries():
	g.db = connect_db()
	cur = g.db.execute("""SELECT id, name FROM LOCATION""")
	loc = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
	g.db.close()
	return loc
	
if __name__ == "__main__":
	app.run(debug=True)
	
