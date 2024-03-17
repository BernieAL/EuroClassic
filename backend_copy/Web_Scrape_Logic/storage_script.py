"""
This script will be imported and used in other scraper scripts
Once a scraper script writes the raw scraped data to the output file, this script is called to make a direct copy of the current output file and store in dir /long-term-prev-scrapes

copied file will have the name - "data source__CURRENT DATE__VEH__NAME

long term storage of raw scraped data
create new dir called long-term-prev-scrapes
	concept:
		file where we store raw data from all prev scrapes
		filenames will include data-source,scrape-date,veh-name
			Ex. EBAY__7-12-2024__Audi-R8.txt
	Benefit:
		having historical scrapes in case cleaned data gets ruined or we lose dome data from db, we have original unprocessed backups
"""

import os
import sys
import shutil
from datetime import date,datetime
import time

current_dir = os.path.abspath(__file__)
# print(current_dir)
sys.path.append(current_dir)


#get abs path of 'this' file, then get the dir path of this file - not including the file name itself
current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(current_dir)


"""
This function takes a file, and creates a copy of it, storing it in curr dir
"""
def copy_file(dest_dir_specifier,source_file,data_source,scrape_date,car):

    """
    
    Copies the source file to a specified destination directory, creating the directory if it doesn't exist.
    The destination file's name is constructed using the data source, scrape date, and car name.

    -dest_dir_specifier: The subdirectory within 'LongTerm_prev_scrapes' where the file should be copied.
    -source_file: Path to the source file that needs to be copied.
        Ex. if dest_dir_specifier is set to EBAY from calling statement in scraper - then we get path to LTS/EBAY and copy source file to this location.
    -data_source: The name of the data source (e.g., 'EBAY').
    -scrape_date: The date of the scrape, used in the file name.
    -car: The name of the car, used in the file name.
    
  
    """
   
    #check that the destination directory exists
    PROJ_ROOT = os.path.join(current_dir,'..')

    DEST_DIR_PATH = os.path.join(PROJ_ROOT,'LongTerm_prev_scrapes', dest_dir_specifier)

    if not os.path.exists(DEST_DIR_PATH):
        os.makedirs(DEST_DIR_PATH)
        print(f"Created directory: {DEST_DIR_PATH}")

   

    #create file name using params 
    output_file_name = f"{data_source.upper()}__{scrape_date}__{car.upper()}.txt"
    output_file_path = os.path.join(DEST_DIR_PATH,output_file_name)

    shutil.copy(source_file,output_file_path)
    print(f"SUCCESSFULLY COPIED FILE CONTENTS FROM {source_file} TO {output_file_name}")



if __name__ == "__main__":

    #using dummy file/data to copy
    test_file_to_copy = os.path.join(current_dir,"EBAY__3-17-24__PORCSHE PANAMERA.txt")
    data_source = "EBAY"
    car = "AUDI R8"
    scrape_date ="03-14-2024" 

    copy_file("EBAY",test_file_to_copy,data_source,scrape_date,car)