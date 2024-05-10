"""
This script will read in data from LTS dir, add vehicles to vehicle_dir csv and then insert to db

LTS (longterm prev scrapes dir) has previously scraped data for many vehicles, and it can be used in the DB
as a means to reduce the need for additional scrapes.

For each file in EBAY/SOLD and EBAY/CURR
    get the vehicle name and scrape data from the file name itself- this will be added to vehicle_directory csv

    Then write all records contained in the file to the db
"""


import psycopg2
import os
from datetime import datetime
import csv
from dotenv import load_dotenv,find_dotenv
from simple_chalk import chalk

postgres_dir = os.path.dirname(__file__)
#directory of 'this' file
INPUT_veh_dir_file_path = os.path.join(postgres_dir,'..','vehicle_directory.csv')

veh_dir = open(INPUT_veh_dir_file_path,'a')

LTS_EBAY_DIR = os.path.join(postgres_dir,'..','LongTerm_prev_scrapes/EBAY')
# print(os.path.isdir(LTS_EBAY_DIR))




# os.walk to access contents of LTS DIR
for root,dirs,files in os.walk(LTS_EBAY_DIR):
   
   try:
    for file in files:
            #determine if file is CURR listing
            #EX filename -> EBAY__CURR__03-30-2024__NISSAN-350Z.txt
        
            tokens = file.split('__') #['EBAY', 'SOLD', '05-02-2024', 'BMW-M6.txt'] 
            record_type = tokens[1] # SOLD or CURR
            date_val = tokens[2]
            
            vehicle = tokens[3].replace('.txt','')
            print(vehicle)
            
            make_model_tokens = vehicle.split('-')
            print(make_model_tokens)
            make,model = make_model_tokens
            print(f"{make},{model}")
   except Exception as e:
       print(f"error: {e}") 
          
    
    
        # vehicle = tokens[3].replace('.txt','')
    
        # make_model_tokens = vehicle.split('-')
        # make,model = make_model_tokens
        # # print(f"{make},{model}")

        #year doesnt matter - using 0000 to match veh_dir csv format
        #veh_dir csv format is MAKE,MODEL,YEAR,LAST_SCRAPE_DATE
        #update date to match date format in veh_dir csv YYYY-MM-DD  
        # date_obj = datetime.strptime(date_val,"%m-%d-%Y")
        # formatted_date = date_obj.strftime("%Y-%m-%d")
        # print(formatted_date)
        # veh = f"{make},{model},{'0000'},{formatted_date}"
        # print(veh)

        # veh_dir.write(veh+'\n')
         
    # #   elif 'SOLD' in file:
    #     #  print(file)
