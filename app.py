from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
# Use PyMongo to establish Mongo connection
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars = mongo.db.mars.find_one()
    print(mars)
    # Return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    # Run the scrape function
    mars=mongo.db.mars
    data = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mars.update({}, data, upsert=True)
    # Redirect back to home page
    return redirect("http://localhost:5000", code=302)

if __name__ == "__main__":
    app.run(debug=True)
