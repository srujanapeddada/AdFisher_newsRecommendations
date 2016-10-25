import time, re
import sys
from selenium import webdriver
from datetime import datetime
import google_ads
import google_search

# strip html
from HTMLParser import HTMLParser

class MLStripper (HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data (self, d):
        self.fed.append(d)
    def get_data (self):
        return ''.join (self.fed)

def strip_tags (html):
    s= MLStripper()
    s.feed (html)
    return s.get_data()

class CnnNewsUnit (google_ads.GoogleAdsUnit):

    def __init__ (self, browser, log_file, unit_id, treatment_id, headless=False, proxy= None):
        google_ads.GoogleAdsUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)

    def get_recommendedStories (self):
        # Get the recommended stories from CNN
        self.driver.set_page_load_timeout (60)
        self.driver.get ("http://www.cnn.com/")
        time = str (datetime.now())
       
	recomms = self.driver.find_element_by_xpath ("//*[@id='outbrain_widget_1']/div/ul")
	articles = recomms.find_elements_by_tag_name ('li')
	for article in articles:
	    temp = article.find_element_by_tag_name ('a')
	    title = temp.get_attribute ('title')
	    heading = "Recommended"
	    news = strip_tags (time+"@|"+heading+"@|"+title).encode("utf8")
	    self.log ('measurement', 'news', news)




