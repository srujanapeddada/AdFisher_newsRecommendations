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

class BbcNewsUnit (google_ads.GoogleAdsUnit):

    def __init__ (self, browser, log_file, unit_id, treatment_id, headless=False, proxy= None):
        google_ads.GoogleAdsUnit.__init__(self, browser, log_file, unit_id, treatment_id, headless, proxy=proxy)

    def get_recommendedStories (self):
        # Get the recommended stories from BBC
        self.driver.set_page_load_timeout (60)
        self.driver.get ("http://www.bbc.com/")
        tim = str (datetime.now())
       
	recomms = self.driver.find_element_by_xpath (".//div[@class='slick-list draggable']/div")
	articles = recomms.find_elements_by_tag_name ('li')
	for article in articles:
	    title = article.find_element_by_xpath(".//div[@class='media__content']/h3/a").get_attribute('innerHTML')
            title = title.strip()
            agency = "BBC"
            ago = "0 minutes ago"
            body = article.find_element_by_xpath(".//div[@class='media__content']/a").get_attribute('innerHTML')
	    heading = "Recommended"
	    news = strip_tags(tim+"@|"+heading+"@|"+title+"@|"+agency+"@|"+ago+"@|"+body).encode("utf8")
            self.log('measurement', 'news', news)         


    def get_news (self,type, reloads, delay):
        rel = 0
        while (rel < reloads):  # number of reloads on sites to capture all ads
            time.sleep(delay)
    #       try:
            for i in range(0,1):
                s = datetime.now()
                if(type == 'bbc'):
                    self.get_recommendedStories()
                else:
                    raw_input("No such site found: %s!" % site)
                e = datetime.now()
                self.log('measurement', 'loadtime', str(e-s))
    #       except:
    #           log('errorcollecting', id, LOG_FILE)
    #           pass
            rel = rel + 1




