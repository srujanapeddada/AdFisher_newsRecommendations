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
            agency = "CNN"
	    ago = "0 minutes ago"
            body = article.find_element_by_xpath(".//span[@class='ob_source']/span").get_attribute('innerHTML')
	    heading = "Recommended"
	    news = strip_tags(time+"@|"+heading+"@|"+title+"@|"+agency+"@|"+ago+"@|"+body).encode("utf8")
            self.log('measurement', 'news', news) 

    def read_CNN_articles (self, count=5, keyword=None, category=None, time_on_site=20):
	self.driver.set_page_load_timeout (60)
	valid_categories = ['us', 'world', 'politics', 'money', 'opinion', 'health', 
                            'entertainment', 'style' 'travel', 'sports']

	if (category.lower() in valid_categories):
	    url = "http://www.cnn.com/" + category.lower()
	else:
	    url = "http://www.cnn.com/"

	self.driver.get (url)
	tim = str (datetime.now())
	
	i = 0

	for i in range (0, count):
	    links = []
	    if (keyword != None):
		print (len(self.driver.find_elements_by_xpath(".//div[@class='cd__content']")))
		print (".//div[@class='cd__content'][contains(text(),'"+keyword+"')]")
		
	        print(len(self.driver.find_elements_by_xpath(".//div[@class='cd__content']/h3/a/span[contains(.,'"+keyword+"')]"))) 
	        links.extend (self.driver.find_elements_by_xpath(".//div[@class='cd__content']/h3/a/span[contains(.,'"+keyword+"')]")) 
	
	    print "links in unit", self.unit_id, "found: ", len (links)

	    if (i>=len(links)):
	        break

	    # may have to modify to array element
	    print (links[i].get_attribute('innerHTML'))
	    self.driver.execute_script ("return arguments[0].scrollIntoView();", links[i])
	    time.sleep (2)
            links[i].click()	

            for handle in self.driver.window_handles:
	        seld.driver.switch_to.window(handle)
		print self.driver.title()
		time.sleep(time_on_site)
		site = self.driver.current_url
		self.log ('treatment', 'read_news', site)
		self.driver.close()
		self.driver.switch_to.window (self.driver.window_handles[0])

	






