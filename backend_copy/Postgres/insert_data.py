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


clean_CURR_LISTINGS_file = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_data_CURRENT_LISTINGS.csv')
clean_SOLD_LISTINGS_file = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_SOLD_DATA.csv')



# #TESTING - USING DUMMY DATA
# clean_output_file_SOLD_DATA_file_path = os.path.join(postgres_dir,'..','Dummy_data_generator/sold_listings_dummy.csv')
# print('SOLD_DATA FILE PATH'  + clean_output_file_SOLD_DATA_file_path)

# clean_output_file_CURRENT_LISTINGS_file_path = os.path.join(postgres_dir,'..','Dummy_data_generator/current_listings_dummy.csv')
# print('SOLD_DATA FILE PATH'  + clean_output_file_CURRENT_LISTINGS_file_path)



"""
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
                values(%s,%s,%s,%s)
                """
            cur.execute(sql,line_uppercase)
            
        except (Exception, psycopg2.DatabaseError) as e:
            print(f"error: {e}")

    print(":::Successfully POPULATED VEH DIR TABLE")
    conn.commit()


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
            print(f"error: {e}")

    try:
        conn.commit()
        print(chalk.green(":::Successfully inserted all SOLD_LISTINGS records into DB"))
    except Exception as e:
        print(f"Failed to insert sold data: {e}")
        

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
        try:
            sql = """
                INSERT INTO CURRENT_LISTINGS(YEAR,MAKE,MODEL,LISTPRICE)
                VALUES(%s,%s,%s,%s)
                """
            cur.execute(sql,line)
        except (Exception, psycopg2.DatabaseError) as e:
            print(f"error: {e}")

    try:
        conn.commit()
        print(chalk.green(":::Successfully inserted all CURRENT_LISTING records into DB"))
    except Exception as e:
            print(f"Failed to insert current data: {e}")

    
""" 
   -This function performs a test query to check that the data was inserted correctly
"""
def insertion_check(cur):
    try:
        sql = """
            SELECT * FROM sold_listings;
            SELECT * FROM current_listings
            """
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)

    except(Exception,psycopg2.DatabaseError) as e:
        print(f"error: {e}")

        conn.close()
        


# def data_insertion_runner():

#     clean_output_file_CURRENT_LISTINGS = open(cleaned_CURRENT_LISTINGS_file_path,"r")
#     csvreader = csv.reader(clean_output_file_CURRENT_LISTINGS,delimiter=',')

if __name__ == '__main__':
    
    conn = psycopg2.connect(os.getenv('DB_URI'))
    cur = conn.cursor()
    populate_vehicles_dir_table(cur, INPUT_veh_dir_file_path)
    # insert_sold_data(cur, clean_SOLD_LISTINGS_file_path)
    # insert_current_listing_data(cur, clean_CURR_LISTINGS_file_path)
    insertion_check(cur)