# import necessary libraries
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # set path to chromedriver
    executable_path = {"executable_path": "C:/chromedrv/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)



def scrape_info():
    
    # *************** MARS NEWS *******************************************

    browser = init_browser()
    mars = {}

    # Visit Mars News Site
    url_news = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url_news)

    time.sleep(1)

    # set variables for scraping news
    html = browser.html
    soup_news = bs(html, "html.parser")

    # Retrieve elements that contain News information
    result_news = soup_news.find('li', class_='slide')

    # Retrieve latest News Title and Paragraph Text      
    news_title = result_news.find('div', class_='content_title').text.strip()
    news_p = result_news.find('div', class_='rollover_description_inner').text.strip()

    # close news data site
    browser.quit()

    # *************** WEATHER REPORT TWITTER *******************************************

    # start new browser session for next scrape
    browser = init_browser()

    # Visit Mars Weather site on twitter
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    time.sleep(1)

    #set variables for scraping weather
    html = browser.html
    soup_weather = bs(html, "html.parser")

    # Retrieve elements that contain Mars Weather information in Twitter
    mars_weather = soup_weather.find('div', class_='js-tweet-text-container').find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text.split('pic')[0]

    # close news data site
    browser.quit()

    # ************** FACTS TABLE ********************************************

    # start new browser session for next scrape
    browser = init_browser()

    # Visit Space Facts site for Mars data
    url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)

    time.sleep(1)

    #set variables for scraping facts table
    tables = pd.read_html(url_facts)

    df = tables[0]
    df.columns = ['Description','Data']

    table = df.set_index('Description')

    mars_table = table.to_html()

    # close data site
    browser.quit()

    # ************ FULL SIZE IMAGE **********************************************
    
    # start new browser session for next scrape
    browser = init_browser()

    # Visit NASA site for image scrape
    url_full_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_full_image)
    time.sleep(1)

    # Click through to desired page
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    # HTML object
    html_full_image = browser.html
    
    # Parse HTML with Beautiful Soup
    soup_full_image = bs(html_full_image, 'html.parser')

    # Retrieve elements that contain Featured Image information
    result_full_image = soup_full_image.find('img', class_='main_image')['src']

    # Isolate src and build URL:
    url = 'https://www.jpl.nasa.gov'      
    mars_image_url = url + result_full_image


    # create dictionary containing scraped data
    mars = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "mars_weather": mars_weather,
        "mars_table": mars_table,
        "mars_image": mars_image_url
    }

    return mars

    # close image site
    browser.quit()
    browser.quit()