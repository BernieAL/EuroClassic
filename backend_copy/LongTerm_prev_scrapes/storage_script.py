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

#get abs path of 'this' file, then get the dir path of this file - not including the file name itself
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


"""
This function takes a file, and creates a copy of it, storing it in curr dir
"""
def copy_file(source_file,data_source,scrape_date,car):

    output_file_name = f"{data_source.upper()}__{scrape_date}__{car.upper()}.txt"
    output_file_path = os.path.join(current_dir,output_file_name)

    shutil.copy(source_file,output_file_path)
    print(f"SUCCESSFULLY COPIED FILE CONTENTS FROM {source_file} TO {output_file_name}")



if __name__ == "__main__":

    #using dummy file/data to copy
    test_file_to_copy = os.path.join(current_dir,"test_data_for_copy.txt")
    data_source = "EBAY"
    car = "AUDI R8"
    scrape_date ="03-14-2024" 

    copy_file(test_file_to_copy,data_source,scrape_date,car)