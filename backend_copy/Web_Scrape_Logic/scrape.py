"""
https://stackoverflow.com/questions/49788257/what-is-default-location-of-chromedriver-and-for-installing-chrome-on-windows
from selenium import webdriver

# Optional argument : if not specified WebDriver will search your system PATH environment variable for locating the chromedriver
driver = webdriver.Chrome(executable_path=r'C:\path\to\chromedriver.exe')
driver.get('https://www.google.co.in')
print("Page Title is : %s" %driver.title)
driver.quit()

https://www.selenium.dev/documentation/webdriver/web_element/

https://stackoverflow.com/questions/34315533/can-i-find-an-element-using-regex-with-python-and-selenium
https://stackoverflow.com/questions/12323403/how-do-i-find-an-element-that-contains-specific-text-in-selenium-webdriver-pyth

https://stackoverflow.com/questions/45990851/how-do-i-iterate-through-a-webelements-list-with-python-and-selenium/46001881


UnicodeEncodeError: 'charmap' codec can't encode characters
https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters




"""


from threading import Thread
from typing import ClassVar
from selenium import webdriver
from datetime import date
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from datetime import datetime

from seleniumwire import webdriver


import time
# from clean_data import clean_the_data



import os
# make = "audi"
# chassis =""
# model ="rs5"
# year =""
# # 98-03 for m5

#dir of raw extracted data
extracted_data_dir_path = os.path.join(os.path.dirname(__file__), '..', 'Extracted_data')

raw_SOLD_output_file_path = os.path.join(extracted_data_dir_path, '..','raw_SOLD_DATA.txt')

raw_CURRENT_LISTING_output_file_path = os.path.join(extracted_data_dir_path, '..','raw_CURRENT_LISTINGS_DATA.txt')

EBAY_raw_SOLD_output_file_path = os.path.join(extracted_data_dir_path, '..','EBAY_raw_SOLD_DATA.txt')


error_log_file = os.path.join(extracted_data_dir_path, '..','error_log.txt')

#files for current listing data and sold data
raw_current_listing_output = open(raw_CURRENT_LISTING_output_file_path,"a",encoding="utf-8")
raw_sold_output = open(raw_SOLD_output_file_path,"a",encoding="utf-8")
error_log_output = open(error_log_file,"a",encoding="utf-8")
EBAY_raw_SOLD_output = open(EBAY_raw_SOLD_output_file_path ,"a",encoding="utf-8")



#CLEAR EXISTING FILE CONTENTS BEFORE EACH NEW SCRAPE FOR VEHICLE

# current_listing_output.truncate(0)
# sold_output.truncate(0)

# Create a new chromedriver
# driver = webdriver.Chrome(executable_path=r'C:\Users\balma\Documents\Programming\chromedriver.exe')

# ===========================================================================
# ===========================================================================
# # :::::: BEGIN EBAY SECTION 

"""
EBAY section has 2 functions
1 function collects current listings and writes to current_listings file
1 function collects sold listings and writes to EBAY_raw_SOLD_output file

ebay_current
    -navigates to ebay
    -targets search bar and enters target vehicle, and enter is clicked to begin search
    -
"""

#this ebay section gets current listings
def ebay_current(car,driver):
    
    target_car = f"{car['make']} {car['model']}"
    
    
    try:
        # driver.get("https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117")
        
        # #enter model 
        # ebay_search_box = driver.find_element(By.CSS_SELECTOR,'#gh-ac')
        # time.sleep(1)
        # ebay_search_box.send_keys(target_car + Keys.RETURN)
        # time.sleep(1.5)

        """This url reduces # of pages to visit by requesting 240 items per page
        """
        # driver.get(f"https://www.ebay.com/sch/6001/i.html?_from=R40&_nkw={car['make']}+{car['model']}&_sacat=6001&_ipg=240&rt=nc")
               
        driver.get("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=audi&_sacat=0&_odkw=nissan+sentra&_osacat=0")
        

        #holds concatenated descrip,price
        ebay_items = []

        """ PAGE NUM DISCOVERY
            -to find out how many pages there are look at element <ol class="pagination__items">
                -nested in the ol, there will be an li element for each page
                -from this li element, theres a nested href with the url for that page	
                -for each li, get the href, these are the available pages to visit
                -we can iterate and visit these page links
        """
        pages_links = driver.find_elements(By.CSS_SELECTOR,'.pagination__items li a')
        for links in pages_links:
            print(links.get_attribute('href'))
        
        
        #get references to all listing info elements on page, store as list
        ebay_listings = driver.find_elements(By.CLASS_NAME,'s-item__info')
        #get references to all description elements on page, store as list
        all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')
        #get references all price elements on page, store as list
        all_prices = driver.find_elements(By.CLASS_NAME,'s-item__price')

        for (descrip,price) in zip(all_descriptions,all_prices):
            item_description= descrip.get_attribute('innerText')
            item_description = item_description.replace('NEW LISTING','')
            item_price = price.get_attribute('innerText')
            temp = f'{item_description} {item_price}'
            ebay_items.append(temp)

        

        #write date of scrape to file right before data
        today = date.today()
        # dd/mm/YY
        current_date = today.strftime("%m/%d/%Y")
        date_string = f" :::EBAY - DATA SCRAPED ON: {current_date} \n"
        raw_current_listing_output.write(date_string)   

        #write items to file
        fileWrite(ebay_items,raw_current_listing_output)
        success_obj = {
                    'success': True,
                    'function':'ebay_scrape',
                    'date': current_date,
        }
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

#this ebay section gets sold listings, it picks up from the page of curr listings

def ebay_sold(driver):
    # target_car = f"{car['make']} {car['model']}"
    
    #get curr_url from last page visited - which is current listings
    curr_url = driver.current_url
    #concat curr_url with necessary ebay url params for sold and complete
    sold_complete_url = curr_url + '&LH_Sold=1&LH_Complete=1'
    
    try:
        # driver.get("https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117")
        # driver.get("https://www.ebay.com/sch/i.html?_from=R40&_nkw=honda+accord&_sacat=6001&_sop=13&_stpos=07029&_fspt=1&LH_PrefLoc=98&rt=nc&LH_Sold=1&LH_Complete=1")
        time.sleep(4)
        driver.get(sold_complete_url)
        

        #this gets prices of all cars on page
        ebay_items = []
        ebay_listings = driver.find_elements(By.CLASS_NAME,'s-item__info')
        all_descriptions = driver.find_elements(By.CLASS_NAME,'s-item__title')

        all_prices = driver.find_elements(By.CLASS_NAME,'s-item__price')

        #targets "Sold Month Date, Year" on each listing
        all_sale_dates = driver.find_elements(By.CSS_SELECTOR,'.s-item__title--tag span.POSITIVE')

        
        # <div class="s-item__title--tag"><span class="POSITIVE">Sold  Jan 11, 2024</span><span class="clipped">Sold Item</span></div>

        for (descrip,price,sale_date) in zip(all_descriptions,all_prices,all_sale_dates):
            item_description= descrip.get_attribute('innerText')
            item_description = item_description.replace('NEW LISTING','')
            item_price = price.get_attribute('innerText')
            
            sale_date_text = sale_date.get_attribute('innerText')
            #convert sale_date_text from January 11th,2024 to 2024-01-11 (yyyy,mm,dd)
            sale_date_text = sale_date_text.replace("Sold ","")
            sale_date_obj = datetime.strptime(sale_date_text,"%b %d, %Y").date()
            print(sale_date_obj)
            
            temp = f'{item_description} {item_price} {sale_date_text}'
            ebay_items.append(temp)

        
        #write date of scrape to file right before data
        today = date.today()
        # dd/mm/YY
        current_date = today.strftime("%m/%d/%Y")
        # date_string = f" :::EBAY - DATA SCRAPED ON: {current_date} \n"
        # raw_current_listing_output.write(date_string)   

        # #write items to file
        fileWrite(ebay_items,EBAY_raw_SOLD_output)
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
        

# # :::::: END EBAY SECTION 
# ===========================================================================

# :::::: BEGIN CRAIGLIST SECTION
def CL(car,driver):
    # search route option 1 - longer and more human-like
    # driver.get('https://miami.craigslist.org/mdc/')
    # CL_searchBar = driver.find_element_by_css_selector('#query')
    # time.sleep(2)
    # CL_searchBar.send_keys(vehicle + Keys.RETURN)

    #search route option 2 - more direct
    make = car['make']
    model = car['model']
    
    try:    
        driver.get(f'https://miami.craigslist.org/d/cars-trucks/search/mdc/cta?query={make}%20{model}&sort=rel')

        CL_prices=[]
        CL_items = []
        CL_items = driver.find_elements(By.CLASS_NAME,'result-info')
        for item in CL_items:
            description = driver.find_elements(By.CLASS_NAME,'result-heading').get_attribute('innerText')
            price = item.find_element(By.CLASS_NAME,'result-price').get_attribute('innerText')
            temp = f" {description}:{price}"
            CL_prices.append(temp)
            # print(f" {description}:{price}")

        #write date of scrape to file right before data
        today = date.today()
        # dd/mm/YY
        current_date = today.strftime("%m/%d/%Y")
        date_string = f" :::CRAIGLIST - DATA SCRAPED ON: {current_date} \n"
        raw_current_listing_output.write(date_string)   

        #write items to file
        fileWrite(CL_prices,raw_current_listing_output)    
        success_obj = {
                    'success': True,
                    'function':'CL_scrape',
                    'date': current_date,
        }
        return success_obj
    except NoSuchElementException as e:
        error_obj = {
               'error':e,
               'function':'bat_scrape',
               'date': current_date
        }
        error_log(error_obj)
        return error_obj
        
# :::::: END CRAIGLIST SECTION
# ===========================================================================

# :::::: BEGIN BAT SECTION
# ON BAT, only getting sold listings 
def bat_scrape(car,driver):
        
    try:
            # this is to get passed "show notifications prompt"
                # driver.send_keys(Keys.TAB)
                # driver.send_keys(Keys.TAB)
                # driver.send_keys(Keys.RETURN)
             #write date of scrape to file right before data
            today = date.today()
            # dd/mm/YY
            current_date = today.strftime("%m/%d/%Y")

            make = car['make']
            model = car['model']
            driver.get(f'https://bringatrailer.com/{make}/{model}')
            # URL EXAMPLE:  https://bringatrailer.com/bmw/e39-m5/?q=e39%20m5
            
            time.sleep(2)
        

            # this is to get passed "show notifications prompt" - SHOULDNT BE NEEDED, SCRAPE STILL WORKS WITHOUT DISMISSING PROMPT
                # driver.send_keys(Keys.TAB)
                # driver.send_keys(Keys.TAB)
                # driver.send_keys(Keys.RETURN)


            # this section clicks 'Show More' on page to load ALL sold listings for target vehicle
            try:
                show_more = driver.find_element(By.LINK_TEXT,'Show More')
                # # # LOGIC TO CLICK SHOW MORE REPEATEDLY UNTIL NO 
                while show_more:
                    try:
                        show_more.click()
                        time.sleep(2)
                    except ElementNotVisibleException:
                        print('NOTHING MORE TO LOAD')
                        break
                    except NoSuchElementException:
                        print('ELEMENT NOT FOUND')
                        break
                    except StaleElementReferenceException:
                        print('NO MORE RESULTS TO LOAD')
                        break
            except NoSuchElementException as e:
                pass
            time.sleep(2)
            # show_more.click()

        

            #target parent group that holds individual previous listing items
            prev_listings = driver.find_element(By.CLASS_NAME,'filter-group')
            time.sleep(1.5)
            
            #extract all block elements from parents group, this gives each indiv listing
            #item_list is all returned listing details found using 'block' class
            item_list = prev_listings.find_elements(By.CLASS_NAME,'block')


            #EXTRACT MODEL,YEAR,PRICE from each item in item_list
            BAT_items = []
            for item in item_list:
                description = item.find_element(By.CLASS_NAME,'title').get_attribute('innerText')
                price = item.find_element(By.CLASS_NAME,'subtitle').get_attribute('innerText')
                temp = f'{description} {price}'
                BAT_items.append(temp)


           
            raw_sold_output.write(date_string)

            #write items to output file
            fileWrite(BAT_items,raw_sold_output)
            # print(BAT_items)
            success_obj = {
                    'success': True,
                    'function':'bat_scrape',
                    'date': current_date,
            }
            return success_obj

    except NoSuchElementException as e:
        error_obj = {
               'error':e,
               'function':'bat_scrape',
               'date': current_date
        }
        error_log(error_obj)
        return error_obj
        
# :::::: END BAT SECTION
# ==============================================================================



#function for writing raw scraped data to respective files
def fileWrite(data,fileIn):
    for line in data:
        temp = f"{line} \n"
        fileIn.write(temp)

"""
this function is called from indiv scraping functions when an exception is encountered 
Recieves error_obj constructed in indiv scraper function with exceptions caught
"""

def error_log(error_obj):
    temp = f"{error_obj} \n -----------"
    error_log_output.write(temp)

#main driver function - CALLING ALL SCRAPE FUNCTIONS sequentially
def run_scrape(car):
        
        # truncate deletes all file contents
        raw_current_listing_output.truncate(0)
        raw_sold_output.truncate(0)


        options = {
            'proxy': {
                'http':'http://S9ut1ooaahvD1OLI:DGHQMuozSx9pfIDX_country-us@geo.iproyal.com:12321',
                'https':'https://S9ut1ooaahvD1OLI:DGHQMuozSx9pfIDX_country-us@geo.iproyal.com:12321'
            },
        }
        
        # driver = webdriver.Chrome(executable_path=r'C:\browserdrivers\chromedriver\chromedriver.exe',seleniumwire_options=options)
        # # driver.get("https://bot.sannysoft.com/")
        # # print(driver.current_url)
        
        driver = webdriver.Chrome(executable_path=r'C:\browserdrivers\chromedriver\chromedriver.exe')

        # scrape results tells you if each scraper function was successful or not
        scrape_results = (
            ebay_current(car,driver),
            # ebay_sold(driver)
            # CL(car,driver),
            # bat_scrape(car,driver)
            time.sleep(9)
        )
    
        driver.close
        
        raw_current_listing_output.close()
        raw_sold_output.close()

        #return scrape_results to calling location
        return scrape_results

# If going to run this file individually uncomment the below
if __name__ == '__main__':

    car  = {
    'year':2017,
    'make':'BMW',
    'model':'3 Series'
    }

    run_scrape(car)




"""RETURNED RAW DATA EXAMPLES::


EVAY RAW RESULT:
    '$91,000.00  ', '$40,100.00 NEW LISTING1966 Jaguar E-Type ', '$60,099.00 1969 Jaguar E-Type Roadster ', '$35,100.00 1969 Jaguar E-Type ', '$89,500.00 1969 Jaguar E-Type Convertible ', '$79,900.00 1968 Jaguar E-Type ', '$45,100.00 1970 Jaguar E-Type Convertible ', '$102,000.00 1963 Jaguar E-Type ', '$187,500.00 1964 Jaguar E-Type ', '$84,987.00 1974 Jaguar E-Type ', '$109,500.00 1963 Jaguar E-Type ', '$158,995.00 1966 Jaguar E-Type Series 1 4.2 Liter Fixed-head coupe ', '$89,900.00 1971 Jaguar E-Type Fixed Head Coupe ', '$56,995.00 1969 Jaguar E-Type XK-E 2+2 Series 2 ', '$74,625.00 1968 Jaguar E-Type XKE Series II 4.2L 6 cyl 4 spd Convertible ', '$99,500.00 1973 Jaguar 
E-Type Roadster v12 ', '$69,750.00 1970 Jaguar E-Type 1970 JAGUAR XKE 2+2 E-TYPE ',

CL RAW RESULT:

    2012 BMW 5 Series 4dr Sdn 535i RWD 90 Days Car Warranty :$9,800
    2015 BMW 3 Series 328i SKU:FF607643 Sedan :$16,992
    2014 BMW 5 Series 528i with :$15,500
    2013 BMW 7 SERIES 750I XDRIVE SEDAN 4D :$12,950
    2014 BMW 5 Series 528i with :$15,500
    2014 BMW Z4 SDRIVE28I ROADSTER 2D :$21,495
    2010 BMW 3 Series 335i Convertible 2D Convertible Gray - FINANCE :$19,590
    2012 BMW X5 AWD 4dr 35i 90 Days Car Warranty :$11,199
    2014 BMW X3 xDrive28i Sport Utility 4D :$0
    2014 BMW 5 Series 528i with :$15,500
    2013 BMW 3 Series 328i with :$13,639
    2002 HONDA S2000 S CONVERTIBLE :$19,995
    BMW 328i Sedan Sport Package Runs Excellent Clean Title :$9,995
    2014 BMW 3 Series 4dr Sdn 328d RWD 90 Days Car Warranty :$10,499
    2016 DODGE CHARGER R/T ROAD & TRACK SEDAN 4D :$16,950
    2011 Cadillac SRX AWD 4dr Luxury Collection :$8,750

BAT RAW RESULT:
    41k-Mile 2004 BMW M3 Coupe 6-Speed Sold for $38,000 on 7/30/21
    43k-Mile 1999 BMW M3 Coupe 5-Speed Sold for $45,000 on 7/29/21
    Modified 1998 BMW M3 Coupe 5-Speed Sold for $34,000 on 7/29/21
    2004 BMW M3 Convertible Sold for $20,000 on 7/28/21


"""