


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import seleniumwire.undetected_chromedriver as uc
import os
from datetime import date,datetime
import time
import random
import sys
from simple_chalk import chalk
import logging

# # Get the current directory of this __init__.py file
# current_dir = os.path.dirname(os.path.abspath(__file__))
# # Add the parent directory to sys.path
# parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)



from Data_Clean_Logic.clean_ebay_data import ebay_clean_data_runner
# from Data_Clean_Logic.clean_bat_data import bat_clean_data_runner
from Web_Scrape_Logic.EBAY_scraper import ebay_CURRENT_scrape_single_veh,ebay_SOLD_scrape_single_veh_2
# from Web_Scrape_Logic.BAT_scraper import BAT_scrape_single_veh,BAT_scrape_all_for_make

from Postgres_logic.insert_data import populate_vehicles_dir_table,insert_new_scraped_veh_VEH_DIR,insert_current_listing_data,insert_sold_data, insertion_check
from Postgres_logic.connect import get_db_connection
# from Web_Scrape_Logic.scrape_runner_main import run_scapers



#get parent dir 'backend_copy' from current script dir - append to sys.path to be searched for modules we import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the directory to sys.path
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import DB_URI,PROXY_HTTPS,PROXY_HTTP





"""PROCESS OVERVIEW: This is the file that will orchestrate all processes for:
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


# get path to central logging file, and pass into config
api_log_file_path = os.path.join(os.path.dirname(__file__),'api_log.txt')

#truncate all logs from prev run
with open(api_log_file_path,'w') as file:
    file.truncate(0)


# custom logger to avoid interacting with selenium using debug level wire
logger = logging.getLogger('APP_MAIN_RUNNER')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(api_log_file_path)
formatter = logging.Formatter('%(asctime)s - APP_MAIN_RUNNER -  %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.debug("Logger initialized - prev logs cleared")



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
EBAY_cleaned_CURRENT_LISTINGS_file_path = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_CURRENT_LISTINGS.csv')
#PATH-> backend/cleaned_data_dir/'EBAY_raw_SOLD_DATA.txt'
EBAY_cleaned_SOLD_DATA_file_path = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_SOLD_DATA.csv')




def initialize_driver():
    seleniumwire_options = {
            'proxy': {
                # 'http':'http://S9ut1ooaahvD1OLI:DGHQMuozSx9pfIDX_country-us@geo.iproyal.com:12321',
                # 'https':'https://S9ut1ooaahvD1OLI:DGHQMuozSx9pfIDX_country-us@geo.iproyal.com:12321'
                'http':PROXY_HTTP,
                'https':PROXY_HTTPS
                # 'no_proxy':'localhost,127.0.0.1'
            },
            'detach':True
        }

    uc_chrome_options = uc.ChromeOptions()
    
    #stop images from loading - improve page speed and reduce proxy data usage
    uc_chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    uc_chrome_options.add_argument('--ignore-ssl-errors=yes')
    uc_chrome_options.add_argument('--ignore-certificate-errors')
    uc_chrome_options.add_argument("--allow-running-insecure-content")
    uc_chrome_options.add_argument("--headless")

    #create undetected chromedriver with proxy and matching chromedriver hanlded by ChromeDriverManager - no .exe path
    driver = uc.Chrome(service=Service(ChromeDriverManager().install()),
                       seleniumwire_options=seleniumwire_options,options=uc_chrome_options)
    
    return driver

"""This gets db connection"""
def initialize_db_connection_connection():

    conn = get_db_connection()
    cur = conn.cursor()
    return conn,cur


def main_runner(veh):

    db_conn,db_cursor = initialize_db_connection_connection()
    driver = initialize_driver()
    # veh = {
    #     'year':2017,
    #     'make':'Nissan',
    #     'model':'370Z'
    # }
    # run_scapers() #runs ebay and bat scrapers
    try:
        #this is coming from scrape_worker
        print(chalk.red(f"(app_main_runner) VEH TO SCRAPE: {veh}"))
        print(chalk.red("(app_main_runner) LAUNCHING SELENIUM PROCESS"))
        # driver.get("https//google.com")

        # #Scraping of ebay data
        ebay_CURRENT_scrape_single_veh(veh,driver,EBAY_raw_CURRENT_LISTINGS_file_path)
        ebay_SOLD_scrape_single_veh_2(veh,driver,EBAY_raw_SOLD_DATA_file_path)
        
        driver.close()  
        time.sleep(1)

        #Scraping of bat data
        # #bat scrape
        # #bat scrape
        
        
        #cleaning of ebay data
        print(chalk.red("(app_main_runner) LAUNCHING CLEANING PROCESS"))
        ebay_clean_data_runner(veh,EBAY_raw_CURRENT_LISTINGS_file_path,EBAY_raw_SOLD_DATA_file_path)
        
        #4/30 TESTING WITH PREV SCRAPED DATA TO AVOID LIVE SCRAPE
        # TEST_prev_sold_path = os.path.join(os.path.dirname(__file__),'PREV_EBAY_SOL_911.txt')
        # ebay_clean_data_runner(veh,TEST_prev_sold_path,TEST_prev_sold_path)

        # #cleaning of bat data
        # #bat_clean_data_single(car,BAT_raw_single)
        # #bat_clean_data_all_make(car,BAT_raw_all_make)
        
        # #insertion of newly scraped ebay data into db
        insert_current_listing_data(db_cursor,db_conn,EBAY_cleaned_CURRENT_LISTINGS_file_path)
        insert_sold_data(db_cursor,db_conn,EBAY_cleaned_SOLD_DATA_file_path)

        # insert veh into veh dir table (vehicles) with last scraped date
        insert_new_scraped_veh_VEH_DIR(db_cursor,db_conn,veh)
        
        #BAT insertion of cleaned data - IMPLEMENT LATER
        #insert_sold_data(db_cursor,BAT_cleaned_single)
        #insert_sold_data(db_cursor,BAT_cleaned_all_make)
        
        #analysis of ebay data
        
        
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        #Ensure the driver is closed in case of an error
        driver.close()  
        time.sleep(1)
        # # Ensure the driver is closed in case of an error
        # return e
    finally:
        db_cursor.close()
        db_conn.close()
         
        pass
        
        #analysis
        #insert data to db

if __name__ == "__main__":
    veh = {
        'year':2017,
        'make': 'BMW', #MUST BE CAPITALIZED OR WILL FAIL
        'model': 'Z4' #MUST BE CAPITALIZED OR WILL FAIL
    }
    main_runner(veh)