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

unclean_input_CURRENT_LISTINGS = open("CURRENT_LISTINGS.txt","r",encoding="utf-8")
unclean_input_SOLD_DATA = open("SOLD_DATA.txt","r",encoding="utf-8")

# clean_output_file_CURRENT_LISTINGS= open("cleaned_data_CURRENT_LISTINGS.csv","w",encoding="utf-8")
# clean_output_file_SOLD_DATA= open("cleaned_data_SOLD_DATA.csv","w",encoding="utf-8")
clean_output_array = []

make = 'Audi'
model = 'RS5'

temp = []
def fileWrite(data,fileIn):
    for line in data:
        temp = f"{line} \n"
        fileIn.write(temp)
    fileIn.write("---------------------- \n")

def clean_the_data(dirty_file,year,make,model):
    

    #output files to write to
    
    clean_output_array = []
    to_output_file = clean_output_file_SOLD_DATA

    unclean_input = open(dirty_file,"r",encoding="utf-8")
    
    if dirty_file == "CURRENT_LISTINGS.txt":
        to_output_file = clean_output_file_CURRENT_LISTINGS

    elif dirty_file == "SOLD_DATA.txt":
        to_output_file = clean_output_file_SOLD_DATA

    for line in unclean_input:
        # only target lines with specific model
        
        if model in line:
            #remove commas from price
            line = line.replace(',','')
            #if current line start with 4 digits, this is year, get it. Otherwise skip line
            if re.findall('^\d{4}',line):
                try:
                    year = (re.findall('^\d{4}',line))[0]
                except NameError:
                    year = 0000
            
            #get price
            price = (re.findall('\$\d[0-9][0-9].+',line))[0]
            if not year:
                year = 0000
            price = price.replace('$','')
            item_line = f"{year},{make},{model},{price}"
            # print(item_line)
            clean_output_array.append(item_line)
    

    
    col_headers = f"Year,Make,Model,Price \n"
    to_output_file.write(col_headers)
    
    fileWrite(clean_output_array,to_output_file)

    to_output_file.close()
    unclean_input.close()


# clean_the_data(unclean_input_CURRENT_LISTINGS,'2012','BMW','M5')

"""
make,model,year,price
"""


