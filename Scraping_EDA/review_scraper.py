#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
from bs4 import BeautifulSoup  
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
import time


# In[5]:


def reviews_scraper(url):
    executable_path = 'C:/Users/Xing Fang/Desktop/2019f/bia 660/geckodriver-v0.25.0-win64/geckodriver'
    page_url=url
    driver = webdriver.Firefox(executable_path=executable_path)
    driver.implicitly_wait(10) 
    driver.get(page_url)
    
    try:
        book_title = driver.find_element_by_xpath("//*[@id='ebooksProductTitle']").text

    except Exception as e:
        try:
            book_title = driver.find_element_by_xpath('//*[@id="productTitle"]').text
        except Exception as e:
            book_title = None


    all_link_css = "#reviews-medley-footer > div.a-row.a-spacing-large > a"
    all_link = WebDriverWait(driver, 20).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, all_link_css)))
    all_link.click()

    #2.2 scrape positive reviews

    #2.2.1 click link for positive reviews
    all_star = driver.find_element_by_css_selector("#a-autoid-6-announce")
    time.sleep(5)
    all_star.click()

    all_positive_css = "#star-count-dropdown_6"
    all_positive = driver.find_element_by_css_selector(all_positive_css)
    all_positive.click()

    positive_review_css = driver.find_element_by_css_selector("#filter-info-section > span:nth-child(1)")
    positive_review_n = positive_review_css.text
    positive_review_n = re.search(r"of\s[0-9]?(\,)?[0-9]+", positive_review_n).group()[3:]
    positive_review_n = [str(i) for i in positive_review_n if i !=',']
    positive_review_n = int(''.join(positive_review_n))
    positive_review_n = int(positive_review_n/10)

    positive_reviews = []
    error = []

    #2.2.1 loop thr positive reviews for many pages
    for j in range(positive_review_n+1):

        reviewslist = driver.find_elements_by_css_selector("#cm_cr-review_list > div")

        for i in range(len(reviewslist)-1):
            
            try:
                star = reviewslist[i].find_element_by_css_selector(
                    "div > div > div:nth-child(2) > a:nth-child(1) > i > span").get_attribute('textContent')[0]
            except Exception as e:
                star = None
                error.append(('star', j, i,1))
                

            try:
                title = reviewslist[i].find_element_by_css_selector("div > div > div:nth-child(2) > a.a-size-base.a-link-normal.review-title.a-color-base.review-title-content.a-text-bold > span").text
            except Exception as e:
                title = None
                error.append(('title', j, i,1))
              
            
            try:
                format_ = reviewslist[i].find_element_by_css_selector("div > div > div.a-row.a-spacing-mini.review-data.review-format-strip > a").text
            except Exception as e:
                format_ = None
                error.append(('format', j, i,1))
           
                     
            try:
                review = reviewslist[i].find_element_by_css_selector("div > div > div.a-row.a-spacing-small.review-data > span > span").text

            except Exception as e:
                review = None
                error.append(('review', j, i,1))
                
            
            try:
                helpful = reviewslist[i].find_element_by_css_selector("div > div > div:last-child > div > span > div.a-row.a-spacing-small > span").text
                
            except Exception as e:
                helpful = None
                error.append(('helpful', j, i,1))
                
            sentiment = 1
            positive_reviews.append((book_title, star, title, format_, review, helpful, sentiment))
        
        print( i+1,  'success!' )
        try:
            next_page = driver.find_element_by_css_selector('div.a-form-actions.a-spacing-top-extra-large > span > div > ul > li.a-last > a')
            next_page.click()
        except:
            continue       

    all_star = driver.find_element_by_css_selector("#a-autoid-6-announce")
    time.sleep(5)
    all_star.click()

    all_negative_css = "#star-count-dropdown_7"
    all_negativ = driver.find_element_by_css_selector(all_negative_css)
    time.sleep(5)
    all_negativ.click()

    negative_review_css = driver.find_element_by_css_selector("#filter-info-section > span:nth-child(1)")
    negative_review_n = negative_review_css.text
    negative_review_n = re.search(r"of\s[0-9]?(\,)?[0-9]+", negative_review_n).group()[3:]
    negative_review_n = [str(i) for i in negative_review_n if i !=',']
    negative_review_n = int(''.join(negative_review_n))
    negative_review_n = int(negative_review_n/10)

    negative_reviews = []
    

    for j in range(negative_review_n+1):
        reviewslist = driver.find_elements_by_css_selector("#cm_cr-review_list > div")

        for i in range(len(reviewslist)-1):
            
            try:
                star = reviewslist[i].find_element_by_css_selector("div > div > div:nth-child(2) > a:first-child > i > span").get_attribute('textContent')[0]
               
            except Exception as e:
                star = None
                error.append(('star', j, i,0))
               
            
            try:
                title = reviewslist[i].find_element_by_css_selector("div > div > div:nth-child(2) > a.a-size-base.a-link-normal.review-title.a-color-base.review-title-content.a-text-bold > span").text
                
            except Exception as e:
                title = None
                error.append(('title', j, i,0))
               
            
            try:
                format_ = reviewslist[i].find_element_by_css_selector("div > div > div.a-row.a-spacing-mini.review-data.review-format-strip > a").text
                
            except Exception as e:
                format_ = None
                error.append(('format', j, i, 0))
               
            
            try:
                review = reviewslist[i].find_element_by_css_selector("div > div > div.a-row.a-spacing-small.review-data > span > span").text
                
            except Exception as e:
                review = None
                error.append(('review', j, i, 0))
                
            
            try:
                helpful = reviewslist[i].find_element_by_css_selector("div > div > div:last-child > div > span > div.a-row.a-spacing-small > span").text
                
            except Exception as e:
                helpful = None
                error.append(('helpful', j, i, 0))
                           
            sentiment=0
            negative_reviews.append((book_title, star, title, format_, review, helpful, sentiment))
        
        try:
            next_page = driver.find_element_by_css_selector('div.a-form-actions.a-spacing-top-extra-large > span > div > ul > li.a-last > a')
            next_page.click()
        except:
            continue

    reviews = positive_reviews + negative_reviews

    
    return reviews,error,book_title


# In[ ]:


url = "https://www.amazon.com/Meathead-Science-Great-Barbecue-Grilling/dp/054401846X/ref=sr_1_132?qid=1572724494&s=books&sr=1-132"
reviews, error,book_title = reviews_scraper(url)
reviews = pd.DataFrame(reviews, columns =["book_title", "star", "title", "format", "review", "helpful", "sentiment"])
reviews_error = pd.DataFrame(error, columns = ["error_item", 'page_num', 'book_num','sentiment'])
reviews.to_csv('C://Users/Xing Fang/Desktop/2019f/bia 660/final project/Result/Meathead-Science-Great-Barbecue-Grilling.csv')
reviews_error.to_csv('C://Users/Xing Fang/Desktop/2019f/bia 660/final project/Result/[error]Meathead-Science-Great-Barbecue-Grilling.csv')

