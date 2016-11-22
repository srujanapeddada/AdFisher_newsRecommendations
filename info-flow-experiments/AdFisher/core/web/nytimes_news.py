import time, re
import sys
from selenium import webdriver
from datetime import datetime
import google_ads
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

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
	valid_categories = ['World', 'U.S.', 'Politics', 'Business',
			    'Opinion', 'Tech', 'Science', 'Health',
			    'Sports', 'Arts', 'Style', 'Food', 'Travel']

	categoryTab = self.driver.find_element_by_css_selector('ul.mini-navigation-menu')
	print ("Element found")


	# check to make sure the category is valid
	if (category in valid_categories):
	    # Go to the page that serves the category
	    categoryLink = categoryTab.find_element_by_partial_link_text(category)
	    print ("Clicking on the link")
	    print (categoryLink.get_attribute("innerHTML"))

	    categoryLink.click()
	    time.sleep (5)

	    visitedLinks = []
	    index = 0

	    # makes sure we visit at most count number of pages
	    for visited in range (0, count):
		self.driver.execute_script ("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3)
		# searches for links on the page
	        searchLinks = self.driver.find_elements_by_partial_link_text(keyword.title())	
		print ("links in unit: ", len(searchLinks))
		# if no links found then break out of the loop
		if (len(searchLinks) == 0): 
		    print ("No Links found on: ", keyword)
		    break
		# for each of the links found

		if (index < len(searchLinks)):
		    searchLinks[index].click()
		    index += 1
		    time.sleep(time_on_site)
		    site = self.driver.current_url
		    print ("Site: ", site)
		    self.log('treatment', 'read_news', site)
		    # Go back to the previous page
		    self.driver.back()

    def get_recommendedStories (self):
        self.driver.set_page_load_timeout (60)
        self.driver.get ('http://www.nytimes.com/')
	tim = str(datetime.now())


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
