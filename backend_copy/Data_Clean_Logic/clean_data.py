import logging
import re
import os
from simple_chalk import chalk

# Configure logging
log_file_path = os.path.join(os.path.dirname(__file__), 'cleaning_log.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO)

#dir of raw extracted data
extracted_data_dir_path = os.path.join(os.path.dirname(__file__), '..', 'Scraped_data_output')

EBAY_raw_CURRENT_LISTINGS_file = os.path.join(extracted_data_dir_path, 'EBAY_raw_CURRENT_LISTINGS_DATA.txt')

EBAY_raw_SOLD_DATA_file = os.path.join(extracted_data_dir_path, 'EBAY_raw_SOLD_DATA.txt')

EBAY_clean_output_file_CURRENT_LISTINGS_file = os.path.join(extracted_data_dir_path, '..', 'EBAY_cleaned_CURRENT_LISTINGS.csv')

EBAY_clean_output_file_SOLD_DATA_file = os.path.join(extracted_data_dir_path, '..', 'EBAY_cleaned_SOLD_DATA.csv')

clean_output_array = []

def fileWrite(data, fileIn):
    for line in data:
        temp = f"{line}\n"
        fileIn.write(temp)
    fileIn.write("---------------------- \n")

def clean_data_SOLD(raw_SOLD_DATA_file, year, make, model):
    try:
        clean_output_file_SOLD_DATA = open(EBAY_clean_output_file_SOLD_DATA_file, "w", encoding="utf-8")
        to_output_file = clean_output_file_SOLD_DATA

        raw_input_SOLD_DATA = open(raw_SOLD_DATA_file, "r", encoding="utf-8")
        unclean_input = raw_input_SOLD_DATA

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

                price_sale_date_split = price.split('on')
                price = price_sale_date_split[0]
                sale_Date = price_sale_date_split[1]
                sale_Date = sale_Date.replace('/', '-')
                item_line = f"{year},{make},{model},{price},{sale_Date}"
                item_line = item_line.replace(' ', '')
                clean_output_array.append(item_line)

        col_headers = f"Year,Make,Model,Price,DateSold\n"
        clean_output_file_SOLD_DATA.write(col_headers)

        fileWrite(clean_output_array, to_output_file)

        clean_output_file_SOLD_DATA.close()
        unclean_input.close()
        logging.info("Data cleaning for SOLD_DATA successful")
        print(chalk.green("Data cleaning for SOLD_DATA successful"))
    except Exception as e:
        logging.error(f"Error during data cleaning for SOLD_DATA: {str(e)}")
        print(chalk.red(f"Error during data cleaning for SOLD_DATA: {str(e)}"))

def clean_data_CURRENT(raw_CURRENT_LISTINGS_file, year, make, model):
    try:
        clean_output_file_CURRENT_LISTINGS = open(EBAY_clean_output_file_CURRENT_LISTINGS_file, "w", encoding="utf-8")
        to_output_file = clean_output_file_CURRENT_LISTINGS

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
        to_output_file.write(col_headers)

        fileWrite(clean_output_array, to_output_file)
        logging.info("Data cleaning for CURRENT_LISTINGS successful")
        print(chalk.green(("Data cleaning for CURRENT_LISTINGS successful")))
    except Exception as e:
        logging.error(f"Error during data cleaning for CURRENT_LISTINGS: {str(e)}")
        print(chalk.red(f"Error during data cleaning for CURRENT_LISTINGS: {str(e)}"))

def clean_all_data(car):
    try:
        clean_data_CURRENT(EBAY_raw_CURRENT_LISTINGS_file, car['year'], car['make'], car['model'])
        clean_data_SOLD(EBAY_raw_SOLD_DATA_file, car['year'], car['make'], car['model'])
        logging.info("Data cleaning for all types successful")
        return True
    except Exception as e:
        logging.error(f"Error during data cleaning for all types: {str(e)}")
        return False

if __name__ == '__main__':
    car = {
        'year': 2021,
        'make': 'Audi',
        'model': 'RS6'
    }
    clean_all_data(car)
