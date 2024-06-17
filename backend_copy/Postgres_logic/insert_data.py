"""insert_data.py

This script inserts data from file into db
-Reads in data from csv file
-writes to db
-has function to check if data was persisted correctly

"""



import psycopg2
import os,sys
import csv
#from dotenv import load_dotenv,find_dotenv
from simple_chalk import chalk
from datetime import date,datetime

#get parent dir 'backend_copy' from current script dir - append to sys.path to be searched for modules we import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.isdir(parent_dir))

# Add the directory to sys.path
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import DB_URI
from Data_Clean_Logic import clean_ebay_data


postgres_dir = os.path.dirname(__file__)
#directory of 'this' file
current_script_dir = os.path.dirname(os.path.abspath(__file__))
#print(os.path.isdir(current_script_dir))

#get ref to project root
PROJ_ROOT = os.path.abspath(os.path.join(current_script_dir,'..'))


#dir of cleaned data
CLEANED_DATA_DIR = os.path.join(PROJ_ROOT,'Cleaned_data_output')
#print(chalk.green(f"CLEANED_DATA_DIR: {os.path.isdir(CLEANED_DATA_DIR)}"))

INPUT_veh_dir_file_path = os.path.join(postgres_dir,'..','vehicle_directory.csv')

clean_CURR_LISTINGS_file = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_CURRENT_LISTINGS.csv')
clean_SOLD_LISTINGS_file = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_SOLD_DATA.csv')

LTR_ROOT_DIR = os.path.join(PROJ_ROOT,'LongTerm_prev_scrapes') 
#print(chalk.green(f"LTR_ROOT_DIR: {os.path.isdir(LTR_ROOT_DIR)}"))

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

    #scrape_date will be populated if its coming from parsed filename - probably from LTR storage
    veh_scrape_date = veh['scrape_date']
    
    #if scrape_date is None, this means this function being called for freshly scraped veh 
    #and not for a parsed filename insertion - so we grab the current date as scrape date
    if veh_scrape_date != None:
        veh_scrape_date = curr_date = (datetime.today()).strftime("%m-%d-%Y") #get curr date as scrape date

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

   -This function accepts a csv file path, reads data from it and inserts it into the db 
   -The source of the data doesnt matter so long as it matches the format specified for current vehicle listings -> YEAR,MAKE,MODEL,LISTPRICE
"""
def insert_current_listing_data(cur,conn,input_data,flag):
    print(chalk.green(":::Starting insert_current_listing_data"))

    if flag == 1:
        #call clean curr data and pass file path
        print(clean_ebay_data.clean_data_EBAY_CURRENT(input_data,1))
        print(chalk.green("::: INPUT IS LTR RAW DATA -"))
        print(chalk.green("::: SENDING FOR CLEANING -"))
        print(chalk.green("::: CLEANED-"))
        clean_output_file_CURRENT_LISTINGS = open(cleaned_CURRENT_LISTINGS_file_path,"r")
    else:
        print(chalk.green("::: INPUT IS FRESH SCRAPE - ALREADY CLEANED-"))
        clean_output_file_CURRENT_LISTINGS = open(cleaned_CURRENT_LISTINGS_file_path,"r")

    clean_output_file_CURRENT_LISTINGS = open(cleaned_CURRENT_LISTINGS_file_path,"r")

    # if os.path.isfile(input_data)
    #     line_reader = csv.reader(clean_output_file_CURRENT_LISTINGS,delimiter=',')
    #     # this skips the first line in file which is col names
    # else:

    # next(line_reader)
    # for line in line_reader:  
    #     # print(line)
    #     line_uppercase = [value.upper() for value in line]
    #     try:
    #         sql = """
    #             INSERT INTO CURRENT_LISTINGS(YEAR,MAKE,MODEL,LISTPRICE)
    #             VALUES(%s,%s,%s,%s)
    #             """
    #         cur.execute(sql,line_uppercase)
    #     except (Exception, psycopg2.DatabaseError) as e:
    #         print(chalk.red(f"error: {e}"))

    # try:
    #     conn.commit()
    #     print(chalk.green(":::Successfully inserted all CURRENT_LISTING records into DB"))
    # except Exception as e:
    #         print(chalk.red(f"Failed to insert current data: {e}"))



def tokenize_filename(filename):
    tokens = file.split("__")

    #token [1]  will be CURR or SOLD
    listing_type = tokens[1]
    #
    token[2] is date
    scrape_date = tokens[3]
    
    #token[3] is make and model, which will need to split at "-"
    make,model = token[3].split("-")
    print(f"${listing_type} ${scrape_date} ${make} ${model}")
    
    return (listing_type,make,model,scrape_date)


def parse_filename_generator(basedir):
    """

        This generator function is called as needed
        for each file, it passes the file to tokenize_filename()
        and recieves back the to
        file names look like: 
        EBAY__CURR__03-20-2024__PORSCHE-911.txt - or - EBAY__SOLD__03-20-2024__PORSCHE-911.txt
        
    """
    for root,dirs,files in os.walk(basedir):
        for file in files:
            info = tokenize_filename(file)
            if info:
                yield info





def LTR_insertion_driver(cur,conn):


    """ Function Notes:

        DIR STRUCTURE OF LongTerm_prev_scrapes


            LongTerm_prev_scrapes/
                 /EBAY
                    /CURR
                        -EBAY__CURR__03-20-2024__PORSCHE-911.txt 
                    /SOLD 
                        -EBAY__SOLD__03-20-2024__PORSCHE-911.txt
                 /BAT
            
            
        extracting file names from files in EBAY/CURR and EBAY/SOLD to populate vehdir table

    """

    #/home/ubuntu/Documents/Projectsz/EuroClassic/backend_copy/Longterm_prev_scrapes/EBAY
    LTR_EBAY_ROOT = os.path.join(LTR_ROOT_DIR,'EBAY')
    #print(os.path.isdir(LTR_EBAY_ROOT))
    batch_filenames = []
    batch_size = 30
    for info in parse_filename_generator(LTR_EBAY_ROOT):

        listing_type,make,model,scrape_date = info
        veh = {
                 'year':year,
                 'make':model,
                 'scrape_date':scrape_date
              }

        #insert parsed filename as new entry in vehdir table
        insert_new_scraped_veh_VEH_DIR(cur,conn,veh)


        #insert file contents to corresponding table
        if listing_type == "sold":
           pass
        elif listing_type == "curr":
            insert_current_listing_data(cur,conn,file_contents)

        """
            if size of sold or curr list exceed batch size threschold
                go on to insert this batch into db
                clear list that was inserted ahead of appending next batch
        """
        if sold.size >= batch_size:
            batch_insert(sold_listings,"SOLD_LISTINGS")
        elif curr.size >= batch_size:
            batch_insert(curr_listings)

        batch_insert(sold_listings)

    

"""

    when on a filename:
        -parse out the filename, this is for vehdir entry
        -open file and load contents in mem as list
        -write parsed filename to vehdir table
        -write contents for this file to corresponding listing table
 
        the point of this is to insert filename into vehdir and also the records of that file
        for each file
        
        EBAY__CURR__03-20-2024__PORSCHE-911.txt  is file name
         |   (inside file we have the data)
         |   
         |    :::EBAY - CURRENT DATA SCRAPED ON: 03-20-2024 
         |   Shop on eBay $20.00
         |   1985 Porsche 911 $18,500.00
         |   2005 Porsche 911 Carrera 997 $25,900.00
         |   1971 Porsche 911 wide body $20,000.00
         |   1967 Porsche 911 Coupe $6,700.00
         |   1911 Porsche 911 $4,050.00

        we need to inser this information into the corresponding table as well

        in generator function 
            call function to parse filename
            call another function read lines into a list 
            yield parsed file name, yield list with file_contents?

        back in driver function
            
            recieve objects from generator

            #insert filename into vehdir 
            batch_insert_filename_vehdir((listing_type,make,model,scrape_date))

            if listing_type == curr:
                #insert the files contents to corresponding table depending on listing_type
                batch_insert_records_curr(file_contents)
                
                #clear list holding file_contents ahead of next file
                file_contents.clear()

            elif listing_type == sold:
                #insert the files contents to corresponding table depending on listing_type
                batch_insert_records_curr(file_contents
                #clear list holding file_contents ahead of next file
                file_contents.clear()
"""

        


    
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
    conn = psycopg2.connect(DB_URI)
    cur = conn.cursor()
    # populate_vehicles_dir_table(cur, INPUT_veh_dir_file_path)
    # insert_new_scraped_veh_VEH_DIR(cur,conn,veh)
    # insert_sold_data(cur,conn, clean_SOLD_LISTINGS_file)
    # insert_current_listing_data(cur, conn,clean_CURR_LISTINGS_file)
    
    # LTR_insert_curr_listings()


    # #create filename of output file to be used 
    # #take input file name and append "_CLEANED to it"
    # LTS_clean_output_file = raw_CURRENT_LISTINGS_file + "_CLEANED"
    # print(chalk.green(f"OUTPUT FILE NAME {LTS_clean_output_file}"))

    # #LTS/EBAY/CURR/CLEANED/<file_name_CLEANED>
    # LTS_clean_output_file_path = os.path.join(CLEANED_DEST_DIR,LTS_clean_output_file)
    # print(chalk.green(f"OUTPUT FILE PATH {LTS_clean_output_file_path} "))
        
    TEST_prev_CURR_path = os.path.join(os.path.dirname(__file__),'..','LongTerm_prev_scrapes/EBAY','EBAY__CURR__05-03-2024__PORSCHE-PANAMERA.txt')    
    insert_current_listing_data(cur,conn,TEST_prev_CURR_path,1)


    #insertion check of tables
    # insertion_check(cur,"VEHICLES")
    # insertion_check(cur,"SOLD_LISTINGS")
    # insertion_check(cur,"CURRENT_LISTINGS")
    conn.close()
    

