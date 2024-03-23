


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import seleniumwire.undetected_chromedriver as uc
import os
from datetime import date,datetime
import time
import random
import sys
from simple_chalk import chalk


from Data_Clean_Logic.clean_ebay_data import ebay_clean_data_runner
# from Data_Clean_Logic.clean_bat_data import bat_clean_data_runner
from Web_Scrape_Logic.EBAY_scraper import ebay_CURRENT_scrape_single_veh,ebay_SOLD_scrape_single_veh
# from Web_Scrape_Logic.BAT_scraper import BAT_scrape_single_veh,BAT_scrape_all_for_make

from Postgres.insert_data import insert_current_listing_data,insert_sold_data, insertion_check
from Postgres.connect import get_db_connection
# from Web_Scrape_Logic.scrape_runner_main import run_scapers

from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())     





"""This is the file that will orchestrate all processes for:
   -scraping
   -cleaning
   -write cleaned data to db
   -analysis of clean data
   -write results to db

   SCRAPING
   -driver should be instantiated and configured here, then passed to all scraper functions
        in this way, if changes need to be made to driver, we dont have to manually do it all scraper functions
   -each scraper function recieves output file paths from main_runner, and will open files and write to them


   CLEANING
   -run cleaning functions, these are specific to the data source
   -have tests to ensure cleaning completed successfully
   -each cleaning function recieves file paths from main_runner, for reading and writing

   WRITING CLEANED DATA TO DB
   -import functions that write to db, pass file references 
        in this way, we can specify files and their locations from a central location (here), and not depend on each cleaning function to have the right path in itself
    -DB functions recieve file paths to read from 
    
   ANALYSIS
   -import analysis functions and pass them cleaned csv files

   -WRITING ANALYSIS DATA TO DB
    -import functions that write to db, pass file paths
    


"""


#dir of current script
current_script_dir = os.path.dirname(os.path.abspath(__file__)) #backend/

###DIR PATHS
#ROOT OF BACKEND 
BACKEND_ROOT = current_script_dir   #backend
SCRAPED_DATA_DIR = os.path.join(BACKEND_ROOT,'Scraped_data_output') #backend/scraped_data_dir
CLEANED_DATA_DIR = os.path.join(BACKEND_ROOT,'Cleaned_data_output')  #backend/cleaned_data_dir
POSTGRES_DIR = os.path.dirname(__file__) #backend/postgres

###FILE PATHS for writing/reading raw data
#PATH-> backend/scraped_data_dir/'EBAY_raw_CURRENT_LISTINGS_DATA.txt'
EBAY_raw_CURRENT_LISTINGS_file_path = os.path.join(SCRAPED_DATA_DIR, 'EBAY_raw_CURRENT_LISTINGS_DATA.txt')  
#PATH -> backend/scraped_data_dir/'EBAY_raw_SOLD_DATA.txt'
EBAY_raw_SOLD_DATA_file_path = os.path.join(SCRAPED_DATA_DIR, 'EBAY_raw_SOLD_DATA.txt')
 
###FILE PATHS for writing/reading cleaned data
#PATH-> backend/cleaned_data_dir/'EBAY_raw_CURRENT_LISTINGS_DATA.txt'
EBAY_clean_OUTPUT_CURRENT_LISTINGS_file_path = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_CURRENT_LISTINGS.csv')
#PATH-> backend/cleaned_data_dir/'EBAY_raw_SOLD_DATA.txt'
EBAY_clean_OUTPUT_SOLD_DATA_file_path = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_SOLD_DATA.csv')



def initialize_driver():
    seleniumwire_options = {
            'proxy': {
                # 'http':'http://S9ut1ooaahvD1OLI:DGHQMuozSx9pfIDX_country-us@geo.iproyal.com:12321',
                # 'https':'https://S9ut1ooaahvD1OLI:DGHQMuozSx9pfIDX_country-us@geo.iproyal.com:12321'
                'http':os.getenv('PROXY_HTTP'),
                'https':os.getenv('PROXY_HTTPS')
            },
            'detach':True
        }

    uc_chrome_options = uc.ChromeOptions()
    
    #stop images from loading - improve page speed and reduce proxy data usage
    uc_chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    uc_chrome_options.add_argument('--ignore-ssl-errors=yes')
    uc_chrome_options.add_argument('--ignore-certificate-errors')
    uc_chrome_options.add_argument("--allow-running-insecure-content")

    #create undetected chromedriver with proxy and matching chromedriver hanlded by ChromeDriverManager - no .exe path
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()),
                       seleniumwire_options=seleniumwire_options,options=uc_chrome_options)
    
    return driver

"""This gets db connection"""
def initialize_db_connection_connection():

    conn = get_db_connection()
    cur = conn.cursor()
    return conn,cur


def main_runner():

    db_conn,db_cursor = initialize_db_connection_connection()
    driver = initialize_driver()
    car = {
        'year':2017,
        'make':'Nissan',
        'model':'370Z'
    }
    # run_scapers() #runs ebay and bat scrapers
    try:
        ebay_CURRENT_scrape_single_veh(car,driver,EBAY_raw_CURRENT_LISTINGS_file_path)
        ebay_SOLD_scrape_single_veh(car,driver,EBAY_raw_SOLD_DATA_file_path)

        # #bat scrape
        # #bat scrape
        driver.close()
        time.sleep(1)
        # ebay_clean_data_runner(car)
        # insert_sold_data(db_cursor)
        # insert_current_listing_data(db_cursor)
        
        
        
    except Exception as e:
        pass
    finally:
        db_cursor.close()
        db_conn.close()
        
    #analysis
    #insert data to db

if __name__ == "__main__":
    pass
    main_runner()