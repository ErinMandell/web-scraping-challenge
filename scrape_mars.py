# ****************************************
# import necessary libraries
# *****************************************

from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


# *********************************************
# Define functions and set path to chromedriver
# ***********************************************

def init_browser():
    executable_path = {"executable_path": "C:/chromedrv/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    
    # *************** GET MARS NEWS ***********************************
    # *****************************************************************
    # Initialize browser, set variables, scrape latest news report and
    # return desired text, close browser

    browser = init_browser()
    mars = {}

    url_news = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url_news)

    time.sleep(1)

    html = browser.html
    soup_news = bs(html, "html.parser")

    result_news = soup_news.find('li', class_='slide')

    news_title = result_news.find('div', class_='content_title').text.strip()
    news_p = result_news.find('div', class_='rollover_description_inner').text.strip()

    browser.quit()


    # *************** GET WEATHER REPORT FROM TWITTER *****************************
    # ******************************************************************************
    # start new browser session for next scrape, set variables, scrape latest weather report and
    # return desired text, close browser
    
    browser = init_browser()

    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)

    time.sleep(1)

    html = browser.html
    soup_weather = bs(html, "html.parser")

    mars_weather = soup_weather.find('div', class_='js-tweet-text-container').find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text.split('pic')[0]

    browser.quit()


    # ************** GET FACTS TABLE ********************************************
    # ***************************************************************************
    # start new browser session for next scrape, set variables, scrape facts table
    # use time.sleep when clicking through screens to allow rendering to complete
    # scrape paragraph just for fun
    # close browser
        
    browser = init_browser()

    url_facts = "https://space-facts.com/mars/"
    browser.visit(url_facts)

    time.sleep(1)

    tables = pd.read_html(url_facts)

    df = tables[0]
    df.columns = ['Description','Data']

    table = df.set_index('Description')
    mars_table = table.to_html()

    html_description = browser.html

    soup_description = bs(html_description, 'html.parser')

    mars_description = soup_description.find('div', class_='entry-content').find('p')

    mars_d = str(mars_description).replace('<a href="https://space-facts.com/the-sun/">', '').replace('<a href="https://space-facts.com/terrestrial-planets/">', '').replace('</a>', '').strip('<p>').strip('</')

    browser.quit()


    # ************ GET FULL SIZE IMAGE *****************************************
    # **************************************************************************
    # start new browser session for next scrape, set variables, scrape image file
    # use time.sleep to allow page to render before clicking through and scraping
    # build url and pass to variable
    # close browser
        
    browser = init_browser()

    url_full_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url_full_image)
    time.sleep(1)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    html_full_image = browser.html
    
    soup_full_image = bs(html_full_image, 'html.parser')

    result_full_image = soup_full_image.find('img', class_='main_image')['src']

    url = 'https://www.jpl.nasa.gov'      
    mars_image_url = url + result_full_image

    browser.quit()


    # ************ MARS HEMISPHERES **********************************************
    # *****************************************************************************
    # start new browser session for next scrape
    # use time.sleep to allow page to render before clicking through and scraping
    # use browser.back function to navigate back to previous page in order to click on next image
    # scrape image files and return to variables
    # close browser
    
    browser = init_browser()

    # ------ First Image -------
    url_first_image = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_first_image)

    time.sleep(2)

    browser.click_link_by_partial_text('Cerberus')

    html_first_image = browser.html

    soup_first_image = bs(html_first_image, 'html.parser')

    result_first_image = soup_first_image.find('div', class_='downloads')   
    first_image = result_first_image.find('a')['href']

    browser.back()
    time.sleep(1)

    # ------ Second Image ------
    browser.click_link_by_partial_text('Schiaparelli')

    html_second_image = browser.html

    soup_second_image = bs(html_second_image, 'html.parser')

    result_second_image = soup_second_image.find('div', class_='downloads')     
    second_image = result_second_image.find('a')['href']

    browser.back()
    time.sleep(1)

    # ------ Third Image ------
    browser.click_link_by_partial_text('Syrtis')

    html_third_image = browser.html

    soup_third_image = bs(html_third_image, 'html.parser')

    result_third_image = soup_third_image.find('div', class_='downloads')     
    third_image = result_third_image.find('a')['href']

    browser.back()
    time.sleep(1)

    # ------ Fourth Image ------
    browser.click_link_by_partial_text('Valles')

    html_fourth_image = browser.html

    soup_fourth_image = bs(html_fourth_image, 'html.parser')

    result_fourth_image = soup_fourth_image.find('div', class_='downloads')     
    fourth_image = result_fourth_image.find('a')['href']

    browser.quit()


    # ***********   CREATE DICTIONARY WITH ALL SCRAPED INFORMATION **************
    # ****************************************************************************
    # Assign each variable to a key
    # Dictionary to be passed to the app.py file to create the mongoDB, and to the index file using jinja

    mars = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "mars_weather": mars_weather,
        "mars_table": mars_table,
        "mars_d": mars_d,
        "mars_image": mars_image_url,
        "mars_hemi_one": first_image,
        "mars_hemi_two": second_image,
        "mars_hemi_three": third_image,
        "mars_hemi_four": fourth_image
    }

    return mars

