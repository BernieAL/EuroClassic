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


As of 10/5, only set up to clean ebay data, not CL
"""



import re

# unclean_input = open("output_file.txt","r",encoding="utf-8")

unclean_input = open("CURRENT_LISTINGS.txt","r",encoding="utf-8")
clean_output_file= open("cleaned_data.csv","w",encoding="utf-8")
clean_output_array = []

make = 'Audi'
model = 'RS5'
temp = []


def fileWrite(data,fileIn):
    for line in data:
        temp = f"{line} \n"
        fileIn.write(temp)
    fileIn.write("---------------------- \n")

def clean_the_data(unclean_input):
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
    clean_output_file.write(col_headers)
    
    fileWrite(clean_output_array,clean_output_file)


clean_the_data(unclean_input)

"""
make,model,year,price
"""


