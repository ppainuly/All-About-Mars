# Import Modules
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 
from urllib.parse import urlparse

mars_dict = {}

# Set Chromedriver local path
chromedriver_url = '/usr/local/bin/chromedriver'

def init_browser(): 

    executable_path = {'executable_path': chromedriver_url}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
# Assign the text to variables that you can reference later
def scrape_news():
    
    try:
        browser = init_browser()

        # Set up url in browser
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        
        # Reading the html page
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        # Get title and description
        news_title = soup.find("div",class_="content_title").text
        news_p = soup.find("div", class_="article_teaser_body").text

        print(f"News Title : {news_title}")
        print(f"News Paragraph : {news_p}")

        browser.quit()

    except Exception as e:
        print("ERROR : " + str(e))
        return

scrape_news()