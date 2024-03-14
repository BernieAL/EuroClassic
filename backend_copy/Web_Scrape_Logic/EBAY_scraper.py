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


current_dir =os.path.abspath(__file__)
print(current_dir)
sys.path.append(current_dir)


SCRAPED_DATA_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'Scraped_data_output')

EBAY_raw_SOLD_output_file_path = os.path.join(SCRAPED_DATA_OUTPUT_DIR,'EBAY_raw_SOLD_DATA.txt')
EBAY_raw_SOLD_output_file = open(EBAY_raw_SOLD_output_file_path ,"a",encoding="utf-8")

error_log_file = os.path.join(SCRAPED_DATA_OUTPUT_DIR, '..','error_log.txt')
error_log_output = open(error_log_file,"a",encoding="utf-8")


#function for writing raw scraped data to respective files
def fileWrite(data,fileIn):
    for line in data:
        temp = f"{line}"
        fileIn.write(temp)

def error_log(error_obj):

    """this function is called from indiv scraping functions when an exception is encountered 
    Recieves error_obj constructed in indiv scraper function with exceptions caught
    """
    
    temp = f"{error_obj} \n -----------"
    error_log_output.write(temp)        


#this function gets current listings
def ebay_current_scrape_single_veh(car,driver):
    
    target_car = f"{car['make']} {car['model']}"
    
    
    try:
        # driver.get("https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117")
        
        # #enter model 
        # ebay_search_box = driver.find_element(By.CSS_SELECTOR,'#gh-ac')
        # time.sleep(1)
        # ebay_search_box.send_keys(target_car + Keys.RETURN)
        # time.sleep(1.5)

        """This url reduces # of pages to visit by requesting 240 items per page ---> &_ipg=240
        """
        intial_url = f"https://www.ebay.com/sch/6001/i.html?_from=R40&_nkw={car['make']}+{car['model']}&_sacat=6001&_ipg=240&rt=nc"
        driver.get(intial_url)

        # #url for testing   
        # intial_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=audi&_sacat=0&_ipg=240&rt=nc"
        # driver.get(intial_url)
        
        

        #holds concatenated descrip,price
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

       
        #write date of scrape to file right before data
        today = date.today()
        current_date = today.strftime("%m/%d/%Y")
        date_string = f" :::EBAY - DATA SCRAPED ON: {current_date} \n"
        EBAY_raw_SOLD_output_file .write(date_string)   

        """
        for page in page range (1->n) start from second page since we are already on first page
        """
        for pg_link in pages_links[1:3]:
            
         
            #get references to all listing info elements on page, store as list
            ebay_listings = driver.find_elements(By.CLASS_NAME,'s-item__info')
            #get references to all description elements on page, store as list
            all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')
            #get references all price elements on page, store as list
            all_prices = driver.find_elements(By.CLASS_NAME,'s-item__price')

            

            for (descrip,price) in zip(all_descriptions,all_prices):
                item_description= descrip.get_attribute('innerText')
                #REMOVES'NEW LISTING from listing description if present
                item_description = item_description.replace('NEW LISTING','')
                item_price = price.get_attribute('innerText')
                temp = f'{item_description} {item_price}'
                ebay_items.append(temp)
                
                
            #write ebay_items to file before going to next page - in case script fails or mem issue with array
            fileWrite(ebay_items,EBAY_raw_SOLD_output_file )
            #clear array ahead of next page - to avoid writing duplicate data to file
            ebay_items.clear
       

            #slow down page navigation
            time.sleep(random.uniform(3,9))
            driver.get(pg_link)

        
        success_obj = {
                    'success': True,
                    'function':'ebay_scrape',
                    'date': current_date,
        }

        #before exiting this 
        return success_obj
    
    except NoSuchElementException as e:
        error_obj = {
               'error':e,
               'function':'bat_scrape',
               'date': current_date
        }
        error_log(error_obj)
        return error_obj
        

    # print(ebay_items)

#this ebay section gets sold listings, beginnning from intial url again, and appends 'sold' and 'complete' params to the url
def ebay_sold_scrape_single_veh(car,driver):
    # target_car = f"{car['make']} {car['model']}"

    intial_url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={car['make']}&{car['model']}_sacat=0&_ipg=240&rt=nc"
    # intial_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=audi&_sacat=0&_ipg=240&rt=nc"
    sold_complete_url = intial_url + '&LH_Sold=1&LH_Complete=1'
    
    try:
        # driver.get("https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117")
        # driver.get("https://www.ebay.com/sch/i.html?_from=R40&_nkw=honda+accord&_sacat=6001&_sop=13&_stpos=07029&_fspt=1&LH_PrefLoc=98&rt=nc&LH_Sold=1&LH_Complete=1")
        
        time.sleep(4)
        driver.get(sold_complete_url)
        

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

    

       #write date of scrape to file right before data
        today = date.today()
        current_date = today.strftime("%m/%d/%Y")
        date_string = f" :::EBAY - DATA SCRAPED ON: {current_date} \n"
        EBAY_raw_SOLD_output_file.write(date_string)                    


        """for page in page range (1->n) start from second page since we are already on first page
        """
        for pg_link in pages_links[1:]:
            #this gets prices of all cars on page
            ebay_items = []
            ebay_listings = driver.find_elements(By.CLASS_NAME,'s-item__info')
            all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')

            all_prices = driver.find_elements(By.CLASS_NAME,'s-item__price')

            #targets "Sold Month Date, Year" on each listing
            all_sale_dates = driver.find_elements(By.CSS_SELECTOR,'.s-item__title--tag span.POSITIVE')

            


            for (descrip,price,sale_date) in zip(all_descriptions,all_prices,all_sale_dates):
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
        fileWrite(ebay_items,EBAY_raw_SOLD_output_file )
         #clear array ahead of next page - to avoid writing duplicate data to file
        ebay_items.clear
        
        #slow down page navigation
        time.sleep(random.uniform(3,9))
        driver.get(pg_link)
        
            
        success_obj = {
                    'success': True,
                    'function':'ebay_scrape_sold',
                    'date': current_date,
        }
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
    'make':'Porsche',
    'model':'911'
    }

    seleniumwire_options = {
            'proxy': {
                'http':'http://S9ut1ooaahvD1OLI:DGHQMuozSx9pfIDX_country-us@geo.iproyal.com:12321',
                'https':'https://S9ut1ooaahvD1OLI:DGHQMuozSx9pfIDX_country-us@geo.iproyal.com:12321'
            },
            'detach':True
        }

    uc_chrome_options =uc.ChromeOptions()
    # chrome_options = Options()
    #uc_chrome_options.add_argument(f"user-agent={my_user_agent}")

    #stop browser from closing - requires manual closing
    # uc.Chrome(use_subprocess=True)

    
    #stop images from loading - improve page speed and reduce proxy data usage
    uc_chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    
    #ignore ssl issues from https
    uc_chrome_options.set_capability('acceptSslCerts',True)
    uc_chrome_options.add_argument('--ignore-ssl-errors=yes')
    uc_chrome_options.add_argument('--ignore-certificate-errors')
    uc_chrome_options.add_argument("--allow-running-insecure-content")

            
    #undetected chromedriver with proxy with chromedriver manager no .exe path
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()),seleniumwire_options=seleniumwire_options,options=uc_chrome_options)

    
    ebay_current_scrape_single_veh()
    ebay_sold_scrape_single_veh()

