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


    **NOTE ABOUT OVERWRITING:
        The shutil.copy function will overwrite the destination file if it already exists. So, if there's a file with the same name in the destination directory, it will be replaced with the new file being copied.

        Ex. if this file (BAT-ALL-MAKE__03-19-2024__PORSCHE 911.txt) exists already and has data, and the the copy_file function is coming from the same source, from the same vehicle, on the same_date, it will cause the existing one to be overwritten. 

"""

import os
import sys
import shutil
from datetime import date,datetime
import time

#Gives - backend_copy\Web_Scrape_Logic\storage_script.py
current_file_path = os.path.abspath(__file__)
sys.path.append(current_file_path)

#Get abs path of 'this' file, then get the dir path of this file - not including the file name itself
#Gives - EuroClassic\backend_copy\Web_Scrape_Logic
current_script_dir= os.path.dirname(os.path.abspath(__file__))
# print(current_script_dir)
# sys.path.append(current_dir)


"""
This function takes a file, and creates a copy of it, storing it in curr dir
"""
def copy_file(dest_dir_specifier,source_file,data_source,scrape_date,vehicle,data_label="NA"):

    """Accepts FILE PATH of source file - NOT THE OPENED FILE OBJECT REFERENCE
    Copies the source file to a specified destination directory, creating the directory if it doesn't exist.
    The destination file's name is constructed using the data source, scrape date, and car name.
    PARAMS:
        -dest_dir_specifier: The subdirectory within 'LongTerm_prev_scrapes' where the file should be copied.
        -source_file: Path to the source file that needs to be copied.
            Ex. if dest_dir_specifier is set to EBAY from calling statement in scraper - then we get path to LTS/EBAY and copy source file to this location.
        -data_source: The name of the data source (e.g., 'EBAY').
        -scrape_date: The date of the scrape, used in the file name.
        -vehicle: The name of the car, used in the file name.
    
  
    """
   
   # Gives - \EuroClassic\backend_copy
    PROJ_ROOT = os.path.abspath(os.path.join(current_script_dir, '..'))
    
    #build destination path string
    # Ex. '../Longterm_prev_scrapes/EBAY' --> where EBAY is dest_dir_specifier
    DEST_DIR_PATH = os.path.join(PROJ_ROOT,'LongTerm_prev_scrapes', dest_dir_specifier)

    #create dest dir if doesnt exist 
    if not os.path.exists(DEST_DIR_PATH):
        os.makedirs(DEST_DIR_PATH)
        print(f"Created directory: {DEST_DIR_PATH}")

   

    #create file name using params 
    #Ex. EBAY__03-18-24__AUDI-R8
    custom_output_file_name = f"{data_source.upper()}__{data_label.upper()}__{scrape_date}__{vehicle.upper()}.txt"
    
    #create file path for output file
    #Ex. '../Longterm_prev_scrapes/EBAY/EBAY__03-18-24__AUDI-R8'
    custom_output_file_path = os.path.join(DEST_DIR_PATH,custom_output_file_name)

    #copy source and store as output filename
    shutil.copy(source_file,custom_output_file_path)
    print(f"SUCCESSFULLY COPIED FILE CONTENTS FROM {source_file} TO {custom_output_file_name}")



if __name__ == "__main__":

    #using dummy file/data to copy
    # Gives - \EuroClassic\backend_copy
    PROJ_ROOT = os.path.abspath(os.path.join(current_script_dir, '..'))

    #Gives - \EuroClassic\backend_copy\LongTerm_prev_scrapes
    DEST_DIR_PATH = os.path.join(PROJ_ROOT,'LongTerm_prev_scrapes')
    print(DEST_DIR_PATH)
    test_file_to_copy = os.path.join(DEST_DIR_PATH,"test_data_for_copy.txt")
    print(os.path.isfile(test_file_to_copy))

    dest_dir_specifier = "EBAY"
    data_label = "SOLD"
    data_source = "EBAY"
    vehicle = "AUDI R8"
    scrape_date ="03-14-2024" 

    copy_file(dest_dir_specifier,test_file_to_copy,data_source,scrape_date,vehicle,data_label)