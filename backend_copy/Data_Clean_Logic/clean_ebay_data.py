import logging
import re
import os
from simple_chalk import chalk
import gzip
import json
from pathlib import Path

#directory of 'this' file
current_script_dir = os.path.dirname(os.path.abspath(__file__))

#get ref to project root
PROJ_ROOT = os.path.abspath(os.path.join(current_script_dir,'..'))

LTS_DIR_EBAY_ROOT = os.path.join(PROJ_ROOT,'LongTerm_prev_scrapes/EBAY') 

#dir of raw extracted data
SCRAPED_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'Scraped_data_output')

#dir of cleaned data
CLEANED_DATA_DIR = os.path.join(PROJ_ROOT,'Cleaned_data_output')

#INPUT get ref to ebay raw current and raw sold listings files
EBAY_raw_CURRENT_LISTINGS_file = os.path.join(SCRAPED_DATA_DIR, 'EBAY_raw_CURRENT_LISTINGS_DATA.txt')
EBAY_raw_SOLD_DATA_file = os.path.join(SCRAPED_DATA_DIR, 'EBAY_raw_SOLD_DATA.txt')

#OUTPUT get ref to output file
EBAY_clean_OUTPUT_CURRENT_LISTINGS_file = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_CURRENT_LISTINGS.csv')
EBAY_clean_OUTPUT_SOLD_DATA_file = os.path.join(CLEANED_DATA_DIR,'EBAY_cleaned_SOLD_DATA.csv')


# get path to central logging file, and pass into config
api_log_file_path = os.path.join(os.path.dirname(__file__),'..','api_log.txt')

# custom logger to avoid interacting with selenium using debug level wire
logger = logging.getLogger('CLEAN_EBAY_SCRIPT')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(api_log_file_path)
formatter = logging.Formatter('%(asctime)s - CLEAN_EBAY_DATA -  %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)



def fileWrite(data, fileIn):
    for line in data:
        temp = f"{line}\n"
        fileIn.write(temp)
    # fileIn.write("---------------------- \n")



"""
If flag is 0 (by default) this function is being called on newly scraped data
If flag is 1, this function is being called on LTS data (Longterm-storage,prev scraped data)
    And the output file name will be the name of the input file, appended with CLEANED
    and it will be stored in LTS/EBAY/CURR/CLEANED
"""

def clean_data_EBAY_CURRENT(car,raw_CURRENT_LISTINGS_file,flag=0):

    logger.debug("ENTERED - clean_data_EBAY_CURRENT")
    logger.debug("PARAMS REC'D car: %s  raw input file: %s",json.dumps(car),raw_CURRENT_LISTINGS_file)
    
    if flag == 1:
       
        print(LTS_DIR_EBAY_ROOT + "\n")
        print(chalk.green("FLAG REC'D == 1, DATA IS FROM LTS (PREV SCRAPED)"))

        # Create LTS/EBAY/CURR/CLEANED if it doesn't exist
        EBAY_CURR_CLEANED_DIR = Path(LTS_DIR_EBAY_ROOT) / 'CURR' / 'CLEANED'
        print(chalk.green(f"ebay curr cleaned dir::: {EBAY_CURR_CLEANED_DIR}\n"))

        if not EBAY_CURR_CLEANED_DIR.exists():
            EBAY_CURR_CLEANED_DIR.mkdir(parents=True, exist_ok=True)
            print(chalk.green(f"Created directory: {EBAY_CURR_CLEANED_DIR}\n"))
        else:
            print(chalk.green(f"DIR EXISTS: {EBAY_CURR_CLEANED_DIR}"))

        # Create filename of output file to be used
        raw_file_path = Path(raw_CURRENT_LISTINGS_file)
        cleaned_file_name = raw_file_path.stem + "_CLEANED" + raw_file_path.suffix
        
        # Construct the full path for the cleaned file
        LTS_clean_output_file_path = EBAY_CURR_CLEANED_DIR / cleaned_file_name
        print(chalk.green(f"OUTPUT FILE PATH {LTS_clean_output_file_path} "))
        clean_output_file_CURRENT_LISTINGS = open(LTS_clean_output_file_path,'w',encoding="utf-8")

    # else:
    #     #open output file for writing clean data
    #     clean_output_file_CURRENT_LISTINGS = open(EBAY_clean_OUTPUT_CURRENT_LISTINGS_file, "w", encoding="utf-8")
           
    try:
        print(chalk.red("(clean_ebay_data) - CLEAN CURR DATA"))
        
        #open raw data file
        raw_input_CURRENT_LISTINGS = open(raw_CURRENT_LISTINGS_file, "r", encoding="utf-8")
        raw_data = raw_input_CURRENT_LISTINGS


        year = car['year']
        make = car['make']
        model = car['model']
        print(make)
        print(model)

        #for writing cleaned concatenated strings 
        clean_output_array = []


        for line in raw_data:
            
            #print(f"raw current data line: {line}")
            
            #only process lines that contain the specific model requested.
            if model in line:
                #remove all commas in raw line - if any
                line = line.replace(',', '')

                #find all groups of 4 digits in curr line
                if re.findall('^\d{4}', line):
                    try:
                        #the first in returned group should be the year
                        year = (re.findall('^\d{4}', line))[0]
                    except NameError:
                        #for any reason, year not found, default to 0000
                        year = 0000
                        logger.debug("COULD NOT LOCATE YEAR IN LINE - DEFAULTING TO '0000' %s ", line)


                #locate the price by locating '$' and ending at decimal point
                #Ex input = $28000.00 -> output 28000
                try:
                    price = (re.findall('\$\d[0-9][0-9].+', line))[0]
                    if not year:
                        year = 0000
                    price = price.replace('$', '')
                except IndexError as error:
                    logger.debug("COULD NOT LOCATE PRICE IN LINE %s ", line)
                    pass

                #concat into single line for to write to csv output file -> 1999,Acura,Integra,28000
                item_line = f"{year},{make},{model},{price}"

                #append cleaned line to array
                clean_output_array.append(item_line)




        col_headers = f"Year,Make,Model,Price\n"
        clean_output_file_CURRENT_LISTINGS.write(col_headers)

        fileWrite(clean_output_array, clean_output_file_CURRENT_LISTINGS)
        logger.debug("WRITING CLEANED CURRENT LISTINGS TO OUTPUT FILE")

        logger.debug("DATA CLEANING FOR CURRENT_LISTINGS successful")
        print(chalk.green((":::DATA CLEANING FOR CURRENT_LISTINGS successful")))
        logger.debug("EXITING - clean_data_EBAY_CURRENT")
        return LTS_clean_output_file_path

    except Exception as e:
        logger.debug(f":::Error during data cleaning for CURRENT_LISTINGS: {str(e)}")
        print(chalk.red(f":::Error during data cleaning for CURRENT_LISTINGS: {str(e)}"))


def clean_data_EBAY_SOLD(car,raw_SOLD_LISTINGS_file,flag=0):
    
    logger.debug("ENTERED - clean_data_EBAY_SOLD")
    logger.debug("PARAMS REC'D car: %s  raw input file: %s",json.dumps(car),raw_SOLD_LISTINGS_file)
    


    # print(chalk.green(f"(clean_data_EBAY_sold) {os.path.isfile(raw_SOLD_LISTINGS_file)}"))
    print(chalk.yellow(f"raw_SOLD_LISTINGS_file {raw_SOLD_LISTINGS_file}"))
    

    if flag == 1:
        # print(LTS_DIR_EBAY_ROOT + "\n")
        print(chalk.green("FLAG REC'D == 1, DATA IS FROM LTS (PREV SCRAPED)"))

        # Create LTS/EBAY/CURR/CLEANED if it doesn't exist
        EBAY_SOLD_CLEANED_DIR = Path(LTS_DIR_EBAY_ROOT) / 'SOLD' / 'CLEANED'
        #print(chalk.green(chalk.yellow(f"ebay sold cleaned dir::: {EBAY_SOLD_CLEANED_DIR}\n")))

        if not EBAY_SOLD_CLEANED_DIR.exists():
            EBAY_SOLD_CLEANED_DIR.mkdir(parents=True,exist_ok=True)
            print(chalk.green(f"Created directory: {EBAY_SOLD_CLEANED_DIR}\n"))
        else:
            print(chalk.green(f"DIR EXISTS: {EBAY_SOLD_CLEANED_DIR}"))

        # Create filename of output file to be used
        raw_file_path = Path(raw_SOLD_LISTINGS_file)
        print(str(raw_file_path))
        
        if "_CLEANED" in str(raw_file_path):
            print(chalk.red(f"file already has '_CLEANED' suffix {raw_file_path}"))
            cleaned_file_name = raw_file_path
        else:
            cleaned_file_name = raw_file_path.stem + "_CLEANED" + raw_file_path.suffix
            print(chalk.red(f"adding '_CLEANED' to file {raw_file_path}"))

        # Construct the full path for the cleaned file
        LTS_clean_output_file_path = EBAY_SOLD_CLEANED_DIR / cleaned_file_name
        print(chalk.green(f"OUTPUT FILE PATH {LTS_clean_output_file_path} "))
        clean_output_file_SOLD_LISTINGS = open(LTS_clean_output_file_path,'w',encoding="utf-8")
        
    try:
        print(chalk.red("(clean_ebay_data) - CLEAN SOLD DATA"))
        
        #open output file for writing clean data
        raw_input_SOLD_LISTINGS = open(raw_SOLD_LISTINGS_file, "r", encoding="utf-8")
        raw_data = raw_input_SOLD_LISTINGS

        year = car['year']
        make = car['make']
        model = car['model']
        print(make)
        print(model)

        clean_output_array = []
        
        #for each line in raw data
        #line looks like -> 2000 Acura Integra Type R $63966.00 2024-02-12
        for line in raw_data:

            # print(f"raw sold data line: {line}")

            #only process lines that contain the specific model requested.
            if model in line:
                #remove all commas in raw line - if any
                line = line.replace(',', '')
                
                #find all groups of 4 digits in curr line
                if re.findall('^\d{4}', line):
                    try:
                        #the first in returned group should be the year
                        veh_year = (re.findall('^\d{4}', line))[0]
                    except NameError:
                        #for any reason, year not found, default to 0000
                        veh_year = 0000
                        logger.debug("COULD NOT LOCATE YEAR IN LINE - DEFAULTING TO '0000' %s ", line)
                

                #locate the price by locating '$' and ending at decimal point
                #Ex input = $28000.00 -> output 28000
                try:
                    sale_price_match = (re.findall('\$(\d+)\.', line))[0]
                    if not veh_year:
                        veh_year = 0000
                    # print(sale_price_match)
                
                except IndexError as error:
                    logger.debug("COULD NOT LOCATE PRICE IN LINE %s ", line)
                    pass
                # print(f"{line}")
                try:
                    #extract date from line using pattern dddd-dd-dd , (where d is regex digit)
                    sale_date_match = (re.findall('\d{4}-\d{2}-\d{2}',line))[0]
                    
                    #concat into single line for to write to csv output file -> 1999,Acura,Integra,28000,2024-02-23
                    item_line = f"{veh_year},{make},{model},{sale_price_match},{sale_date_match}"
                    # print(item_line)
                    
                    #remove any spacing
                    item_line = item_line.replace(' ', '')
                    # print(item_line)
                    clean_output_array.append(item_line)

                except IndexError as error:
                    print(error)

        col_headers = f"Year,Make,Model,Price,DateSold\n"
        clean_output_file_SOLD_LISTINGS.write(col_headers)
        print(clean_output_array)
        fileWrite(clean_output_array, clean_output_file_SOLD_LISTINGS)

        clean_output_file_SOLD_LISTINGS.close()
        raw_input_SOLD_LISTINGS.close()

        logger.debug("WRITING CLEANED SOLD DATA TO OUTPUT FILE")
        logger.debug("DATA CLEANING FOR SOLD DATA successful")
        logger.debug("EXITING - clean_data_EBAY_SOLD")
        print(chalk.green(":::DATA CLEANING FOR SOLD_DATA successful"))
        return LTS_clean_output_file_path
    except Exception as e:
        logger.debug(f":::Error during data cleaning for SOLD_DATA: {str(e)}")
        print(chalk.red(f":::Error during data cleaning for SOLD_DATA: {str(e)} \n OFFENDING LINE--> {line}"))
        return e



def ebay_clean_data_runner(car,EBAY_raw_CURRENT_LISTINGS_file_path,EBAY_raw_SOLD_DATA_file_path):
    try:
        

        logger.debug("ENTERED - EBAY_CLEANED_DATA_RUNNER")
        
        # #TESTING WITH PREV SCRAPED DATA FROM LTS DIR TO AVOID LIVE SCRAPE
        # TEST_prev_SOLD_path = os.path.join(os.path.dirname(__file__),'..','LongTerm_prev_scrapes/EBAY','EBAY__SOLD__05-03-2024__NISSAN-350Z.txt')
        # TEST_prev_CURR_path = os.path.join(os.path.dirname(__file__),'..','LongTerm_prev_scrapes/EBAY','EBAY__CURR__05-03-2024__PORSCHE-PANAMERA.txt')
        # clean_data_EBAY_CURRENT(car,TEST_prev_CURR_path)
        # clean_data_EBAY_SOLD(car,TEST_prev_SOLD_path)       
        
        #lts test of cleaning data
        #using a LTS test for of curr and sold data
        # test_LTS_curr_file_path = os.path.join(LTS_DIR_EBAY_ROOT,"CURR/EBAY__CURR__03-20-2024__PORSCHE-911.txt")
        # clean_data_EBAY_CURRENT(car,test_LTS_curr_file_path,1)
        # test_LTS_sold_file_path = os.path.join(LTS_DIR_EBAY_ROOT,"SOLD/EBAY__SOLD_03-20-2024__PORSCHE-911.txt")
        # clean_data_EBAY_SOLD(car,test_LTS_sold_file_path,1)
        

        #NOT PART OF TESTING, UNCOMMENT FOR FULL RUN
        # clean_data_EBAY_CURRENT(car,EBAY_raw_CURRENT_LISTINGS_file_path)
        #clean_data_EBAY_SOLD(car,EBAY_raw_SOLD_DATA_file_path)       
        
        
        logger.debug("Data cleaning for all types successful")
        print("Data cleaning for all types successful")
        logger.debug("EXITING - EBAY_CLEANED_DATA_RUNNER")
        return True
    except Exception as e:
        logger.debug(f"Error during data cleaning for all types: {str(e)}")
        print(f"Error during data cleaning for all types: {str(e)}")
        return False

if __name__ == '__main__':
    car = {
        'year': 0000,
        'make': 'PORSCHE', #MUST BE CAPITALIZED OR WILL FAIL
        'model': '911' #MUST BE CAPITALIZED OR WILL FAIL
    }
    # ebay_clean_data_runner(car,EBAY_raw_CURRENT_LISTINGS_file,EBAY_raw_SOLD_DATA_file)

    # test_LTS_sold_file_path = os.path.join(LTS_DIR_EBAY_ROOT,"SOLD/EBAY__SOLD__03-28-2024__PORSCHE-911.txt")
    # clean_data_EBAY_SOLD(car,test_LTS_sold_file_path,1)
    # test_LTS_curr_file_path = os.path.join(LTS_DIR_EBAY_ROOT,"CURR/EBAY__CURR__03-20-2024__PORSCHE-911.txt")
    # clean_data_EBAY_CURRENT(car,test_LTS_curr_file_path,1)