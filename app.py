from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_phone

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars = mongo.db.mars
    mars_app_scrape = scrape_phone.scrape()
    mars.update_one({}, {"$set": mars_app_scrape}, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
