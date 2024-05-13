"""
This script will read in data from LTS dir, add vehicles to vehicle_dir.csv
which will be written to db in insert_data.py script

LTS (longterm prev scrapes dir) has previously scraped data for many vehicles, 
and it can be used in the DB as a means to reduce the need for additional scrapes.

For each file in EBAY/SOLD and EBAY/CURR
    get the vehicle name and scrape data from the file name itself- this will be added to vehicle_directory csv

"""


import psycopg2
import os
from datetime import datetime
import csv
from dotenv import load_dotenv,find_dotenv
from simple_chalk import chalk
import pandas as pd

postgres_dir = os.path.dirname(__file__)
#directory of 'this' file
INPUT_veh_dir_file_path = os.path.join(postgres_dir,'..','vehicle_directory.csv')



LTS_EBAY_DIR = os.path.join(postgres_dir,'..','LongTerm_prev_scrapes/EBAY')
# print(os.path.isdir(LTS_EBAY_DIR))



def build_dir_entry_from_filename(INPUT_veh_dir_file_path):

    veh_dir = open(INPUT_veh_dir_file_path,'a')

    """
    The filename for vehicles scrapes record in LTS looks like
        EBAY__CURR__03-30-2024__NISSAN-350Z.txt
    
    From the filename, we parse the values we need to create a formatted entry for veh_dir
        Which is in format -> NISSAN,350Z,0000,2024-03-22
    """
    # os.walk to access contents of LTS DIR
    for root,dirs,files in os.walk(LTS_EBAY_DIR):
    
        try:
            for file in files: #EX filename -> EBAY__CURR__03-30-2024__NISSAN-350Z.txt

                
                tokens = file.split('__') #['EBAY', 'SOLD', '05-02-2024', 'BMW-M6.txt'] 
                
                record_type = tokens[1] # SOLD or CURR
                date_val = tokens[2] 
                #must convert date_val from MM-DD-YYYY to required format by veh_dir csv YYYY-MM-DD
                date_obj = datetime.strptime(date_val,"%m-%d-%Y")
                date_formatted = date_obj.strftime("%Y-%m-%d")
                
                # NISSAN-350Z.txt -> NISSAN-350Z
                vehicle = tokens[3].replace('.txt','')
                
                #NISSAN-350Z -> [NISSAN,350Z]
                make_model_tokens = vehicle.split('-')
                
                make,model = make_model_tokens
                #using "0000" for year because scraped records are not year specific and contain various years
                veh_dir_entry = f"{make},{model},{'0000'},{date_formatted}"
                print(veh_dir_entry)

                veh_dir.write(veh_dir_entry+'\n')


        except Exception as e:
            print(f"error: {e}") 
            

    veh_dir.close()
        

def keep_latest(INPUT_veh_dir_file_path):

    """
        In the Event theres multiple entries for a vehicle, keep the latest date, remove all others
        Ex.    
            BMW,M3,2018,2024-01-20
            BMW,M3,0000,2024-05-01
            BMW,M3,0000,2024-04-03
            BMW,M3,0000,2024-05-02

            output:
                BMW,M3,0000,2024-05-02
    """
    df = pd.read_csv(INPUT_veh_dir_file_path)
    #making sure last_scrape_date is datetime obj
    df['LAST_SCRAPE_DATE'] = pd.to_datetime(df['LAST_SCRAPE_DATE'])
    #sort by date, in place
    df.sort_values(by='LAST_SCRAPE_DATE',inplace=True)

    #for each make,model group, keep the entry with latest date
    latest_date = df.groupby(['MAKE','MODEL']).tail(1).reset_index(drop=True)
    
    sorted_by_makes = latest_date.sort_values(by='MAKE')
    sorted_by_makes.to_csv(INPUT_veh_dir_file_path,index=False)

    
   


    


if __name__ == "__main__":
     
     
    keep_latest(INPUT_veh_dir_file_path)