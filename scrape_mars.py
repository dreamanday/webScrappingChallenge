
# Dependencies
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
from twitter_scraper import get_tweets
import re
import pandas as pd
import pymongo

def scrape_mars():

    # News

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    response = response.text
    soup = bs(response, 'html.parser')

    titles = soup.find_all('div', class_='content_title')
    title1 = titles[0].a.text.replace('\n','')

    p = soup.find_all('div', class_='rollover_description_inner')
    p1 = p[0].text.replace('\n','')

    # Images

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    html = browser.html
    soup2 = bs(html, "html.parser")

    image = soup2.find('div', class_='carousel_container')
    image = image.article['style']
    image = image.replace("background-image: url('","https://www.jpl.nasa.gov")
    image = image.replace("');","")

    # Weather

    dict=[]
    for tweet in get_tweets('MarsWxReport', pages=1):
        if re.search('InSight sol.+',tweet['text']):
            dict.append(tweet)

    temp = dict[0]['text']

    # Facts

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    facts = tables[0]

    # Hemispheres

    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    browser.click_link_by_partial_text("Cerberus Hemisphere Enhanced")
    html = browser.html
    soup3 = bs(html, "html.parser")
    cerberus_img = soup3.find('li')
    cerberus_img = cerberus_img.a['href']
    cerberus_title = soup3.find('title')
    cerberus_title = cerberus_title.text

    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    browser.click_link_by_partial_text("Schiaparelli Hemisphere Enhanced")
    html = browser.html
    soup3 = bs(html, "html.parser")
    schiaparelli_img = soup3.find('li')
    schiaparelli_img = schiaparelli_img.a['href']
    schiaparelli_title = soup3.find('title')
    schiaparelli_title = schiaparelli_title.text

    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    browser.click_link_by_partial_text("Syrtis Major Hemisphere Enhanced")
    html = browser.html
    soup3 = bs(html, "html.parser")
    syrtis_img = soup3.find('li')
    syrtis_img = syrtis_img.a['href']
    syrtis_title = soup3.find('title')
    syrtis_title = syrtis_title.text

    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')
    browser.click_link_by_partial_text("Valles Marineris Hemisphere Enhanced")
    html = browser.html
    soup3 = bs(html, "html.parser")
    valles_img = soup3.find('li')
    valles_img = valles_img.a['href']
    valles_title = soup3.find('title')
    valles_title = valles_title.text

    hemisphere_image_urls=[
        {'title':cerberus_title, 'img_url': cerberus_img},
        {'title':schiaparelli_title, 'img_url': schiaparelli_img},
        {'title':syrtis_title, 'img_url': syrtis_img},
        {'title':valles_title, 'img_url': valles_img}
    ]

    # Results

    results={
    'dict1': {'key':'news', 'title': title1, 'teaser': p1},
    'dict2': {'key':'image', 'image': image},
    'dict3': {'key':'weather', 'temp': temp},
    'dict4': {'key':'facts', 'facts': f'''{facts}'''},
    'dict5': {'key':'hemispheres', 'facts': hemisphere_image_urls}
 }

    return results
