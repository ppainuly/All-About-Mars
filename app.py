# Import Dependencies 
from flask import Flask, render_template
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

    # Run scrapped functions
    # mars_dict = scrape_news()
    # mars_dict = scrape_jpl()   
    # mars_dict = mars_facts()
    # mars_dict = mars_hemisphere()
    mars_data = scrape_mars.scrape_all()
    #b.collection.update({}, mars_data, upsert=True)
    db.mars_info.insert_one(mars_data)

    pprint.pprint(mars_data)
    return "Scrapping Mars Data..."

@app.route("/")
def home():
    #data = list(db.mars_info.find())
    data = {'featured_image': 'https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA17793-1920x1200.jpg',
 'hemisphere_img_url': [{'img_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg',
                         'title': 'Cerberus Hemisphere Enhanced'},
                        {'img_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg',
                         'title': 'Schiaparelli Hemisphere Enhanced'},
                        {'img_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg',
                         'title': 'Syrtis Major Hemisphere Enhanced'},
                        {'img_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg',
                         'title': 'Valles Marineris Hemisphere Enhanced'}],
 'mars_facts': '<table border="1" class="dataframe">\n'
               '  <thead>\n'
               '    <tr style="text-align: right;">\n'
               '      <th></th>\n'
               '      <th>Values</th>\n'
               '    </tr>\n'
               '    <tr>\n'
               '      <th>Description</th>\n'
               '      <th></th>\n'
               '    </tr>\n'
               '  </thead>\n'
               '  <tbody>\n'
               '    <tr>\n'
               '      <th>Equatorial Diameter:</th>\n'
               '      <td>6,792 km</td>\n'
               '    </tr>\n'
               '    <tr>\n'
               '      <th>Polar Diameter:</th>\n'
               '      <td>6,752 km</td>\n'
               '    </tr>\n'
               '    <tr>\n'
               '      <th>Mass:</th>\n'
               '      <td>6.39 × 10^23 kg (0.11 Earths)</td>\n'
               '    </tr>\n'
               '    <tr>\n'
               '      <th>Moons:</th>\n'
               '      <td>2 (Phobos &amp; Deimos)</td>\n'
               '    </tr>\n'
               '    <tr>\n'
               '      <th>Orbit Distance:</th>\n'
               '      <td>227,943,824 km (1.38 AU)</td>\n'
               '    </tr>\n'
               '    <tr>\n'
               '      <th>Orbit Period:</th>\n'
               '      <td>687 days (1.9 years)</td>\n'
               '    </tr>\n'
               '    <tr>\n'
               '      <th>Surface Temperature:</th>\n'
               '      <td>-87 to -5 °C</td>\n'
               '    </tr>\n'
               '    <tr>\n'
               '      <th>First Record:</th>\n'
               '      <td>2nd millennium BC</td>\n'
               '    </tr>\n'
               '    <tr>\n'
               '      <th>Recorded By:</th>\n'
               '      <td>Egyptian astronomers</td>\n'
               '    </tr>\n'
               '  </tbody>\n'
               '</table>',
 'news_paragraph': 'Through Nov. 1, K-12 students in the U.S. are encouraged '
                   "to enter an essay contest to name NASA's next Mars rover.",
 'news_title': 'NASA Invites Students to Name Mars 2020 Rover'}
    return render_template("index.html", data = data)

#for key,values in d.items():
#    print("")
#    print(key)
#    print(values)
#    print("")