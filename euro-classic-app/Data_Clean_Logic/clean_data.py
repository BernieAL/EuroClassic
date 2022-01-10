"""
Read file in
Clean data
write to new file
Done
"""
"""THIS FILE TAKES IN THE RAW DATA AND CLEANS IT. OUTPUT FORMAT IS:
    year:1987, make:BMW, model:M6, price:$84997.00 +
    year:1987, make:BMW, model:M6, price:$39950.00 +
    year:1987, make:BMW, model:M6, price:$19750.00 +
    year:2005, make:BMW, model:M6, price:$25000.00 +

!!!
As of 12/27 it can clean ebay and CL data

Issue right now is the call from data_process_scripts is only handling SOLD_DATA
when both calls are uncommented.
When SOLD_DATA call is commented, CURRENT_LISTINGS works.

Only when both are uncommented, CURRENT_LISTINGS is not handled, its skipped over
Nothing gets written to cleaned_data_CURRENT_LISTINGS.csv
"""



import re
clean_output_file_CURRENT_LISTINGS= open("cleaned_data_CURRENT_LISTINGS.csv","w",encoding="utf-8")
clean_output_file_SOLD_DATA= open("cleaned_data_SOLD_DATA.csv","w",encoding="utf-8")

# unclean_input_CURRENT_LISTINGS = open("CURRENT_LISTINGS.txt","r",encoding="utf-8")
# unclean_input_SOLD_DATA = open("SOLD_DATA.txt","r",encoding="utf-8")


clean_output_array = []



temp = []
def fileWrite(data,fileIn):
    for line in data:
        temp = f"{line} \n" #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! try writing to file without \n to see if reading the data is easier for prediction
        fileIn.write(temp)
    fileIn.write("---------------------- \n")

def clean_the_data(dirty_file,year,make,model):
    

    
    option = 0
    #output files to write to
    
    clean_output_array = []
    to_output_file = ""

    unclean_input = open(dirty_file,"r",encoding="utf-8")
    
    if dirty_file == "CURRENT_LISTINGS.txt":
        to_output_file = clean_output_file_CURRENT_LISTINGS
    
    elif dirty_file == "SOLD_DATA.txt":
        to_output_file = clean_output_file_SOLD_DATA

    for line in unclean_input:
        print(line)
        # only target lines with specific model
        
        if model in line:
            #remove commas from price
            line = line.replace(',','')
            print(line)
            #if current line start with 4 digits, this is year, get it. Otherwise skip line
            if re.findall('^\d{4}',line):
                try:
                    year = (re.findall('^\d{4}',line))[0]
                except NameError:
                    year = 0000
            
            #get price
            try:
                price = (re.findall('\$\d[0-9][0-9].+',line))[0]
                if not year:
                    year = 0000
                price = price.replace('$','')
            except IndexError as error:
                pass

            #THIS ONLY RUNS IF THE LINE HAS 'ON' in it, otherwise we go to else and dont include sale date because there is none
            #if no sale date, then we are dealing with current listing
            # for handling the 'on' in the sold data
            #we first check if the data line has 'on' in it because if we are handling current listings, it wont have 'sold on'
            #if there is an 'on' in the current line, we need to split at the on to get the price and sale data
            """
            checks for 'on' in - 2001,BMW,M5,45000 on 11/23/20 
            if line has 'on', we split at it and get  ['45000 ', ' 11/23/20 ']
            reassign price to be the first element in array returned from split
            set sale_Date to be second element in the array returned from split
            set item_line string to include price and sale_Date
            """
            
            # if dirty_file == "SOLD_DATA.txt" and price.find('Sold on'):
            #      price_sale_date_split = price.split('on')
            #      price = price_sale_date_split[0]
            #      sale_Date = price_sale_date_split[1]
            #      #replace / with - in sale_Date
            #      sale_Date = sale_Date.replace('/','-')
            #      item_line = f"{year},{make},{model},{price},{sale_Date}"
            #      #remove extra space between price and sale date Ex. ['45000 ', ' 11/23/20 '] -> 44250,12/22/21 
            #      item_line = item_line.replace(' ','')
            #      clean_output_array.append(item_line)
            #      col_headers = f"Year,Make,Model,Price,DateSold\n"    
            # else:
            #     item_line = f"{year},{make},{model},{price}"
            #     clean_output_array.append(item_line)
            #     col_headers = f"Year,Make,Model,Price\n"



            if dirty_file == "SOLD_DATA.txt" and price.find('on'):
                 price_sale_date_split = price.split('on')
                 price = price_sale_date_split[0]
                 sale_Date = price_sale_date_split[1]
                 #replace / with - in sale_Date
                 sale_Date = sale_Date.replace('/','-')
                 item_line = f"{year},{make},{model},{price},{sale_Date}"
                 #remove extra space between price and sale date Ex. ['45000 ', ' 11/23/20 '] -> 44250,12/22/21 
                 item_line = item_line.replace(' ','')
                 clean_output_array.append(item_line)
                 option = 1
                 col_headers = f"Year,Make,Model,Price,DateSold\n"
            else:
                 item_line = f"{year},{make},{model},{price}"
                 clean_output_array.append(item_line)
                 option = 2
                 col_headers = f"Year,Make,Model,Price\n"
                 

    to_output_file.write(col_headers)
    # if option == 1:
    #     col_headers = f"Year,Make,Model,Price,DateSold\n"
    #     to_output_file.write(col_headers)
    # elif option == 2:
    #     col_headers = f"Year,Make,Model,Price\n"
    #     to_output_file.write(col_headers)
    
    
    fileWrite(clean_output_array,to_output_file)

    # to_output_file.close()
    # unclean_input.close()


# clean_the_data("SOLD_DATA.txt",'2012','Audi','R8')
clean_the_data("CURRENT_LISTINGS.txt",'2012','Audi','R8')
"""
make,model,year,price
"""


