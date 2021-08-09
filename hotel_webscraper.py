#!/apps/anaconda3/bin/python
# -*- coding: utf-8 -*-

import sys
import csv
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

#Path where .csv file will be created/saved
file_path = "/user/ocj2105/Documents/bostonharborreviews.csv"

#number of pages of review
num_page = 462

#url of the hotel to be scraped
url = "https://www.tripadvisor.com/Hotel_Review-g60745-d89575-Reviews-Boston_Harbor_Hotel-Boston_Massachusetts.html"


if len(sys.argv) == 4:
    file_path = sys.argv[1]
    num_page = int(sys.argv[2])
    url = sys.argv[3]

csvFile = open(file_path, 'w', encoding="utf-8")
csvWriter = csv.writer(csvFile)

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
browser.get(url)
html = browser.page_source

browser.implicitly_wait(10)

product = browser.find_element_by_xpath('//*[@id="HEADING"]').text

csvWriter.writerow(["Product Name", product])

name = "Usernames"
title = "Titles"
rating = "Rating"
review = "Reviews"

csvWriter.writerow([name, title, rating, review])

for i in range(0, num_page):
    time.sleep(2)
    for j in range(0, 5):
        try:
            name = browser.find_element_by_xpath('//*[@id="component_15"]/div/div[3]/div['+str(j+3)+']/div[1]/div/div[2]/span/a').text
            title = browser.find_element_by_xpath('//*[@id="component_15"]/div/div[3]/div['+str(j+3)+']/div[2]/div[2]/a/span/span').text
            rate = browser.find_element_by_css_selector('div._2wrUUKlw:nth-child('+str(j+3)+') > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')
            rating_class = rate.get_attribute('class')

            if rating_class == 'ui_bubble_rating bubble_50':
                rating = '5'
            elif rating_class == 'ui_bubble_rating bubble_40':
                rating = '4'
            elif rating_class == 'ui_bubble_rating bubble_30':
                rating = '3'
            elif rating_class == 'ui_bubble_rating bubble_20':
                rating = '2'
            elif rating_class == 'ui_bubble_rating bubble_10':
                rating = '1'

            review = browser.find_element_by_xpath('//*[@id="component_15"]/div/div[3]/div['+str(j+3)+']/div[2]/div[3]/div[1]/div[1]/q/span').text.replace("<br>", " ")
            csvWriter.writerow([name, title, rating, review])

        except NoSuchElementException as exception:
            print("Element not found")

    if i < 1:
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[9]/div/div[1]/div[1]/div/div/div[3]/div[8]/div/a').click()
    else:
        browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[9]/div/div[1]/div[1]/div/div/div[3]/div[8]/div/a[2]').click()

browser.close()