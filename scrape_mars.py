# import necessary libraries
from flask import Flask, render_template
import pymongo

from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # set path to chromedriver
    executable_path = {"executable_path": "C:chromedrv/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_mars():
    browser = init_browser()

    # Visit Mars News site
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)

    time.sleep(1)

    # set variables for scraping news
    html_news = browser.html
    soup_news = bs(html_news, 'html.parser')

    # Retrieve elements that contain News information
    result_news = soup_news.find('li', class_='slide')

    # Retrieve latest News Title and Paragraph Text      
    news_title = result_news.find('div', class_='content_title').text.strip()
    news_p = result_news.find('div', class_='rollover_description_inner').text.strip()

    # create dictionary containing scraped data
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p
    }

    # close weather data site
    browser.quit()

    return mars_data