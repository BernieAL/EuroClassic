from EBAY_scraper import ebay_CURRENT_scrape_single_veh,ebay_SOLD_scrape_single_veh
from BAT_scraper import BAT_scrape_single_veh,BAT_scrape_all_for_make

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import seleniumwire.undetected_chromedriver as uc


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support import expected_conditions as EC


import os
from datetime import date,datetime
import time
import random
import sys


"""
   -This function configures the driver instance that will be used in run_scrapers(), where the driver 
   will be passed to each scraper function
   -Moved driver config logic into seperate function for organization
"""
def initialize_driver():
    seleniumwire_options = {
            'proxy': {
                'http':'http://S9ut1ooaahvD1OLI:DGHQMuozSx9pfIDX_country-us@geo.iproyal.com:12321',
                'https':'https://S9ut1ooaahvD1OLI:DGHQMuozSx9pfIDX_country-us@geo.iproyal.com:12321'
            },
            'detach':True
        }

    uc_chrome_options = uc.ChromeOptions()
    
    #stop images from loading - improve page speed and reduce proxy data usage
    # uc_chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    
    #ignore ssl issues from https
    # uc_chrome_options.set_capability('acceptSslCerts',True)
    uc_chrome_options.add_argument('--blink-settings=imagesEnabled=false','--ignore-ssl-errors=yes','--ignore-certificate-errors','--allow-running-insecure-content')
    # uc_chrome_options.add_argument('--ignore-certificate-errors')
    # uc_chrome_options.add_argument('--allow-running-insecure-content')

            
    #undetected chromedriver with proxy with chromedriver manager no .exe path
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()),seleniumwire_options=seleniumwire_options,options=uc_chrome_options)
    
    return driver

def run_scapers(driver,car):

    
    driver = initialize_driver()

    
    ebay_CURRENT_scrape_single_veh(car,driver)
    ebay_SOLD_scrape_single_veh(car,driver)

    driver.close()
    
    
    # #DO NOT CHANGE OR REMOVE THIS SLEEP - IT HANDLES DRIVER ERROR
    time.sleep(1)


   

    





if __name__ == '__main__':
    
    
    ebay_CURRENT_scrape_single_veh()
    ebay_SOLD_scrape_single_veh()