import time, re
import sys
from selenium import webdriver
from datetime import datetime
import google_ads
import google_search

# strip html
from HTMLParser import HTMLParser

class MLSTripper (HTMLParser):
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
        left_container = self.driver.find_elements_by_class_name("l-container")
        print (len(left_container))
        print (left_container)

