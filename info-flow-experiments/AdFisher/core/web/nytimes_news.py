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

    # Search for articles by category and keyword and click 
    def read_NYT_articles (self, count=5, keyword=None, category=None, time_on_site=20):
        self.driver.set_page_load_timeout (60)
	self.driver.get('http://nytimes.com/')
	valid_categories = ['world', 'national', 'politics', 'sports', 'opinion', 'technology',
			    'science', 'business']

	categoryTab = self.driver.find_element_by_css_selector('ul.mini-navigation-menu')
	print ("Element found")


	# check to make sure the category is valid
	if (category.lower() in valid_categories):
	    # Go to the page that serves the category
	    categoryLink = categoryTab.find_element_by_partial_link_text(category.title())
	    print ("Clicking on the link")
	    print (categoryLink.get_attribute("innerHTML"))

	    categoryLink.click()
	    time.sleep (3)

	    # find all links with the search keyword
	    searchLinks = self.driver.find_elements_by_partial_link_text(keyword.title())	

	    print ("links in unit: ", len(searchLinks))
	    visited = 0
		

	    for link in searchLinks:
		link.click()
	        for handle in self.driver.window_handles:
		    self.driver.switch_to.window(handle)
		    print (self.driver.title())
		    time.sleep(time_on_site)
		    site = self.driver.current_url
		    self.log('treatment', 'read_news', site)
		    self.driver.close()
		    self.driver.switch_to.window (self.driver.window_handles[0])
		visited += 1
		if (visited == count): break

	    



    def get_recommendedStories (self):
        self.driver.set_page_load_timeout (60)
        self.driver.get ('http://www.nytimes.com/')
	tim = str(datetime.now())


	self.driver.execute_script ("window.scrollTo(0, document.body.scrollHeight);")
	time.sleep(3)

	recomms = self.driver.find_element_by_xpath ("//*[@id='recommendations']/div[5]")

	headlines = recomms.find_elements_by_class_name('headline')
	for headline in headlines:
		title1 = (headline.get_attribute("innerHTML"))
		title2 = strip_tags (title1).encode("utf8")
		title3 = title2.strip() 
            	agency = "NYTimes"
            	heading = "Recommended"
            	news = tim+"@|"+heading+"@|"+title3+"@|"+agency+"@|"+"ago"+"@|"+"Body"
            	self.log('measurement', 'news', news)
