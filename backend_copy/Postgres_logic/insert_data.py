"""insert_data.py

This script inserts data from file into db
-Reads in data from csv file
-writes to db
-has function to check if data was persisted correctly

"""



import psycopg2
import os
import csv
from dotenv import load_dotenv,find_dotenv
from simple_chalk import chalk
from datetime import date,datetime

load_dotenv(find_dotenv())     


postgres_dir = os.path.dirname(__file__)
#directory of 'this' file
current_script_dir = os.path.dirname(os.path.abspath(__file__))

#get ref to project root
PROJ_ROOT = os.path.abspath(os.path.join(current_script_dir,'..'))


#dir of cleaned data
CLEANED_DATA_DIR = os.path.join(PROJ_ROOT,'Cleaned_data_output')
print(CLEANED_DATA_DIR)
INPUT_veh_dir_file_path = os.path.join(postgres_dir,'..','vehicle_directory.csv')


clean_CURR_LISTINGS_file = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_CURRENT_LISTINGS.csv')
clean_SOLD_LISTINGS_file = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_SOLD_DATA.csv')

LTR_ROOT_DIR = os.path.join(PROJ_ROOT,'Longterm_prev_scrapes') 

# #TESTING - USING DUMMY DATA
# clean_output_file_SOLD_DATA_file_path = os.path.join(postgres_dir,'..','Dummy_data_generator/sold_listings_dummy.csv')
# print('SOLD_DATA FILE PATH'  + clean_output_file_SOLD_DATA_file_path)

# clean_output_file_CURRENT_LISTINGS_file_path = os.path.join(postgres_dir,'..','Dummy_data_generator/current_listings_dummy.csv')
# print('SOLD_DATA FILE PATH'  + clean_output_file_CURRENT_LISTINGS_file_path)



"""
NO LONGER NEEDED - VEH DIR TABLE POPULATED THROUGH CONT_B_ENTRYPOINT.sh
-Populates DB using veh_directory.csv 
-Veh directory is a file with vehicles we have results for and their last scrape date
-When user requests a vehicle, we check if we have a record for the vehicle and get its last scrape date 
    -if no record of vehicle, a new scrape is queued
    -if last scrape date is too old, new scrape is queued
"""
def populate_vehicles_dir_table(cur,veh_dir_file_path):
    
    veh_dir_data = open(veh_dir_file_path,"r")
    csvreader = csv.reader(veh_dir_data,delimiter=',')

    # this skips the first line in file which is col names
    next(csvreader)
    for line in csvreader:
        try:

            #convert all values in line to uppercase to standardize and elminate failed queries due to mismatch case
            line_uppercase = [value.upper() for value in line]

            sql = """
                INSERT INTO VEHICLES(MAKE,MODEL,YEAR,LAST_SCRAPE_DATE)
                VALUES(%s,%s,%s,%s)
                """
            cur.execute(sql,line_uppercase)
            
        except (Exception, psycopg2.DatabaseError) as e:
             print(chalk.red(f"Failed to populate veh_dir: {e} "))

    print(chalk.green(":::Successfully POPULATED VEH DIR TABLE"))
    conn.commit()


def insert_new_scraped_veh_VEH_DIR(cur,conn,veh):

    """ INCOMING VEH OBJ STRUCTURE
        
           # veh = {
            #     'year':2017,
            #     'make':'Nissan',
            #     'model':'370Z'
            # }
    """

    veh_year = veh['year']
    veh_make = veh['make']
    veh_model = veh['model']
    curr_date = (datetime.today()).strftime("%m-%d-%Y") #get curr date as scrape date

    sql =   """
            INSERT INTO VEHICLES(MAKE,MODEL,YEAR,LAST_SCRAPE_DATE)
            VALUES(%s,%s,%s,%s)
            """ 
    try:
        cur.execute(sql,(veh_year,veh_make,veh_model,curr_date))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
         print(chalk.red(f"Failed to insert veh into veh dir: {e}"))

    print(chalk.green(":::Successfully INSERTED NEWLY SCRAPED VEH into VEH DIR TABLE"))




"""
   -This function accepts a csv file path of sold records
   and inserts them into the db 
   -The source of the data doesnt matter so long as it matches the format specified for sold vehicles records -> YEAR,MAKE,MODEL,SALEPRICE,DATESOLD
"""
def insert_sold_data(cur,conn,cleaned_SOLD_DATA_file_path):
    print(chalk.green(":::Starting insert_sold_data"))
    clean_output_file_SOLD_DATA = open(cleaned_SOLD_DATA_file_path,"r")
    csvreader = csv.reader(clean_output_file_SOLD_DATA,delimiter=',')

    
    # this skips the first line in file which is col names
    next(csvreader)
    for line in csvreader:  
        # print(line)
        #convert all values in line to uppercase to standardize and elminate failed queries due to mismatch case
        line_uppercase = [value.upper() for value in line]
        try:
            sql = """
                INSERT INTO SOLD_LISTINGS(YEAR,MAKE,MODEL,SALEPRICE,DATESOLD)
                VALUES(%s,%s,%s,%s,%s)
                """
            cur.execute(sql,line_uppercase)
        except (Exception, psycopg2.DatabaseError) as e:
            print(f"error: {e} {line}")

    try:
        conn.commit()
        print(chalk.green(":::Successfully inserted all SOLD_LISTINGS records into DB"))
    except Exception as e:
        print(chalk.red(f"Failed to insert sold data: {e}"))
        

""" 

   -This function accepts a csv file path of current records
   and inserts them into the db 
   -The source of the data doesnt matter so long as it matches the format specified for current vehicle listings -> YEAR,MAKE,MODEL,LISTPRICE
"""
def insert_current_listing_data(cur,conn,cleaned_CURRENT_LISTINGS_file_path):
    print(chalk.green(":::Starting insert_current_listing_data"))
    clean_output_file_CURRENT_LISTINGS = open(cleaned_CURRENT_LISTINGS_file_path,"r")
    csvreader = csv.reader(clean_output_file_CURRENT_LISTINGS,delimiter=',')
    # this skips the first line in file which is col names
    next(csvreader)
    for line in csvreader:  
        # print(line)
        line_uppercase = [value.upper() for value in line]
        try:
            sql = """
                INSERT INTO CURRENT_LISTINGS(YEAR,MAKE,MODEL,LISTPRICE)
                VALUES(%s,%s,%s,%s)
                """
            cur.execute(sql,line_uppercase)
        except (Exception, psycopg2.DatabaseError) as e:
            print(chalk.red(f"error: {e}"))

    try:
        conn.commit()
        print(chalk.green(":::Successfully inserted all CURRENT_LISTING records into DB"))
    except Exception as e:
            print(chalk.red(f"Failed to insert current data: {e}"))


def LTR_insert_curr_listings():

    LTR_EBAY_ROOT = os.path.join(LTR_ROOT_DIR,'EBAY')
    """
        This function will user insert_current_listing_data()
        to insert data into DB from files in LTR storage for current listings

        -Will need path to LTR EBAY -> Longterm_prev_scrapes/EBAY
        -Then parse file name
            - determine if file is curr or sold
            - extract vehicle name, and scrape data
        - build query string and insert into db
    """

    for dirs,path,file in os.walk(LTR_EBAY_ROOT):

        """
            file name format:
              EBAY__CURR__03-22-2024__NISSAN-350Z.txt 
              OR 
              EBAY__SOLD__03-22-2024__NISSAN-350Z.txt
        """
      
        tokens = file.split("__")

        #token [1] will be CURR or SOLD
        listing_type = tokens[1]

        #token[2] is date
        scrape_date = tokens[3]

        #token[3] is make and model, which will need to split at "-"
        make,model = token[3].split("-")

        print(f"${listing_type} ${scrape_date} ${make} ${model}")


    
""" 
   -This function performs a test query to check that the data was inserted correctly
"""
def insertion_check(cur,table):
    try:
        sql = f"SELECT * FROM {table}"
        cur.execute(sql)
        rows = cur.fetchall()
        print(chalk.green(f"BEGIN RESULTS FOR ${table}"))
        for row in rows:
            print(row)
        print(chalk.green(f"END RESULTS FOR ${table}"))

    except(Exception,psycopg2.DatabaseError) as e:
        print(chalk.red(f"COULDNT RETRIEVE RECORDS FOR {table} - error: {e}"))

        
        


# def data_insertion_runner():

#     clean_output_file_CURRENT_LISTINGS = open(cleaned_CURRENT_LISTINGS_file_path,"r")
#     csvreader = csv.reader(clean_output_file_CURRENT_LISTINGS,delimiter=',')

if __name__ == '__main__':
    

    veh = {
        'year':2017,
        'make':'Ferrari',
        'model':'458'
    }
    conn = psycopg2.connect(os.getenv('DB_URI'))
    cur = conn.cursor()
    populate_vehicles_dir_table(cur, INPUT_veh_dir_file_path)
    insert_new_scraped_veh_VEH_DIR(cur,conn,veh)
    insert_sold_data(cur,conn, clean_SOLD_LISTINGS_file)
    insert_current_listing_data(cur, conn,clean_CURR_LISTINGS_file)
    
    #insertion check of tables
    insertion_check(cur,"VEHICLES")
    insertion_check(cur,"SOLD_LISTINGS")
    insertion_check(cur,"CURRENT_LISTINGS")
    conn.close()
    

