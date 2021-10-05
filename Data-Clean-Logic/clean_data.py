"""
Read file in
Clean data
write to new file
Done
"""

import re


# unclean_input = open("output_file.txt","r",encoding="utf-8")
# clean_output= open("cleaned_data.txt","a",encoding="utf-8")
unclean_input = open("outputv2.txt","r",encoding="utf-8")
clean_output = []

make = 'BMW'
model = 'M6'
temp = []

for line in unclean_input:
    # only target lines with specific model
    
    if model in line:
        #remove commas from price
        line = line.replace(',','')
        #if current line start with 4 digits, this is year, get it. Otherwise skip line
        if re.findall('^\d{4}',line):
            year = (re.findall('^\d{4}',line))[0]
        #get price
        price = (re.findall('\$\d[0-9][0-9].+',line))[0]
        print(f"year:{year}, make:{make}, model:{model}, price:{price}")
                

    

"""
make,model,year,price
"""


