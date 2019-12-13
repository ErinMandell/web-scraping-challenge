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

    # convert table to dataframe and then to html
    df = tables[0]
    df.columns = ['Description','Data']

    table = df.set_index('Description')
    mars_table = table.to_html()

    # grab Mars Description paragraph
    # HTML object
    html_description = browser.html

    # Parse HTML
    soup_description = bs(html_description, 'html.parser')

    # Retrieve elements
    mars_description = soup_description.find('div', class_='entry-content').find('p')

    mars_d = str(mars_description).replace('<a href="https://space-facts.com/the-sun/">', '').replace('<a href="https://space-facts.com/terrestrial-planets/">', '').replace('</a>', '').strip('<p>').strip('</')

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

    # close image site
    browser.quit()


# ************ MARS HEMISPHERES **********************************************
    
    # start new browser session for next scrape
    browser = init_browser()

    # Visit NASA site for image scrape
    url_first_image = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_first_image)

    time.sleep(2)

    #Click image #1
    browser.click_link_by_partial_text('Cerberus')

    # HTML object
    html_first_image = browser.html

    # Parse HTML
    soup_first_image = bs(html_first_image, 'html.parser')

    # Retrieve elements
    result_first_image = soup_first_image.find('div', class_='downloads')   
    first_image = result_first_image.find('a')['href']

    # go back to main Mars Hemisphere page and wait for it to render
    browser.back()
    time.sleep(1)

    #Click image #2
    browser.click_link_by_partial_text('Schiaparelli')

    # HTML object
    html_second_image = browser.html

    # Parse HTML
    soup_second_image = bs(html_second_image, 'html.parser')

    # Retrieve desired elements
    result_second_image = soup_second_image.find('div', class_='downloads')     
    second_image = result_second_image.find('a')['href']

    # go back to main Mars Hemisphere page and wait for it to render
    browser.back()
    time.sleep(1)

    #Click image #3
    browser.click_link_by_partial_text('Syrtis')

    # HTML object
    html_third_image = browser.html

    # Parse HTML
    soup_third_image = bs(html_third_image, 'html.parser')

    # Retrieve desired elements
    result_third_image = soup_third_image.find('div', class_='downloads')     
    third_image = result_third_image.find('a')['href']

    # go back to main Mars Hemisphere page and wait for it to render
    browser.back()
    time.sleep(1)

    #Click image #4
    browser.click_link_by_partial_text('Valles')

    # HTML object
    html_fourth_image = browser.html

    # Parse HTML
    soup_fourth_image = bs(html_fourth_image, 'html.parser')

    # Retrieve desired elements
    result_fourth_image = soup_fourth_image.find('div', class_='downloads')     
    fourth_image = result_fourth_image.find('a')['href']

    # go back to main Mars Hemisphere page and wait for it to render
    browser.quit()

    # create dictionary containing scraped data
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

