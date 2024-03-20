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



# Ensure the storage_script is accessible from the path where this script is located
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend_copy.Web_Scrape_Logic.LTS_storage_script import copy_file

SCRAPED_DATA_OUTPUT_DIR = "Scraped_data_output"
if not os.path.exists(SCRAPED_DATA_OUTPUT_DIR):
    os.makedirs(SCRAPED_DATA_OUTPUT_DIR)

SCRAPED_DATA_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'Scraped_data_output')

error_log_file = os.path.join(SCRAPED_DATA_OUTPUT_DIR, '..','error_log.txt')

#Getting path to and opening output file - all listing for given Vehicle maker
BAT_raw_ALL_MAKE_LISTINGS_SOLD_output_file_path = os.path.join(SCRAPED_DATA_OUTPUT_DIR,'BAT_raw_ALL_MAKE_SOLD_DATA.html')
BAT_raw_ALL_MAKE_LISTINGS_SOLD_output_file = open(BAT_raw_ALL_MAKE_LISTINGS_SOLD_output_file_path ,"a",encoding="utf-8")

##Getting path to and opening output file - all listings for indiv vehicle
BAT_raw_SINGLE_VEH_SOLD_output_file_path = os.path.join(SCRAPED_DATA_OUTPUT_DIR,'BAT_raw_SINGLE_VEH_SOLD_DATA.html')
# print(os.path.isfile(BAT_raw_SINGLE_VEH_SOLD_output_file_path))
BAT_raw_SINGLE_VEH_SOLD_output_file = open(BAT_raw_SINGLE_VEH_SOLD_output_file_path,"a",encoding="utf-8")



def error_log(error_obj):

    """this function is called from indiv scraping functions when an exception is encountered 
    Recieves error_obj constructed in indiv scraper function with exceptions caught
    """
    
    temp = f"{error_obj} \n -----------"
    # error_log_output.write(temp)        



# :::::: BEGIN BAT SECTION
# ON BAT, only getting sold listings 
def BAT_scrape_single_veh(car,driver):
    
    today = date.today()
    current_date = today.strftime("%m-%d-%Y")

    #clear existing data from prev scrape
    # BAT_raw_SINGLE_VEH_SOLD_output_file.truncate(0)
    

    try:     
            
            make = car['make']
            model = car['model']
            
            #SEARCH OPTINON 1 -  BY URL
            # URL EXAMPLE:  https://bringatrailer.com/bmw/e39-m5/?q=e39%20m5
            driver.get(f'https://bringatrailer.com/{make}/{model}/?q={make}+{model}')
           
            
            #SEARCH OPTION 2 - BY SEARCH BAR INTERACTION
            # driver.get('https://bringatrailer.com')
            # search_bar = driver.find_element(By.CSS_SELECTOR,'.search-bar-input')
            # time.sleep(random.uniform(1,5))
            # search_bar.send_keys('Porsche 911' + Keys.RETURN)
            
            time.sleep(random.uniform(4,9))
        
            # this is to get passed "show notifications prompt" - SHOULDNT BE NEEDED, SCRAPE STILL WORKS WITHOUT DISMISSING PROMPT
                # driver.send_keys(Keys.TAB)
                # driver.send_keys(Keys.TAB)
                # driver.send_keys(Keys.RETURN)

            # this section clicks 'Show More' button on page to load ALL sold listings for target vehicle
            try:
                # show_more = driver.find_element(By.LINK_TEXT,'Show More')
                # show_more.click()

                #find 'Auction Results' Section
                auction_results_section = driver.find_element(By.CSS_SELECTOR,'.auctions-completed')

                #find 'show-more' button
                show_more_listing_button = auction_results_section.find_element(By.CSS_SELECTOR,'button.button-show-more')
                show_more_listing_button.click()
                
                #set number of times you want to click "show more" to load more listing sets
                desired_clicks = 2
                i=0
                while i < desired_clicks:
                    try:
                        show_more_listing_button.click()
                        print(f"FOUND 'SHOW MORE' - CLICKING ")
                        time.sleep(random.uniform(4,9))
                    
                    except ElementNotVisibleException:
                        print('NOTHING MORE TO LOAD')
                        break
                    except NoSuchElementException:
                        print('ELEMENT NOT FOUND')
                        break
                    except StaleElementReferenceException:
                        print('NO MORE RESULTS TO LOAD')
                        break
                    i+=1
            except NoSuchElementException as e:
                pass
            
            time.sleep(random.uniform(5,11))


            #get html content and write to output file
            html_content = driver.page_source
            BAT_raw_SINGLE_VEH_SOLD_output_file.write(html_content)
            #before closing file - explicitly flush file bugger to ensure all data is written to disk immediatley
            BAT_raw_ALL_MAKE_LISTINGS_SOLD_output_file.flush()
            print(":::BAT_SCRAPE_SINGLE_VEH -  HTML content successfully saved to file.")

            #close file before copying or it will result in empty copied file
            BAT_raw_SINGLE_VEH_SOLD_output_file.close()

            carName = f"{car['make']} {car['model']}"    
            copy_file("BAT",BAT_raw_SINGLE_VEH_SOLD_output_file_path,'BAT-SINGLE',current_date,carName)

            print(":::BAT_SCRAPE_SINGLE_VEH -  HTML file SUCCESSFULLY COPIED to LTS/BAT")          
           

    except NoSuchElementException as e:
        error_obj = {
               'error':e,
               'function':'bat_scrape',
               'date': current_date
        }
        error_log(error_obj)
        return error_obj
    except TimeoutException as e:
        # Handle the case where the element is not clickable within the specified time
        print("Element not clickable within the specified time.")
    except Exception as e:
        print(f"Error: {e}")
  



def BAT_scrape_all_for_make(car,driver):
    today = date.today()
    current_date = today.strftime("%m-%d-%Y")
    
    #clear existing data from prev scrape
    BAT_raw_ALL_MAKE_LISTINGS_SOLD_output_file.truncate(0)

    try:
        #BY URL
        driver.get(f"https://bringatrailer.com/{car['make']}/?q={car['make']}")

        #ALTERNATE OPTION - BY SEARCH BAR INTERACTION
        # driver.get('https://bringatrailer.com')
        # search_bar = driver.find_element(By.CSS_SELECTOR,'.search-bar-input')
        # time.sleep(random.uniform(1,5))
        # search_bar.send_keys('Porsche 911' + Keys.RETURN)
        
        #find 'Auction Results' Section
        auction_results_section = driver.find_element(By.CSS_SELECTOR,'.auctions-completed')

        #find 'show-more' button
        show_more_listing_button = auction_results_section.find_element(By.CSS_SELECTOR,'button.button-show-more')
        time.sleep(random.uniform(1,5))
        show_more_listing_button.click()
        time.sleep(random.uniform(1,4))
        
        """
            -how many times to click show more button?
            -get number of Auction Results on page and divide by 24 to get number of clicks we need to do - because each click loads 24 more results
            -also as backup, check for existence of show more button, if not visible, stop the loop
        """
        desired_clicks = 2
        for i in range(desired_clicks):
            if show_more_listing_button.is_displayed():
                show_more_listing_button.click()
                print(f"FOUND 'SHOW MORE' - CLICKING ")
                time.sleep(random.uniform(2,7))
            else:
                print(f"SHOW MORE NOT DISPLAYED OR # OF DESIRED CLICKS EXECUTED")
                break;
            
        """
        Get html from page, write to file for parsing later with Beautiful Soup
        """

        html_content = driver.page_source
        BAT_raw_ALL_MAKE_LISTINGS_SOLD_output_file.write(html_content)
        print("HTML content successfully saved to file.")

        #close file before copying or it will result in empty copied file
        BAT_raw_ALL_MAKE_LISTINGS_SOLD_output_file.close()

        carName = f"{car['make']} {car['model']}"    
        copy_file("BAT",BAT_raw_ALL_MAKE_LISTINGS_SOLD_output_file_path,'BAT-ALL-MAKE',current_date,carName)
       
        print(":::BAT_SCRAPE_SINGLE_VEH -  HTML file SUCCESSFULLY COPIED to LTS/BAT")    


    except NoSuchElementException as e:
        error_obj = {
               'error':e,
               'function':'bat_scrape_all',
            #    'date': current_date
        }
        error_log(error_obj)
        return error_obj
    except TimeoutException as e:
        # Handle the case where the element is not clickable within the specified time
        print("Element not clickable within the specified time.")
    except Exception as e:
        print(f"Error: {e}")


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

    uc_chrome_options = uc.ChromeOptions()
    
    #stop images from loading - improve page speed and reduce proxy data usage
    uc_chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    
    #ignore ssl issues from https
    # uc_chrome_options.set_capability('acceptSslCerts',True)
    uc_chrome_options.add_argument('--ignore-ssl-errors=yes')
    uc_chrome_options.add_argument('--ignore-certificate-errors')
    uc_chrome_options.add_argument("--allow-running-insecure-content")

            
    #undetected chromedriver with proxy with chromedriver manager no .exe path
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()),seleniumwire_options=seleniumwire_options,options=uc_chrome_options)

    
    BAT_scrape_single_veh(car,driver)
    # BAT_scrape_all_for_make(car,driver)

    driver.close()
    
    
    
    # #DO NOT CHANGE OR REMOVE THIS SLEEP - IT HANDLES DRIVER ERROR
    time.sleep(1)
