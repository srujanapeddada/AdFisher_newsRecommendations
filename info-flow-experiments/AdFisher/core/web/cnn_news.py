import time, re
import sys
from selenium import webdriver
import selenium.common.exceptions
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
        # Set the timeout for page load to one minute
        self.driver.set_page_load_timeout (60)
        self.driver.get ("http://www.cnn.com/")
        time = str (datetime.now())

    # Get the recommendations section of the page
	recomms = self.driver.find_element_by_xpath ("//*[@id='outbrain_widget_1']/div/ul")
    # Get the headlines from the recommended section
	articles = recomms.find_elements_by_tag_name ('li')

    # For each article log the headline and body
	for article in articles:
	    temp = article.find_element_by_tag_name ('a')
	    title = temp.get_attribute ('title')
        agency = "CNN"
	    ago = "0 minutes ago"
        body = article.find_element_by_xpath(".//span[@class='ob_source']/span").get_attribute('innerHTML')
	    heading = "Recommended"
	    news = strip_tags(time+"@|"+heading+"@|"+title+"@|"+agency+"@|"+ago+"@|"+body).encode("utf8")
        self.log('measurement', 'news', news)

    # Search and click on articles based on category and keyword and spend some
    # time on the page to simulate reading
    def read_CNN_articles (self, count=5, keyword=None, category=None, time_on_site=20):
	    self.driver.set_page_load_timeout (60)
        self.driver.get('http://cnn.com/')

        # List of valid categories supported
	    valid_categories = ['u.s.', 'world', 'politics', 'money', 'opinion', 'health',
                            'entertainment', 'style' 'travel', 'sports']

	    categoryTab = self.driver.find_element_by_css_selector('div.nav-menu-links')
        print ("Element found")

	    if (category.lower() in valid_categories):
            # Find the category tab on the naviagation section
	        categoryLink = categoryTab.find_element_by_partial_link_text(category.title())

            # click on the link and wait for it to load
	        categoryLink.click()
	        time.sleep (5)

	        visitedLinks = []
            # index is used to track the articles read since the list
            # needs to be refreshed every time we reload the page
	        index = 0

            # makes sure we visit at most count number of pages
	        for visited in range (0, count):
		        try:
                    time.sleep(3)
		            # searches for links on the page
	                searchLinks = self.driver.find_elements_by_partial_link_text(keyword.title())
		            print ("links in unit: ", len(searchLinks))

                    if (len(searchLinks) == 0):
		                print ("No Links found on: ", keyword)
		                break

	    	    # for each of the links found
	 	        if (index < len(searchLinks)):
		            searchLinks[index].click()
		            index += 1
		            time.sleep(time_on_site)
		            site = self.driver.current_url
		            self.log('treatment', 'read_news', site)
		            # Go back to the previous page
		            self.driver.back()
		    except Exception as e:
		        print (e)
		        print ("Since page cannot be clicked, we use the link")
		        self.driver.get (searchLinks[index].get_attribute('href'))
		        index += 1
		        time.sleep (time_on_site)
		        site = self. driver.current_url
		        self.log('treatment', 'read_news', site)
		        # Go back to the previous page
		        self.driver.back()

