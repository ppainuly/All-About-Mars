# Import Modules
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 
from urllib.parse import urlparse
import time

mars_dict = {}

# Set Chromedriver local path
chromedriver_url = '/usr/local/bin/chromedriver'

def init_browser(): 

    executable_path = {'executable_path': chromedriver_url}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

# Scrape all data into a single combined dictionary
def scrape_all():

    try:
        
        mars_dict = scrape_news()
        mars_dict = scrape_jpl()   
        mars_dict = mars_facts()
        mars_dict = mars_hemisphere()
        return mars_dict

    except Exception as e:
        print("ERROR : " + str(e))
        return


# NASA Mars News
# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later
def scrape_news():
    
    try:
        browser = init_browser()

        # Set up url in browser
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        
        # Reading the html page
        html_news = browser.html
        soup = BeautifulSoup(html_news, "html.parser")

        # Get title and description
        news_title = soup.find("div",class_="content_title").text
        news_p = soup.find("div", class_="article_teaser_body").text

        # Store into dictionary
        mars_dict['news_title'] = news_title
        mars_dict['news_paragraph'] = news_p

        browser.quit()
        return mars_dict

    except Exception as e:
        print("ERROR : " + str(e))
        return

# JPL Mars Space Images - Featured Image    
#Visit Jet Propulsion laboratory. Find and save the image url for the current featured Mars Image
def scrape_jpl():
    
    try:
        browser = init_browser()

        # Set up url in browser
        jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
        browser.visit(jpl_url)
        
        # Reading the html page
        jpl_html = browser.html
        soup = BeautifulSoup(jpl_html, "html.parser")
        img_text = soup.find("article", class_="carousel_item")["style"][:]

        # Get image full text url
        import re
        parsed_url = urlparse(jpl_url)
        image_param = re.findall(r"'([^']*)'", img_text)[0]
        image_param

        # Set base url
        base_url = parsed_url.scheme +'://'+ parsed_url.netloc

        # Combine base and image url to get full image url
        featured_image_url = base_url + image_param

        # Store into dictionary
        mars_dict['featured_image'] = featured_image_url

        browser.quit()
        return mars_dict
        

    except Exception as e:
        print("ERROR : " + str(e))
        return

# Mars Facts
# Visit the Mars Facts webpage and scrape the table containing facts about the planet including Diameter, Mass, etc
def mars_facts():

    try:
        browser = init_browser()

        # Set up url in browser
        fact_url = 'https://space-facts.com/mars/'
        browser.visit(fact_url)

        # Read html page table into Pandas dataframe
        mars_facts = pd.read_html(fact_url)

        # Set up Mars Profile dataframe
        mars_facts_df = mars_facts[1]
        mars_facts_df.columns = ["Description", "Values"]
        mars_facts_df = mars_facts_df.set_index(["Description"])

        # Save table as html 
        mars_tbl = mars_facts_df.to_html()

        # Store into dictionary
        mars_dict['mars_facts'] = mars_tbl

        browser.quit()
        return mars_dict

    except Exception as e:
        print("ERROR : " + str(e))
        return

# Mars Hemispheres
# Visit the USGS Astrogeology site to obtain high resolution images for each of Mars's hemispheres. 
# Save image URL and the image in full resolution. Store image url in a dictionary
def mars_hemisphere():

    try:
        browser = init_browser()

        usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(usgs_url)

        # Empty list to store all hemisphere image URL's
        hemisphere_img_url = []
        hemispheres_base_url = 'https://astrogeology.usgs.gov'

        # Open USGS Page and store HTMl
        usgs_html = browser.html
        soup = BeautifulSoup(usgs_html, 'html.parser')

        # Find all Image Item blocks
        hemisphere = soup.find_all('div', class_='item')

        # Store all hemisphere images and title
        for hem in hemisphere:
            
            # Store the title of each Hemisphere Image
            title = hem.find('h3').text
            img_url = hem.find('a')['href']
            
            # open the URL for each image to get full size
            browser.visit(hemispheres_base_url + img_url)
            
            # Store HTMl for Each Image Page
            img_html = browser.html
            soup = BeautifulSoup(img_html, 'html.parser')
            
            # Store URL for full size image by finding image class
            img_full_url = soup.find('img', class_='wide-image')['src']

            # Append title and Image URL to dictionary
            hemisphere_img_url.append({"title" : title, "img_url" : hemispheres_base_url + img_full_url})
            time.sleep(1) 
        # Store into dictionary
        #print(hemisphere_img_url)

        mars_dict['hemisphere_img_url'] = hemisphere_img_url

        browser.quit()
        return mars_dict

    except Exception as e:
        print("ERROR : " + str(e))
        return

d = scrape_all()

for key,values in d.items():
    print("")
    print(key)
    print(values)
    print("")