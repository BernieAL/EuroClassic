from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import seleniumwire.undetected_chromedriver as uc
from simple_chalk import chalk

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
from simple_chalk import chalk
import gzip
import logging
import json




# 4/30 LTS TEST USING PREV DATA INSTEAD OF LIVE SCRAPE
"""instead of running live scrape - we are using prev scraped data to test the LTS copy function
  this is to check if lts copy is being made when running with docker compose"""
# TEST_prev_sold_path = os.path.join(os.path.dirname(__file__),'..','PREV_EBAY_SOL_911.txt')
# TEST_prev_sold = open(TEST_prev_sold_path,'r')


# get path to central logging file, and pass into config
api_log_file_path = os.path.join(os.path.dirname(__file__),'..','api_log.txt')

# custom logger to avoid interacting with selenium using debug level wire
logger = logging.getLogger('EBAY_SCRAPER')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(api_log_file_path)
formatter = logging.Formatter('%(asctime)s - EBAY_SCRAPER -  %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
# logging.basicConfig(filename=api_log_file_path,filemode='a',format='%(asctime)s - EBAY_SCRAPER -  %(message)s',level=logging.DEBUG)



from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())     

# Ensure the storage_script is accessible from the path where this script is located
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from LTS_storage_script import copy_file


SCRAPED_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'Scraped_data_output')
# EBAY_raw_SOLD_output_file_path = os.path.join(SCRAPED_DATA_OUTPUT_DIR,'EBAY_raw_SOLD_DATA.txt')

# file paths for writing/reading raw data
EBAY_raw_CURRENT_LISTINGS_file_path = os.path.join(SCRAPED_DATA_DIR, 'EBAY_raw_CURRENT_LISTINGS_DATA.txt')
EBAY_raw_SOLD_DATA_file_path = os.path.join(SCRAPED_DATA_DIR, 'EBAY_raw_SOLD_DATA.txt')

# 3/28 testcl
# array_test_current = os.path.join(SCRAPED_DATA_DIR, 'result-array-test-current.txt')
# array_test_sold = os.path.join(SCRAPED_DATA_DIR, 'result-array-test-sold.txt')

EBAY_SEARCH_URL = "https://www.ebay.com/sch/i.html?_nkw=porsche+911&_sacat=6001&_sop=12&rt=nc&LH_PrefLoc=2&_ipg=240"


def calculate_data_exchanged():
    
    total_data_exchanged = 0

    for request in driver.requests:
        # Get the length of the request body
        request_body_length = len(request.body) if request.body else 0
        
        # Get the length of the response body
        response_body_length = len(request.response.body) if request.response else 0
        
        # Calculate the total data exchanged for this request and response
        data_exchanged = request_body_length + response_body_length
        
        # Add to the total amount of data exchanged
        total_data_exchanged += data_exchanged

    # Convert total_data_exchanged from bytes to megabytes
    total_data_mb = total_data_exchanged / (1024 * 1024)
    return f"{total_data_mb:.2f} MB"

def check_output_dir_exists():
    """checks if the output dir for scraped data exists, if not it creates it
       Path for scraped data dir is backend/Scraped_data_output
    """
    # dir of current script

    current_script_dir = os.path.dirname(os.path.abspath(__file__))  # backend/Web_Scrape_Logic
    BACKEND_ROOT = os.path.abspath(os.path.join(current_script_dir, '..'))  # backend/
    SCRAPED_DATA_DIR = os.path.join(BACKEND_ROOT, 'Scraped_data_output')  # backend/Scraped_data_output
   
    if not os.path.exists(SCRAPED_DATA_DIR):
        os.makedirs(SCRAPED_DATA_DIR)
        print(chalk.green(':::::SCRAPED OUTPUT DIR DNE - CREATING NOW'))
        print(chalk.green(':::::SCRAPED OUTPUT CREATED'))    
    else:
        print(chalk.green(f":::::SCRAPED OUTPUT DIR EXISTS - {SCRAPED_DATA_DIR}"))    
        # print(chalk.green(SCRAPED_DATA_DIR))  

# check_output_dir_exists()

# function for writing raw scraped data to respective files
def fileWrite(data,fileIn):
    for line in data:
        temp = f"{line}\n"
        fileIn.write(temp)

def error_log(error_obj):

    """this function is called from indiv scraping functions when an exception is encountered 
    Recieves error_obj constructed in indiv scraper function with exceptions caught
    """
    
    temp = f"{error_obj} \n -----------"
    # error_log_output.write(temp)        

# def pagination_present_wait():
#     pages = WebDriverWait(driver,12,1,EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.pagination__items li a')))
#     return pages

#this function gets current listings
"""Function accepts file it should write to
"""
def ebay_CURRENT_scrape_single_veh(car,driver,EBAY_raw_CURRENT_output_file_path):
    
    logger.debug("ENTERED EBAY_CURRENT_SCRAPE")
    print(chalk.red("ENTERED EBAY_CURRENT_SCRAPE"))

    logger.debug("PARAMS REC'D %s - %s",json.dumps(car),EBAY_raw_CURRENT_output_file_path)
    print(chalk.red(f"PARAMS REC'D {json.dumps(car)} - {EBAY_raw_CURRENT_output_file_path}"))
    # target_car = f"{car['make']} {car['model']}"
    
    check_output_dir_exists()
    logger.debug("OUTPUT DIR EXISTS")
    print(chalk.red("OUTPUT DIR EXISTS"))
    
    EBAY_raw_CURRENT_output_file = open(EBAY_raw_CURRENT_output_file_path,"a",encoding="utf-8")
    # clear data from prev run scrape to start with empty file
    EBAY_raw_CURRENT_output_file.truncate(0)
    logger.debug("CLEARED PREV FILE DATA")

    # write date of scrape to file right before data
    today = date.today()
    current_date = today.strftime("%m-%d-%Y")
    date_string = f" :::EBAY - CURRENT DATA SCRAPED ON: {current_date} \n"
    EBAY_raw_CURRENT_output_file.write(date_string)   
        

    try:
        
        ### VIA SEARCH BOX INERACTION
        # driver.get("https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117")
        # #enter model 
        # ebay_search_box = driver.find_element(By.CSS_SELECTOR,'#gh-ac')
        # time.sleep(1)
        # ebay_search_box.send_keys(target_car + Keys.RETURN)
        # time.sleep(1.5)

        """This url reduces # of pages to visit by requesting 240 items per page ---> &_ipg=240"""
        intial_url = f"https://www.ebay.com/sch/i.html?_nkw={car['make']}+{car['model']}&_sacat=6001&_sop=12&rt=nc&LH_PrefLoc=2&_ipg=240"
        driver.get(intial_url)
        logger.debug("NAVIGATED TO %s",intial_url)
        #wait for page to load
        time.sleep(random.uniform(3,9))
        
        # URL FOR TESTING PURPOSES ONLY  
        # intial_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=audi&_sacat=0&_ipg=240&rt=nc"
        # driver.get(intial_url)
        
        #Will store concatenated string of descrip,price for each listing result
        ebay_items = []

        # """ PAGE NUM DISCOVERY
        #     -to find out how many pages there are look at element <ol class="pagination__items">
        #         -nested in the ol, there will be an li element for each page
        #         -from this li element, theres a nested href with the url for that page	
        #         -for each li, get the href, these are the available pages to visit
        #         -we can iterate and visit these page links
        # """
        # Stores extracted page links for use in navigation later
        
        pages_links=[]
        # Find each page link in pagination list, store in pages[]
        pages = driver.find_elements(By.CSS_SELECTOR,'.pagination__items li a')

        

        # if len of pages > 0, theres more than one page
        if len(pages) > 0:

            logger.debug("# OF PAGES > 0") 
            logger.debug("# OF PAGES %s",len(pages_links))            
            
            # for each page link in pages[], extract href and store in page links
            for links in pages:
                pages_links.append(links.get_attribute('href'))
            # print(chalk.green(f"Pages Links: {pages_links}"))
       
            """# Navigate through pagination links to visit subsequent pages of eBay listings.
               # Start from the second page because the first page is already loaded.
               # Iterate over pagination links to access all available pages for data extraction.
            """
            for pg_link in pages_links[1:len(pages_links)]: 
                
                
                #get references to all listing info elements on page, store as list
                #ebay_listings = driver.find_elements(By.CLASS_NAME,'s-item__info')
                
                #get references to all description elements on page, store as list
                all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')
                
                #get references all price elements on page, store as list
                all_prices = driver.find_elements(By.CLASS_NAME,'s-item__price')
                
                logger.debug("FINDING ELEMENTS ON PAGE")
                
                #for each descrip in all_descriptions, for each price in all_prices
                for (descrip,price) in zip(all_descriptions,all_prices):
                    
                    #extract descrip text
                    item_description= descrip.get_attribute('innerText')
                    
                    #REMOVES'NEW LISTING' from listing description if present
                    item_description = item_description.replace('NEW LISTING','')
                    
                    #extract price text
                    item_price = price.get_attribute('innerText')
                    
                    #concat into single string
                    temp = f'{item_description} {item_price}'
                    
                    #store in ebay_items[]
                    ebay_items.append(temp)
                    # logger.debug("WROTE DESCRIP ELEMENTS TO EBAY_ITEMS_ARRAY")    
                
                #write current ebay_items to file before going to next page - in case script fails or mem issue with array
                fileWrite(ebay_items,EBAY_raw_CURRENT_output_file)
                logger.debug("WROTE EBAY_ITEMS ARRAY TO FILE")
                # print(ebay_items)
                
                # clear array ahead of next page - to avoid writing duplicate data to file
                ebay_items.clear()
                logger.debug("CLEARING EBAY ITEMS ARRAY BEFORE NEXT PAGE VISIT")

                # slow down page navigation
                time.sleep(random.uniform(3,9))

                # navigate to next page in list of pg_links
                driver.get(pg_link)
                logger.debug("NAVIGATING TO NEXT PAGE OF RESULTS")

        # if len pages == 0, theres only one page (the current page), get all the data from this page
        else:
            logger.debug("ONLY 1 PAGE RESULT")
            """If single page, and If not many results on page, ebay provides additional section on page
            called "Results matching fewer words" - to avoid scraping irrelevant results,
            we use the number of results indicated by ebay in the upper right corner of page to filter down the number of found listing card elements down to match the number given by ebay
            
            Ex. #Ex. -> "18 results for nissan 350z"

            -using this, we now know theres only 18 exact match results, and all else are irrelevant
            -Extract the '18' from the string
            -Proceed as normal to find all listing card elements on the page using selenium, which stores them in array
            -slice the array down to the number of exact matches count
                    all_descriptions = all_descriptions[:18+1]
                    +1 to make inclusive - because list slicing stops right before given index, we want to include the last exact match as well
            
            """

            # Ex. -> "18 results for nissan 350z"
            exact_results_count = driver.find_element(By.XPATH,"//h1[contains(., 'results for')]").get_attribute('innerText')
            
            # 18 results for nissan 350z -> ['18', 'results', 'for', 'nissan', '350z'] -> [18]"
            exact_results_count_num = int(exact_results_count.split(" ")[0])
            print(f"(CURR SCRAPER) exact results count: {exact_results_count_num}")
            
            # find all elements listing card element using s-item__title class
            all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')
            
            # from all found listing card elements,
            # use exact_results_count_num to filter list down only to exact matches
            all_descriptions_reduced = all_descriptions[:exact_results_count_num+1]
         
            # get references all price elements on page, store as list
            all_prices = driver.find_elements(By.CLASS_NAME,'s-item__price')

            
            # for each descrip in all_descriptions, for each price in all_prices
            for (descrip,price) in zip(all_descriptions_reduced,all_prices):
                # extract descrip text
                item_description= descrip.get_attribute('innerText')
                
                # REMOVES'NEW LISTING' from listing description if present
                item_description = item_description.replace('NEW LISTING','')
                
                # extract price text
                item_price = price.get_attribute('innerText')
                
                # concat into single string
                temp = f'{item_description.upper()} {item_price}'
                #store in ebay_items[]
                ebay_items.append(temp)
                # logger.debug("WROTE DECSCRIP ELEMENTS TO EBAY_ITEMS_ARRAY")   
                
            # write current ebay_items to file
            fileWrite(ebay_items,EBAY_raw_CURRENT_output_file)
            logger.debug("WROTE EBAY_ITEMS ARRAY TO FILE")

            ebay_items.clear()

            logger.debug("CLEARING EBAY ITEMS ARRAY")
            
        #     #TEST logger reqeusts to file for each page
        #     # data_exchanged = calculate_data_exchanged() 
        #     # test_log_file.write(f" exact_results: { exact_results_count} data used:  {data_exchanged} \n")   
        #     # har_log_file_current.write(driver.har)
        #     # del driver.requests
        #     # time.sleep(2)

        carName = f"{car['make']}-{car['model']}"
        # close file before copying or it will result in empty copied file
        EBAY_raw_CURRENT_output_file.close()
        logger.debug("CLOSING OUTPUT FILE %s -", EBAY_raw_CURRENT_output_file)
        copy_file("EBAY",EBAY_raw_CURRENT_output_file_path,"EBAY",current_date,carName,"CURR")

        # FOR TESTING LTS COPY WITH PREV DATA TO AVOID LIVE SCRAPE
        # copy_file("EBAY",TEST_prev_sold_path,"EBAY",current_date,"test_prev_sold_911","CURR")
        
        logger.debug("MADE COPY OF OUTPUT FILE, STORED IN LTS ")
        print(chalk.red("MADE COPY OF OUTPUT FILE, STORED IN LTS "))

        success_obj = {
                    'success': True,
                    'function':'ebay_scrape',
                    'date': current_date,
        }

        # before exiting this
        time.sleep(random.uniform(4,11))
        # driver.close()
        # DO NOT CHANGE OR REMOVE THIS SLEEP - IT HANDLES DRIVER ERROR
        time.sleep(1)
        logger.debug("EXITING EBAY_CURRENT_SCRAPE")
        print(chalk.red("EXITING EBAY_CURRENT_SCRAPE"))
        return success_obj
    
    except Exception as e:
        error_obj = {
               'error':e,
               'function':'EBAY CURRENT',
               'date': current_date
        }
        # error_log(error_obj)
        logger.error("Exception occurred %s", error_obj, exc_info=True)
        return error_obj
        

   

"""this ebay section gets sold listings, beginnning from intial url again, and appends 'sold' and 'complete' params to the url"""
def ebay_SOLD_scrape_single_veh_2(car,driver,EBAY_raw_SOLD_DATA_output_file_path):
    

    logger.debug("ENTERED EBAY_SOLD_SCRAPE")
    print(chalk.red("ENTERED EBAY_SOLD_SCRAPE"))
    
    logger.debug("PARAMS REC'D %s - %s",json.dumps(car),EBAY_raw_SOLD_DATA_output_file_path)
    print(chalk.red(f"PARAMS REC'D {json.dumps(car)} - {EBAY_raw_SOLD_DATA_output_file_path}"))
    
    check_output_dir_exists()
    logger.debug("OUTPUT DIR EXISTS")
    print(chalk.red("OUTPUT DIR EXISTS"))

    # target_car = f"{car['make']} {car['model']}"
    #open output file to store raw scraped data
    EBAY_raw_SOLD_output_file = open(EBAY_raw_SOLD_DATA_output_file_path,"a",encoding="utf-8")

    #clear existing data from prev scrape
    EBAY_raw_SOLD_output_file.truncate(0)
    logger.debug("CLEARED PREV FILE DATA")

    #write date of scrape to file right before data
    today = date.today()
    current_date = today.strftime("%m-%d-%Y")
    date_string = f" :::EBAY - SOLD DATA SCRAPED ON: {current_date} \n"
    EBAY_raw_SOLD_output_file.write(date_string)    

   

    # https://www.ebay.com/sch/i.html?_nkw=BMW+M3&_sacat=6001&_sop=12&rt=nc&LH_PrefLoc=2&_ipg=240&LH_Sold=1&LH_Complete=1
    
    
    try:

        #paremertized url with vehicle details
        intial_url = f"https://www.ebay.com/sch/i.html?_nkw={car['make']}+{car['model']}&_sacat=6001&_sop=12&rt=nc&LH_PrefLoc=2&_ipg=240"
        # intial_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=audi&_sacat=0&_ipg=240&rt=nc"
        #url params for getting sold listing results
        sold_complete_url = intial_url + '&LH_Sold=1&LH_Complete=1'
        
        #navigate to url
        driver.get(sold_complete_url)
        logger.debug("NAVIGATED TO %s",sold_complete_url)
        print(chalk.red(f"NAVIGATED TO %s {sold_complete_url}"))
        time.sleep(random.uniform(3,9))

        #Will store concatenated string of descrip,price for each listing result
        ebay_items = []
        
        """ PAGE NUM DISCOVERY
            -to find out how many pages there are look at element <ol class="pagination__items">
                -nested in the ol, there will be an li element for each page
                -from this li element, theres a nested href with the url for that page	
                -for each li, get the href, these are the available pages to visit
                -we can iterate and visit these page links
        """
        
        # Stores extracted page links for use in navigation later
        pages_links=[]
        # Find each page link in pagination list, store in pages[]
        pages = driver.find_elements(By.CSS_SELECTOR,'.pagination__items li a') 
         # for each page link in pages[], extract href and store in page links
        for links in pages:
            pages_links.append(links.get_attribute('href'))        


        # if len of pages > 0, theres more than one page of results
        if len(pages) > 0:
            """
            # Navigate through pagination links to visit subsequent pages of eBay listings.
            # Start from the second page because the first page is already loaded.
            # Iterate over pagination links to access all available pages for data extraction.
            """
            logger.debug("# OF PAGES > 0") 
            logger.debug("# OF PAGES %s",len(pages_links))


            for pg_link in pages_links[1:len(pages_links)]:  
                
                # ebay_listings = driver.find_elements(By.CLASS_NAME,'s-item__info')
                
                # get references to all description elements on page, store as list
                all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')
                
                # get references all price elements on page, store as list
                all_prices = driver.find_elements(By.CLASS_NAME,'s-item__price')

                # targets "Sold Month Date, Year" on each listing
                all_sale_dates = driver.find_elements(By.XPATH,"//span[contains(.,'Sold')]")
                logger.debug("FINDING ELEMENTS ON PAGE")
                

                # for each descrip in all_descriptions, for each price in all_prices,for each sale date in all_sale_dates
                for (descrip,price,sale_date) in zip(all_descriptions,all_prices,all_sale_dates):
                    item_description= descrip.get_attribute('innerText')
                    item_description = item_description.replace('NEW LISTING','')
                    item_price = price.get_attribute('innerText')
                    
                    sale_date_text = sale_date.get_attribute('innerText')
                    # convert sale_date_text from January 11th,2024 to 2024-01-11 (yyyy,mm,dd)
                    sale_date_text = sale_date_text.replace("Sold ","")
                    sale_date_text_date_obj = datetime.strptime(sale_date_text,"%b %d, %Y").date()
                    
                    # concat into single string
                    temp = f'{item_description.upper()} {item_price} {sale_date_text_date_obj}'
                    # store in ebay_items[]
                    ebay_items.append(temp)
                    print(temp)
                    # logger.debug("WROTE DESCRIP ELEMENTS TO EBAY_ITEMS_ARRAY")    

                # write items to file
                fileWrite(ebay_items,EBAY_raw_SOLD_output_file)
                logger.debug("WROTE EBAY_ITEMS ARRAY TO FILE")
                # har_log_file_sold.write(driver.har)
                # clear array ahead of next page - to avoid writing duplicate data to file
                ebay_items.clear()
                logger.debug("CLEARING EBAY ITEMS ARRAY BEFORE NEXT PAGE VISIT")
                
                # slow down page navigation
                time.sleep(random.uniform(3,9))

                driver.get(pg_link)
                logger.debug("NAVIGATING TO NEXT PAGE OF RESULTS")
            
        # if len pages == 0, theres only one page (the current page), get all the data from this page
        else:
            logger.debug("ONLY 1 PAGE RESULT")
            """If single page, and If not many results on page, ebay provides additional section on page
            called "Results matching fewer words" - to avoid scraping irrelevant results,
            we use the number of results indicated by ebay in the upper right corner of page to filter down the number of found listing card elements down to match the number given by ebay
            
            Ex. #Ex. -> "18 results for nissan 350z"

            -using this, we now know theres only 18 exact match results, and all else are irrelevant
            -Extract the '18' from the string
            -Proceed as normal to find all listing card elements on the page using selenium, which stores them in array
            -slice the array down to the number of exact matches count
                    all_descriptions = all_descriptions[:18+1]
                    +1 to make inclusive - because list slicing stops right before given index, we want to include the last exact match as well
            
            """
            # Ex. -> "18 results for nissan 350z"
            exact_results_count = driver.find_element(By.XPATH,"//h1[contains(., 'results for')]").get_attribute('innerText')
            
            # 18 results for nissan 350z -> ['18', 'results', 'for', 'nissan', '350z'] -> [18]"
            exact_results_count_num = int(exact_results_count.split(" ")[0])
            print(f"(SOLD SCRAPER) exact results count: {exact_results_count_num}")
            
            # find all elements listing card element using s-item__title class
            all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')
            
            # from all found listing card elements,
            # use exact_results_count_num to filter list down only to exact matches
            all_descriptions = all_descriptions[:exact_results_count_num+1]
            all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')

            # Assuming exact_results_count_num is defined somewhere
            # Reduce the list down only to exact matches
            all_descriptions_reduced = all_descriptions[:exact_results_count_num+1]

            all_prices = driver.find_elements(By.CLASS_NAME,'s-item__price')

            #targets "Sold Month Date, Year" on each listing
            all_sale_dates = driver.find_elements(By.XPATH,"//span[contains(.,'Sold')]")

            for (descrip,price,sale_date) in zip(all_descriptions_reduced,all_prices,all_sale_dates):
                    
                    sale_date_text = sale_date.get_attribute('innerText')
                    
                    # Handle edge case of skipping "Sold Items", we want "Sold on <Month> <Day> <Year>"
                    if sale_date_text == "Sold Items":
                        continue
                    
                    sale_date_text = sale_date.get_attribute('innerText')
                    #convert sale_date_text from January 11th,2024 to 2024-01-11 (yyyy,mm,dd)
                    sale_date_text = sale_date_text.replace("Sold ","")
                    sale_date_text_date_obj = datetime.strptime(sale_date_text,"%b %d, %Y").date()
                    
                    item_description= descrip.get_attribute('innerText')
                    item_description = item_description.replace('NEW LISTING','')
                    item_price = price.get_attribute('innerText')
                    
                  
                    #concat into single string
                    temp = f'{item_description.upper()} {item_price} {sale_date_text_date_obj}'
                    #store in ebay_items[]
                    ebay_items.append(temp) 


            #write items to file
            fileWrite(ebay_items,EBAY_raw_SOLD_output_file)
            logger.debug("WROTE EBAY_ITEMS ARRAY TO FILE")
            
            # ebay_items.clear()
            
            logger.debug("CLEARING EBAY ITEMS ARRAY")
            # har_log_file_sold.write(driver.har)
            
        carName = f"{car['make']}-{car['model']}"
        #close file before copying or it will result in empty copied file
        EBAY_raw_SOLD_output_file.close()

        logger.debug("CLOSING OUTPUT FILE %s -", EBAY_raw_SOLD_output_file)
        copy_file("EBAY",EBAY_raw_SOLD_DATA_output_file_path,"EBAY",current_date,carName,"SOLD")
        

        #FOR TESTING LTS COPY WITH PREV DATA
        # copy_file("EBAY",TEST_prev_sold_path,"EBAY",current_date,"test_prev_sold_911","SOLD")
        
        logger.debug("MADE COPY OF OUTPUT FILE, STORED IN LTS ")
        print(chalk.red("MADE COPY OF OUTPUT FILE, STORED IN LTS "))

        success_obj = {
                    'success': True,
                    'function':'ebay_scrape_sold',
                    'date': current_date,
        }
        
        time.sleep(random.uniform(4,11))
        # driver.close()
        
        #DO NOT CHANGE OR REMOVE THIS SLEEP - IT HANDLES DRIVER ERROR
        time.sleep(1)
        logger.debug("EXITING EBAY_SOLD_SCRAPE")
        print(chalk.red("EXITING EBAY_SOLD_SCRAPE"))
        return success_obj
    
    except Exception as e:
        
        error_obj = {
               'error':e,
               'function':'ebay_sold_listings',
               'date': current_date
        }
        error_log(error_obj)
        return error_obj


def ebay_SOLD_scrape_single_veh(car,driver,EBAY_raw_SOLD_DATA_output_file_path):
    
    # target_car = f"{car['make']} {car['model']}"
    EBAY_raw_SOLD_output_file = open(EBAY_raw_SOLD_DATA_output_file_path,"a",encoding="utf-8")

    #clear existing data from prev scrape
    EBAY_raw_SOLD_output_file.truncate(0)
    

    intial_url = f"https://www.ebay.com/sch/i.html?_nkw={car['make']}+{car['model']}&_sacat=6001&_sop=12&rt=nc&LH_PrefLoc=2&_ipg=240"
   

    # intial_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=audi&_sacat=0&_ipg=240&rt=nc"

    sold_complete_url = intial_url + '&LH_Sold=1&LH_Complete=1'
    
    #write date of scrape to file right before data
    today = date.today()
    current_date = today.strftime("%m-%d-%Y")
    date_string = f" :::EBAY - SOLD DATA SCRAPED ON: {current_date} \n"
    EBAY_raw_SOLD_output_file.write(date_string)        
    
    try:
        # driver.get("https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117")
        # driver.get("https://www.ebay.com/sch/i.html?_from=R40&_nkw=honda+accord&_sacat=6001&_sop=13&_fspt=1&LH_PrefLoc=98&rt=nc&LH_Sold=1&LH_Complete=1")
        
        
        driver.get(sold_complete_url)
        time.sleep(7)

        #Stores concatenated string of descrip,price
        ebay_items = []
        
        """ PAGE NUM DISCOVERY
            -to find out how many pages there are look at element <ol class="pagination__items">
                -nested in the ol, there will be an li element for each page
                -from this li element, theres a nested href with the url for that page  
                -for each li, get the href, these are the available pages to visit
                -we can iterate and visit these page links
        """
        pages_links=[]
        pages = driver.find_elements(By.CSS_SELECTOR,'.pagination__items li a') 
        for links in pages:
            pages_links.append(links.get_attribute('href'))            

        #if len of pages > 0, theres more than one page
        if len(pages) > 0:
            """
        # Navigate through pagination links to visit subsequent pages of eBay listings.
        # Start from the second page because the first page is already loaded.
        # Iterate over pagination links to access all available pages for data extraction.
        """
            for pg_link in pages_links[1:len(pages_links)]:  
                
                #ebay_listings = driver.find_elements(By.CLASS_NAME,'s-item__info')
                
                #get references to all description elements on page, store as list
                all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')
                #get references all price elements on page, store as list
                all_prices = driver.find_elements(By.CLASS_NAME,'s-item__price')

                #targets "Sold Month Date, Year" on each listing
                all_sale_dates = driver.find_elements(By.XPATH,"//span[contains(.,Sold')]")

                

                #for each descrip in all_descriptions, for each price in all_prices,for each sale date in all_sale_dates
                for (descrip,price,sale_date) in zip(all_descriptions,all_prices,all_sale_dates):
                    
                    sale_date_text = sale_date.get_attribute('innerText')
                    
                    # Handle edge case of skipping "Sold Items", we want "Sold on <Month> <Day> <Year>"
                    if sale_date_text == "Sold Items":
                        continue
                    
                    sale_date_text = sale_date.get_attribute('innerText')
                    #convert sale_date_text from January 11th,2024 to 2024-01-11 (yyyy,mm,dd)
                    sale_date_text = sale_date_text.replace("Sold ","")
                    sale_date_text_date_obj = datetime.strptime(sale_date_text,"%b %d, %Y").date()
                    
                    item_description= descrip.get_attribute('innerText')
                    item_description = item_description.replace('NEW LISTING','')
                    item_price = price.get_attribute('innerText')
                    
                  
                    #concat into single string
                    temp = f'{item_description.upper()} {item_price} {sale_date_text_date_obj}'
                    #store in ebay_items[]
                    ebay_items.append(temp)

                #write items to file
                fileWrite(ebay_items,EBAY_raw_SOLD_output_file)
                # har_log_file_sold.write(driver.har)
                #clear array ahead of next page - to avoid writing duplicate data to file
                ebay_items.clear
                
                #slow down page navigation
                time.sleep(random.uniform(3,9))
                driver.get(pg_link)
            
           
        #if len pages == 0, theres only one page (the current page), get all the data from this page   
        else:
            
            """
            If single page, and If not many results on page, ebay provides additional section on page
            called "Results matching fewer words" - to avoid scraping irrelevant results,
            we use the number of results indicated by ebay in the upper right corner of page to filter down the number of found listing card elements down to match the number given by ebay
            
            Ex. #Ex. -> "18 results for nissan 350z"

            -using this, we now know theres only 18 exact match results, and all else are irrelevant
            -Extract the '18' from the string
            -Proceed as normal to find all listing card elements on the page using selenium, which stores them in array
            -slice the array down to the number of exact matches count
                    all_descriptions = all_descriptions[:18+1]
                    +1 to make inclusive - because list slicing stops right before given index, we want to include the last exact match as well
            
            """
            #Ex. -> "18 results for nissan 350z"
            exact_results_count = driver.find_element(By.XPATH,"//h1[contains(., 'results for')]").get_attribute('innerText')
            
            # 18 results for nissan 350z -> ['18', 'results', 'for', 'nissan', '350z'] -> [18]"
            exact_results_count_num = int(exact_results_count.split(" ")[0])
            print(exact_results_count_num)
            
            #find all elements listing card element using s-item__title class
            all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')
            
            #from all found listing card elements, 
            #use exact_results_count_num to filter list down only to exact matches
            all_descriptions = all_descriptions[:exact_results_count_num+1]
            all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')

            # Assuming exact_results_count_num is defined somewhere
            # Reduce the list down only to exact matches
            all_descriptions_reduced = all_descriptions[:exact_results_count_num+1]

            all_prices = driver.find_elements(By.CLASS_NAME,'s-item__price')

            #targets "Sold Month Date, Year" on each listing
            all_sale_dates = driver.find_elements(By.CSS_SELECTOR,'.s-item__title--tag span.POSITIVE')

            for (descrip,price,sale_date) in zip(all_descriptions_reduced,all_prices,all_sale_dates):
                    item_description= descrip.get_attribute('innerText')
                    item_description = item_description.replace('NEW LISTING','')
                    item_price = price.get_attribute('innerText')
                    
                    sale_date_text = sale_date.get_attribute('innerText')
                    #convert sale_date_text from January 11th,2024 to 2024-01-11 (yyyy,mm,dd)
                    sale_date_text = sale_date_text.replace("Sold ","")
                    sale_date_text_date_obj = datetime.strptime(sale_date_text,"%b %d, %Y").date()
                    
                    
                    temp = f'{item_description} {item_price} {sale_date_text_date_obj}'
                    ebay_items.append(temp)

            #write items to file
            fileWrite(ebay_items,EBAY_raw_SOLD_output_file)
            # har_log_file_sold.write(driver.har)
            
        carName = f"{car['make']}-{car['model']}"
        #close file before copying or it will result in empty copied file
        EBAY_raw_SOLD_output_file.close()
        copy_file("EBAY",EBAY_raw_SOLD_DATA_output_file_path,"EBAY",current_date,carName,"SOLD")
        success_obj = {
                    'success': True,
                    'function':'ebay_scrape_sold',
                    'date': current_date,
        }
        
        time.sleep(random.uniform(4,11))
        # driver.close()
        #DO NOT CHANGE OR REMOVE THIS SLEEP - IT HANDLES DRIVER ERROR
        time.sleep(1)
        return success_obj
    
    except NoSuchElementException as e:
       
        error_obj = {
               'error':e,
               'function':'ebay_sold_listings',
               'date': current_date
        }
        error_log(error_obj)
        return error_obj
          

if __name__ == '__main__':


    car  = {
    'year':2017,
    'make':'BMW',
    'model':'M5'
    }

    seleniumwire_options = {
            'proxy': {
                'http':os.getenv('PROXY_HTTP'),
                # 'https':os.getenv('PROXY_HTTPS')
            },
            'detach':True,
            'enable_har': True 
        }

    uc_chrome_options = uc.ChromeOptions()
    
    #stop images from loading - improve page speed and reduce proxy data usage
    uc_chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    
    #ignore ssl issues from https
    # uc_chrome_options.set_capability('acceptSslCerts',True)
    uc_chrome_options.add_argument('--ignore-ssl-errors=yes')
    # uc_chrome_options.add_argument('--headless')
    uc_chrome_options.add_argument('--ignore-certificate-errors')
    uc_chrome_options.add_argument("--allow-running-insecure-content")

            
    #undetected chromedriver with proxy and with chromedriver manager no .exe path
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()),seleniumwire_options=seleniumwire_options,options=uc_chrome_options)


    current_script_dir = os.path.dirname(os.path.abspath(__file__)) #backend/
    test_log_file_path = os.path.join(current_script_dir,'TEST_request_log.txt')
    
    # ebay_CURRENT_scrape_single_veh(car,driver,EBAY_raw_CURRENT_LISTINGS_file_path)
    ebay_SOLD_scrape_single_veh_2(car,driver,EBAY_raw_SOLD_DATA_file_path)
    
    # test_log_file = open(test_log_file_path,'a')

    # har_log_file_path_sold = os.path.join(current_script_dir,'HAR_request_log_sold.json')
    # har_log_file_sold = open(har_log_file_path_sold,'w')
   
    # har_log_file_path_current = os.path.join(current_script_dir,'HAR_request_log_current.json')
    # har_log_file_current = open(har_log_file_path_current,'w')

    # har_log_file_path_bot_test = os.path.join(current_script_dir,'HAR_request_log_bot_test.json')
    # har_log_file_bot_test = open(har_log_file_path_current,'w')

    # driver.get("https://bot.sannysoft.com/")
    # har_log_file_bot_test.write(driver.har)


    # TEST logger reqeusts to file for each page
    # for request in driver.requests:
    #     try:
    #         print(chalk.green((request.url, request.response.status_code)))
    #         test_log_file.write(f"REQ: {request.url} --- \n"
    #                             f"REQUEST BODY:{(gzip.decompress(request.body)).decode('utf-8')}\n"
    #                             f"RESPONSE BODY:{(gzip.decompress(request.response.body)).decode('utf-8')}\n"
    #                             f"{request.response.status_code}\n"
    #                               "++++++++ \n")
    #     except Exception as e:
    #         print(chalk.red(e))

    # Calculate the total amount of data exchanged
    # total_data_exchanged = 0

    # for request in driver.requests:
    #     # Get the length of the request body
    #     request_body_length = len(request.body) if request.body else 0
        
    #     # Get the length of the response body
    #     response_body_length = len(request.response.body) if request.response else 0
        
    #     # Calculate the total data exchanged for this request and response
    #     data_exchanged = request_body_length + response_body_length
        
    #     # Add to the total amount of data exchanged
    #     total_data_exchanged += data_exchanged

    # # Convert total_data_exchanged from bytes to megabytes
    # total_data_mb = total_data_exchanged / (1024 * 1024)

    # print(f"Total amount of data exchanged: {total_data_mb:.2f} MB")
        
    
    # DO NOT CHANGE OR REMOVE THIS SLEEP - IT HANDLES DRIVER ERROR
    time.sleep(10)
    driver.close()
    time.sleep(1)

    

   

    



