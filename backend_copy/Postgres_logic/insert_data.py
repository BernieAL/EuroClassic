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
    if veh_scrape_date == None:
        veh_scrape_date = (datetime.today()).strftime("%m-%d-%Y") #get curr date as scrape date

    sql =   """
            INSERT INTO VEHICLES(YEAR,MAKE,MODEL,LAST_SCRAPE_DATE)
            VALUES(%s,%s,%s,%s)
            """ 
    try:
        cur.execute(sql,(veh_year,veh_make,veh_model,veh_scrape_date))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as e:
         print(chalk.red(f"Failed to insert veh into veh dir: {e}"))

    print(chalk.green(":::Successfully INSERTED NEWLY SCRAPED VEH into VEH DIR TABLE"))




"""
   -This function accepts a csv file path of sold records
   and inserts them into the db 
   -The source of the data doesnt matter so long as it matches the format specified for sold vehicles records -> YEAR,MAKE,MODEL,SALEPRICE,DATESOLD
"""
def insert_sold_listing_data(cur,conn,input_data,flag=0):
    print(chalk.green(":::Starting insert_sold_data"))


    print(chalk.green(f"input data {input_data}"))
    print(os.path.isfile(input_data))
    try:
        #if flag == 1, being called from LTS process
        if flag == 1:
            #call clean_sold_data and pass input file path, recieve file path of newly created cleaned data
            LTR_created_file_path = clean_ebay_data.clean_data_EBAY_SOLD(veh,input_data,1)

            print(chalk.green(f"::: REC'D OUTPUT FILE PATH FOR CLEANED DATA: {LTR_created_file_path}"))
            print(chalk.green("::: INPUT IS LTR RAW DATA -"))
            print(chalk.green("::: SENDING FOR CLEANING -"))
            print(chalk.green("::: CLEANED- "))

            #open ltr/ebay/sodl/cleaned/<file_name>
            clean_output_file_SOLD_LISTINGS = open(LTR_created_file_path,"r",encoding="utf-8")

        #if flag == 0, being called from fresh scrape process   
        else:
            print(chalk.green("::: INPUT IS FRESH SCRAPE - ALREADY CLEANED-"))
            clean_output_file_SOLD_LISTINGS = open(clean_SOLD_LISTINGS_file,"r",encoding="utf-8")

        line_reader = csv.reader(clean_output_file_SOLD_LISTINGS ,delimiter=',')
        # this skips the first line in file which is col names
        next(line_reader)
        for line in line_reader:  
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
    except Exception as e:
        print(chalk.red(f"Failed to read lines from file: {e}"))
    try:
        conn.commit()
        print(chalk.green(":::Successfully inserted all SOLD_LISTINGS records into DB"))
    except Exception as e:
        print(chalk.red(f"Failed to insert sold data: {e}"))
        

""" 

   -This function accepts a csv file path, reads data from it and inserts it into the db 
   -The source of the data doesnt matter so long as it matches the format specified for current vehicle listings -> YEAR,MAKE,MODEL,LISTPRICE
"""
def insert_current_listing_data(cur,conn,input_data,flag=0):
    print(chalk.green(":::Starting insert_current_listing_data"))

    print(chalk.green(f"input data {input_data}"))
    print(os.path.isfile(input_data))

    #if flag == 1, being called from LTS process
    if flag == 1:
        #call clean_curr_data and pass input file path, recieve file path of newly created cleaned data
        LTR_created_file_path = clean_ebay_data.clean_data_EBAY_CURRENT(veh,input_data,1)


        print(chalk.green(f"::: REC'D OUTPUT FILE PATH FOR CLEANED DATA: {LTR_created_file_path}"))
        print(chalk.green("::: INPUT IS LTR RAW DATA -"))
        print(chalk.green("::: SENDING FOR CLEANING -"))
        print(chalk.green("::: CLEANED- "))

        #open ltr/ebay/curr/cleaned/<file_name>
        clean_output_file_CURRENT_LISTINGS = open(LTR_created_file_path,"r",encoding="utf-8")
    else:
        print(chalk.green("::: INPUT IS FRESH SCRAPE - ALREADY CLEANED-"))
        clean_output_file_CURRENT_LISTINGS = open(clean_CURR_LISTINGS_file,"r",encoding="utf-8")

    
    line_reader = csv.reader(clean_output_file_CURRENT_LISTINGS,delimiter=',')
    next(line_reader)
    for line in line_reader:  
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



def tokenize_filename(filename):

    """
        Works FOR BOTH SOLD AND CURR
    """
    try:
        tokens = filename.split("__")

        #token [1]  will be CURR or SOLD
        listing_type = tokens[1].upper()
        #
        #tokens[2] is date
        scrape_date = tokens[2]
        
        #token[3] is "make-model.txt", first strip ".txt" then split at "-" to get make and model
        make,model = ((tokens[3].rstrip(".txt")).upper()).split("-")
        # print(f"TEST:{listing_type} {scrape_date} {make} {model}")
        return (listing_type,make,model,scrape_date)
    except Exception as e:
        print(chalk.green(f"(tokenize_filename) Error tokenizing {filename}"))


def parse_filename_generator(basedir):
    """
        WORKS FOR BOTH SOLD AND CURR
        This generator function is called as needed
        for each file, it passes the file to tokenize_filename()
        and recieves back the to
        file names look like: 
        EBAY__CURR__03-20-2024__PORSCHE-911.txt - or - EBAY__SOLD__03-20-2024__PORSCHE-911.txt
        
    """

    skip_dirs = {'EBAY/SOLD/CLEANED','EBAY/CURR/CLEANED'}
    try:
        # max_files = 10
        # file_count = 0
        
        for root,dirs,files in os.walk(basedir):
            
            #modify dirs in place to skip specific dirs
            #return list of dirs that are not found in skip dirs
            #dirs[:] is slice operation that refers to all element of the list
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for dir in dirs:

                subdir_path = os.path.join(root,dir)
                for subdir_root,subdir_dirs, subdir_files in os.walk(subdir_path):
                    for file in subdir_files:
                        # print(os.path.join(subdir_root,file))
                
                        #full path of curr file from root
                        filepath = os.path.join(root,file)
                        filename_tokens = tokenize_filename(file) #listing_type,make,model,scrape_date
                        # print(filename_tokens)
                        if filename_tokens:
                            #yield parsed file and original file path - original file path will be needed in db insertion function
                            yield {
                                    "filename_tokens":filename_tokens,
                                    "filepath": filepath
                                } 
                
            #     # file_count +=1
            #     # if file_count == 10:
            #     #     return

    except Exception as e:
        print(chalk.green(f"(parse_filename_generator) Error {e}"))

#TESTING parse_filename_generator
# LTR_EBAY_ROOT = os.path.join(LTR_ROOT_DIR,'EBAY')
# for res in parse_filename_generator(LTR_EBAY_ROOT):
#     print(f"{res} \n --------------")




def LTR_insertion_driver(cur,conn):


    """Function Notes:
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

    try:
        #/home/ubuntu/Documents/Projectsz/EuroClassic/backend_copy/Longterm_prev_scrapes/EBAY
        LTR_EBAY_ROOT = os.path.join(LTR_ROOT_DIR,'EBAY')
        #print(os.path.isdir(LTR_EBAY_ROOT))
        batch_filenames = []
        batch_size = 30

        #for each parsed_filename returned from generator
        for res in parse_filename_generator(LTR_EBAY_ROOT):

            listing_type,make,model,scrape_date = res["filename_tokens"]
            
            curr_filepath = res["filepath"]
            # print(res["filename_tokens"])
            # print(f"curr_filepath {curr_filepath}")

            
            veh = {
                     "year":0000,
                     "make":make,
                     "model": model,
                     "scrape_date":scrape_date
                  }

            #insert parsed filename as new entry in vehdir table
            # insert_new_scraped_veh_VEH_DIR(cur,conn,veh)


            #insert file data into to corresponding table
            if listing_type == "SOLD":
                # print(res["filename_tokens"])
                pass
                # print(chalk.green(f"listing type is SOLD - inserting to SOLD table"))
                # insert_sold_listing_data(cur,conn,curr_filepath,1)
            elif listing_type == "CURR":
                # pass
                # print(chalk.green(f"listing type is CURR - inserting to CURR table"))
                insert_current_listing_data(cur,conn,curr_filepath,1)
    except Exception as e:
            print(chalk.red(f"Error {e}"))

        # """
        #     if size of sold or curr list exceed batch size threschold
        #         go on to insert this batch into db
        #         clear list that was inserted ahead of appending next batch
        # """
        # if sold.size >= batch_size:
        #     batch_insert(sold_listings,"SOLD_LISTINGS")
        # elif curr.size >= batch_size:
        #     batch_insert(curr_listings)

        # batch_insert(sold_listings)

    

"""when on a filename:
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
        'make':'NISSAN',
        'model':'ALTIMA'
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
        
    # TEST_prev_CURR_file = os.path.join(LTR_ROOT_DIR,"EBAY/CURR","EBAY__CURR__03-28-2024__NISSAN-ALTIMA.txt")
    # print(TEST_prev_CURR_file)
    # insert_current_listing_data(cur,conn,TEST_prev_CURR_file,1)

    # TEST_prev_CURR_file = os.path.join(LTR_ROOT_DIR,"EBAY/CURR","EBAY__CURR__03-28-2024__NISSAN-ALTIMA.txt")
    # print(TEST_prev_CURR_file)
    # insert_current_listing_data(cur,conn,TEST_prev_CURR_file,1)


    # LTR_insertion_driver(cur,conn)

    #insertion check of tables
    # insertion_check(cur,"VEHICLES")
    # insertion_check(cur,"SOLD_LISTINGS")
    # insertion_check(cur,"CURRENT_LISTINGS")
    conn.close()
    

