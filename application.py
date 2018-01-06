from flask import Flask, flash, redirect, render_template, request, session, url_for
from collections import namedtuple
import os
from urllib import parse
import psycopg2

app = Flask(__name__)

# Setup database
parse.uses_netloc.append("postgres")
url = parse.urlparse(os.environ["postgres://mbtlbohgmwqgti:df8e78a5a6a5f8f55450a64dd28bd4a909616699155483c3fa1b8645fcdc0711@ec2-107-22-183-40.compute-1.amazonaws.com:5432/dfs76spenfdagp"])
Location = namedtuple("Location", "name lat lon low high current")
conn = psycopg2.connect(
	database=url.path[1:],
	user=url.username,
	password=url.password,
	host=url.hostname,
	port=url.port
)

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
	
