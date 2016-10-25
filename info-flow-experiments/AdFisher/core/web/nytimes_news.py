import time, re
import sys
from selenium import webdriver
from datetime import datetime
import google_ads


from HTMLParser import HTMLParser

class MLStripper (HTMLParser):
    def __init__ (self):
	self.reset ()
        self.fed = []
    
    def handle_data (self, d):
	self.fed.append(d)
    
    def get_data (self):
	return ''.join(self.fed)

def strip_tags (html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class NYTNewsUnit (google_ads.GoogleAdsUnit):

    def __init__ (self, browser, log_file, unit_id, treatment_id, headless=False, proxy = None):
	google_ads.GoogleAdsUnit.__init__(self,browser,log_file,unit_id, treatment_id, headless, proxy=proxy)

    def get_recommendedStories (self):
        self.driver.set_page_load_timeout (60)
        self.driver.get ('http://www.nytimes.com/')
	time = str(datetime.now())

	recomms = self.driver.find_element_by_xpath ("//*[@id='recommendations']/div[5]")
	print (recomms.get_attribute("class"))
	headlines = recomms.find_elements_by_tag_name ("li")
	print (len(headlines))
	for headline in headlines:
	    print ("Headline: " + headline.get_attribute())
   
 
