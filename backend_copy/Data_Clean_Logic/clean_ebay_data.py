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

def clean_data_EBAY_SOLD(raw_SOLD_DATA_file, year, make, model):
    try:
        #open output file
        clean_output_file_SOLD_DATA = open(EBAY_clean_OUTPUT_SOLD_DATA_file, "w", encoding="utf-8")
        
        #open raw input source file
        raw_input_SOLD_DATA = open(raw_SOLD_DATA_file, "r", encoding="utf-8")
        
        #for each line in raw data
        #line looks like -> 2000 Acura Integra Type R $63966.00 2024-02-12
        for line in raw_input_SOLD_DATA:
            
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
                    print(sale_price_match)
                
                except IndexError as error:
                    pass
                print(f"{line}")
                try:
                    #extract date from line using pattern dddd-dd-dd , (where d is regex digit)
                    sale_date_match = (re.findall('\d{4}-\d{2}-\d{2}',line))[0]
                    
                    #concat into single line for to write to csv output file -> 1999,Acura,Integra,28000,2024-02-23
                    item_line = f"{veh_year},{make},{model},{sale_price_match},{sale_date_match}"
                    print(item_line)
                    
                    #remove any spacing
                    item_line = item_line.replace(' ', '')
                    print(item_line)
                    clean_output_array.append(item_line)

                except IndexError as error:
                    print(error)

        col_headers = f"Year,Make,Model,Price,DateSold\n"
        clean_output_file_SOLD_DATA.write(col_headers)

        fileWrite(clean_output_array, clean_output_file_SOLD_DATA)

        clean_output_file_SOLD_DATA.close()
        raw_input_SOLD_DATA.close()

        logging.info("Data cleaning for SOLD_DATA successful")
        print(chalk.green("Data cleaning for SOLD_DATA successful"))
    except Exception as e:
        logging.error(f"Error during data cleaning for SOLD_DATA: {str(e)}")
        print(chalk.red(f"Error during data cleaning for SOLD_DATA: {str(e)} \n OFFENDING LINE--> {line}"))

def clean_data_EBAY_CURRENT(raw_CURRENT_LISTINGS_file, year, make, model):
    try:
        clean_output_file_CURRENT_LISTINGS = open(EBAY_clean_OUTPUT_CURRENT_LISTINGS_file, "w", encoding="utf-8")
        

        raw_input_CURRENT_LISTINGS = open(raw_CURRENT_LISTINGS_file, "r", encoding="utf-8")
        unclean_input = raw_input_CURRENT_LISTINGS

        clean_output_array = []

        for line in unclean_input:
            if model in line:
                line = line.replace(',', '')
                if re.findall('^\d{4}', line):
                    try:
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
        logging.info("Data cleaning for CURRENT_LISTINGS successful")
        print(chalk.green(("Data cleaning for CURRENT_LISTINGS successful")))
    except Exception as e:
        logging.error(f"Error during data cleaning for CURRENT_LISTINGS: {str(e)}")
        print(chalk.red(f"Error during data cleaning for CURRENT_LISTINGS: {str(e)}"))

def ebay_clean_data_runner(car):
    try:
        clean_data_EBAY_SOLD(EBAY_raw_SOLD_DATA_file, car['year'], car['make'], car['model'])
        # clean_data_EBAY_CURRENT(EBAY_raw_CURRENT_LISTINGS_file, car['year'], car['make'], car['model'])
               
        logging.info("Data cleaning for all types successful")
        return True
    except Exception as e:
        logging.error(f"Error during data cleaning for all types: {str(e)}")
        return False

if __name__ == '__main__':
    car = {
        'year': 0000,
        'make': 'Acura',
        'model': 'Integra'
    }
    ebay_clean_data_runner(car)
