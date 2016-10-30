import time, re
import sys
from selenium import webdriver
from datetime import datetime
import google_ads
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
	    tim = str(datetime.now())


	    self.driver.execute_script ("window.scrollTo(0, document.body.scrollHeight);")
	    time.sleep(3)

	    recomms = self.driver.find_element_by_xpath ("//*[@id='recommendations']/div[5]")

	    headlines = recomms.find_elements_by_class_name('headline')
	    for headline in headlines:
		    title = (headline.get_attribute("innerHTML"))
            agency = "NYTimes"
            ago = "0 minutes ago"
            body = ""
            heading = "Recommended"
            news = strip_tags (tim+"@|"+heading+"@|"+title+"@|"+agency+"@|"+ago+"@|"+body).encode("utf8")
            self.log('measurement', 'news', news)



