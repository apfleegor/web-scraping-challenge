# import dependencies
from flask import Flask, render_template
import scrape
import pymongo

# create instance of Flask
app = Flask(__name__)

# create connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.scrape_db

# create root route
@app.route("/")
def home():
    data = list(db.mars.find())
    
    return render_template("index.html", data=data)

# create scrape route
@app.route("/scrape")
def scrape_func():
    db.mars.insert_many(scrape())


if __name__ == "__main__":
    app.run(debug=True)