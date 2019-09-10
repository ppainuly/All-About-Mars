# Import Dependencies 
from flask import Flask,redirect, render_template
import pymongo
import scrape_mars
import pprint

# Create an instance of Flask app
app = Flask(__name__)



# Set up Mongo Connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db
db.mars_info.drop()


@app.route("/scrape")
def scrape(): 
    db.mars_info.drop()
    mars_data = scrape_mars.scrape_all()
    db.mars_info.insert_one(mars_data)

    pprint.pprint(mars_data)
    return redirect("/", code=302)

@app.route("/")
def home():
    mars_data = list(db.mars_info.find())
    pprint.pprint(mars_data)
    return render_template("index.html", data = mars_data)

if __name__ == "__main__": 
    app.run(debug= True)
