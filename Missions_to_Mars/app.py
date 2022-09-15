# import dependencies
from flask import Flask, render_template, redirect
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
    data = db.mars.find_one()
    
    return render_template("index.html", data=data)

# create scrape route
@app.route("/scrape")
def scrape_func():
    scraped_data = scrape.scrape()

    # db.mars.insert_one(scraped_data)
    db.mars.update_one({}, {"$set": scraped_data}, upsert=True)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)