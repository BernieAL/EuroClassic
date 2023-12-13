"""

insert_data.py

This script inserts data from file into db
-Reads in data from csv file
-writes to db
-has function to check if data was persisted correctly

"""



import psycopg2
from config import config
import os
import csv




def populate_vehicles_table(cur,veh_dir_file_path):
    
    veh_dir_data = open(veh_dir_file_path,"r")
    csvreader = csv.reader(veh_dir_data,delimiter=',')

    # this skips the first line in file which is col names
    next(csvreader)
    for line in csvreader:
        try:
            sql = """
                INSERT INTO vehicles(make,model,year,last_scrape_date)
                values(%s,%s,%s,%s)
                """
            cur.execute(sql,line)
            
        except (Exception, psycopg2.DatabaseError) as e:
            print(f"error: {e}")

    print("Successfully inserted all vehicles into DB")
    conn.commit()

def insert_sold_data(cur,clean_output_SOLD_DATA_file_path):
    
    clean_output_file_SOLD_DATA = open(clean_output_SOLD_DATA_file_path,"r")
    csvreader = csv.reader(clean_output_file_SOLD_DATA,delimiter=',')
    # this skips the first line in file which is col names
    next(csvreader)
    for line in csvreader:  
        # print(line)
        try:
            sql = """
                INSERT INTO sold_listings(year,make,model,saleprice,datesold)
                VALUES(%s,%s,%s,%s,%s)
                """
            cur.execute(sql,line)
        except (Exception, psycopg2.DatabaseError) as e:
            print(f"error: {e}")

    print("Successfully inserted all SOLD_LISTINGS records into DB")
    conn.commit()

def insert_current_listing_data(cur,clean_output_file_CURRENT_LISTINGS_file_path):
    
    clean_output_file_CURRENT_LISTINGS = open(clean_output_file_CURRENT_LISTINGS_file_path,"r")
    csvreader = csv.reader(clean_output_file_CURRENT_LISTINGS,delimiter=',')
    # this skips the first line in file which is col names
    next(csvreader)
    for line in csvreader:  
        # print(line)
        try:
            sql = """
                INSERT INTO current_listings(year,make,model,listPrice)
                VALUES(%s,%s,%s,%s)
                """
            cur.execute(sql,line)
        except (Exception, psycopg2.DatabaseError) as e:
            print(f"error: {e}")

    print("Successfully inserted all CURRENT_LISTING records into DB")
    conn.commit()

    

def insertion_check(cur):
    try:
        sql = """
            SELECT * FROM sold_listings
            """
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print(row)

    except(Exception,psycopg2.DatabaseError) as e:
        print(f"error: {e}")

        conn.close()
        



postgres_dir = os.path.dirname(__file__)


INPUT_veh_dir_file_path = os.path.join(postgres_dir,'..','vehicle_directory.csv')
print('VEH DIR FILE PATH '  + INPUT_veh_dir_file_path)

# clean_output_file_SOLD_DATA_file_path = os.path.join(postgres_dir,'..','cleaned_data_SOLD_DATA.csv')
# print('SOLD_DATA FILE PATH'  + clean_output_file_SOLD_DATA_file_path)

#Using dummy data
clean_output_file_SOLD_DATA_file_path = os.path.join(postgres_dir,'..','Dummy_data_generator/sold_listings_dummy.csv')
print('SOLD_DATA FILE PATH'  + clean_output_file_SOLD_DATA_file_path)

clean_output_file_CURRENT_LISTINGS_file_path = os.path.join(postgres_dir,'..','Dummy_data_generator/current_listings_dummy.csv')
print('SOLD_DATA FILE PATH'  + clean_output_file_CURRENT_LISTINGS_file_path)




if __name__ == '__main__':
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    populate_vehicles_table(cur,INPUT_veh_dir_file_path)
    insert_sold_data(cur,clean_output_file_SOLD_DATA_file_path)
    insert_current_listing_data(cur,clean_output_file_CURRENT_LISTINGS_file_path)
    # insertion_check(cur)