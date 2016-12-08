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

class News360NewsUnit (google_ads.GoogleAdsUnit):

    def __init__ (self, browser, log_file, unit_id, treatment_id, headless=False, proxy = None):
			google_ads.GoogleAdsUnit.__init__(self,browser,log_file,unit_id, treatment_id, headless, proxy=proxy)


    def login(self, username, password):
      self.driver.set_page_load_timeout(60)
      self.driver.get('https://www.news360.com')
      categoryTab = self.driver.find_element_by_css_selector('div.eHSignIn_text.mBottom')
      categoryLink = categoryTab.find_element_by_partial_link_text('Sign in with email')
      categoryLink.click()
      time.sleep(3)
      self.driver.find_element_by_id("signinemail").send_keys(username)
      time.sleep(3)
      self.driver.find_element_by_css_selector("input[name='password']").send_keys(password)
      time.sleep(3)
      self.driver.find_element_by_css_selector('button.signin-button[type="submit"]').click()

    def get_news(self):
      self.driver.set_page_load_timeout(60)
      tim = str(datetime.now())

      recomms = self.driver.find_element_by_css_selector('.headlines')

      headlines = recomms.find_elements_by_class_name('headline-card')
      print ("Number of headlines found: ", len(headlines))
      for headline in headlines:
	title1 = (headline.get_attribute("innerHTML"))
	title2 = strip_tags (title1).encode("utf8")
	title3 = title2.strip()
        agency = "News360"
        heading = "Recommended"
        news = tim+"@|"+heading+"@|"+title3+"@|"+agency+"@|"+"ago"+"@|"+"Body"
        self.log('measurement', 'news', news)


    # Search for articles by category and keyword and click
    def read_articles (self, count=5, time_on_site=20):
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
		try:
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
		except:
		    print("finding links on page failed")
		    pass

    def get_recommendedStories (self):
        self.driver.set_page_load_timeout (60)
        self.driver.get ('http://www.nytimes.com/')
	tim = str(datetime.now())


	recomms = self.driver.find_element_by_xpath ("//*[@id='recommendations']/div[5]")

	headlines = recomms.find_elements_by_class_name('headline')
	for headline in headlines:
		title1 = (headline.get_attribute("summarytext"))
		title2 = strip_tags (title1).encode("utf8")
		title3 = title2.strip()
            	agency = "NYTimes"
            	heading = "Recommended"
            	news = tim+"@|"+heading+"@|"+title3+"@|"+agency+"@|"+"ago"+"@|"+"Body"
            	self.log('measurement', 'news', news)
