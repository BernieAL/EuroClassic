import logging
import re
import os
from simple_chalk import chalk

# Configure logging
log_file_path = os.path.join(os.path.dirname(__file__), 'cleaning_log.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO)

#directory of 'this' file
current_script_dir = os.path.dirname(os.path.abspath(__file__))

#get ref to project root
PROJ_ROOT = os.path.abspath(os.path.join(current_script_dir,'..'))


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


clean_output_array = []

def fileWrite(data, fileIn):
    for line in data:
        temp = f"{line}\n"
        fileIn.write(temp)
    # fileIn.write("---------------------- \n")



def clean_data_EBAY_CURRENT(car,raw_CURRENT_LISTINGS_file):
    try:
        
        #open raw data file
        raw_input_CURRENT_LISTINGS = open(raw_CURRENT_LISTINGS_file, "r", encoding="utf-8")
        raw_data = raw_input_CURRENT_LISTINGS

        #open output file
        clean_output_file_CURRENT_LISTINGS = open(EBAY_clean_OUTPUT_CURRENT_LISTINGS_file, "w", encoding="utf-8")

        year = car['year']
        make = car['make']
        model = car['model']

        clean_output_array = []

        for line in raw_data:
            #if we find model in curr line
            if model in line:
                line = line.replace(',', '')
                #find all groups of 4 digits in curr line
                if re.findall('^\d{4}', line):
                    try:
                        #the first in returned group should be the year
                        year = (re.findall('^\d{4}', line))[0]
                    except NameError:
                        year = 0000

                try:
                    price = (re.findall('\$\d[0-9][0-9].+', line))[0]
                    if not year:
                        year = 0000
                    price = price.replace('$', '')
                except IndexError as error:
                    pass

                item_line = f"{year},{make},{model},{price}"
                clean_output_array.append(item_line)

        col_headers = f"Year,Make,Model,Price\n"
        clean_output_file_CURRENT_LISTINGS.write(col_headers)

        fileWrite(clean_output_array, clean_output_file_CURRENT_LISTINGS)

        logging.info(":::DATA CLEANING FOR CURRENT_LISTINGS successful")
        print(chalk.green((":::DATA CLEANING FOR CURRENT_LISTINGS successful")))
    except Exception as e:
        logging.error(f":::Error during data cleaning for CURRENT_LISTINGS: {str(e)}")
        print(chalk.red(f":::Error during data cleaning for CURRENT_LISTINGS: {str(e)}"))


def clean_data_EBAY_SOLD(car,raw_SOLD_DATA_file):

    try:
        #open raw data file
        clean_output_file_SOLD_DATA = open(EBAY_clean_OUTPUT_SOLD_DATA_file, "w", encoding="utf-8")
        
        #open  output file
        raw_input_SOLD_DATA = open(raw_SOLD_DATA_file, "r", encoding="utf-8")
        raw_data = raw_input_SOLD_DATA

        year = car['year']
        make = car['make']
        model = car['model']
        
        #for each line in raw data
        #line looks like -> 2000 Acura Integra Type R $63966.00 2024-02-12
        for line in raw_data:
           
            #if curr line contains our target veh model
            if model in line:
                #remove all commas - if any
                line = line.replace(',', '')
                
                #locate 4 digits in a row, this would be the year of the vehicle
                #if not found, use 0000 as year
                if re.findall('^\d{4}', line):
                    try:
                        veh_year = (re.findall('^\d{4}', line))[0]
                    except NameError:
                        veh_year = 0000
                

                #locate price value by finding $ symbol, get all values after this up to decimal point 
                #Ex input = $28000.00 -> output 28000
                try:
                    sale_price_match = (re.findall('\$(\d+)\.', line))[0]
                    if not veh_year:
                        veh_year = 0000
                    # print(sale_price_match)
                
                except IndexError as error:
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
        clean_output_file_SOLD_DATA.write(col_headers)

        fileWrite(clean_output_array, clean_output_file_SOLD_DATA)

        clean_output_file_SOLD_DATA.close()
        raw_input_SOLD_DATA.close()

        logging.info(":::DATA CLEANING FOR SOLD_DATA successful")
        print(chalk.green(":::DATA CLEANING FOR SOLD_DATA successful"))
    except Exception as e:
        logging.error(f":::Error during data cleaning for SOLD_DATA: {str(e)}")
        print(chalk.red(f":::Error during data cleaning for SOLD_DATA: {str(e)} \n OFFENDING LINE--> {line}"))



def ebay_clean_data_runner(car,EBAY_raw_CURRENT_LISTINGS_file_path,EBAY_raw_SOLD_DATA_file_path):
    try:
       
        clean_data_EBAY_CURRENT(car,EBAY_raw_CURRENT_LISTINGS_file_path)
        clean_data_EBAY_SOLD(car,EBAY_raw_SOLD_DATA_file_path)       
        
        logging.info("Data cleaning for all types successful")
        return True
    except Exception as e:
        logging.error(f"Error during data cleaning for all types: {str(e)}")
        return False

if __name__ == '__main__':
    car = {
        'year': 0000,
        'make': 'Nissan',
        'model': '350Z'
    }
    ebay_clean_data_runner(car,EBAY_raw_CURRENT_LISTINGS_file,EBAY_raw_SOLD_DATA_file)

