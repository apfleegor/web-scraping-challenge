# import dependencies
from flask import Flask, render_template, redirect
import scrape_mars
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

    # query mongo database
    data = db.mars.find_one()
    
    # pass data into html template
    return render_template("index.html", data=data)

# create scrape route
@app.route("/scrape")
def scrape_func():

    # scrape the data using the scrape function from scrape_mars.py
    scraped_data = scrape_mars.scrape()

    # put the scraped data into the database
    db.mars.update_one({}, {"$set": scraped_data}, upsert=True)

    # redirect back to the home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)