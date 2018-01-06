from flask import Flask, flash, redirect, render_template, request, session, url_for
from collections import namedtuple

app = Flask(__name__)

Location = namedtuple("Location", "name lat lon low high current")

@app.route("/")
def index():
	locations = []
	locations.append(Location("Tokio", 35.6584421, 139.7328635, 0, 0, 0))
	locations.append(Location("Helsinki", 60.1697530, 24.9490830, 0, 0, 0))
	return render_template("index.html", locations=locations)
	
@app.route("/about")
def about():
    return "TODO"
    
@app.route("/more")
def more():
    return "TODO"
    
@app.route("/add")
def add():
    return "TODO"
	
if __name__ == "__main__":
	app.run()
	
