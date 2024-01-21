import os
from bs4 import BeautifulSoup
import re
import json


#RAW HTML FROM BAT
BAT_raw_SOLD_html_file_path = os.path.join(os.path.dirname(__file__),'..','Scraped_data_output/BAT_RAW_SOLD_HTML.html')
BAT_raw_SOLD_HTML = open(BAT_raw_SOLD_html_file_path,"r",encoding="utf-8")

#ALL VEH MAKES JSON DATA FROM - https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json
NHS_all_veh_makes_data_file_path = os.path.join(os.path.dirname(__file__),'..','Resources/NHS_all_veh_makes.json')
NHS_all_veh_makes_file = open(NHS_all_veh_makes_data_file_path,"r",encoding="utf-8")
NHS_all_veh_makes_data = json.load(NHS_all_veh_makes_file)


#CSV OUTPUT FILE
BAT_cleaned_SOLD_Data_file_path = os.path.join(os.path.dirname(__file__),'..','Cleaned_data_output/BAT_cleaned_SOLD_data.csv')
BAT_cleaned_SOLD_Data = open(BAT_cleaned_SOLD_Data_file_path,"w",encoding="utf-8")



missing_year_listings = []
def extract_year_make_model(content_main):
    
    """CLEANING LISTING_CARD TITLE
       -From title text find vehicle year using regex
       -wherever the year starts up, add 4 to this index, this is the indexes of year in the string
       -After year, the remainder of string will be the vehicle make and model
       -To extract the make, we will need to run the 


       -Function is to be called on each listing_card element found
       -Recieves content_main from listing_card element
    """
    
    #target h3 element to get title text
    listing_card_title_text = content_main.select_one("h3[data-bind='html: title']").getText().upper()
    
    #remove any extra white spaces that cause text to span 2 lines
    listing_card_title_text = re.sub(r'\s{2,}', ' ', listing_card_title_text).strip()
    print(listing_card_title_text)

    
    """FINDING AND REMOVING YEAR"""
    #find year by matching 4 digits in a row
    veh_year_match = re.search(r'\b\d{4}\b', listing_card_title_text)
    #if theres no year in the listing, we just use 0000 in place of 4 digit year to not break script
    veh_year = veh_year_match.group() if veh_year_match else '0000' 
    # print(veh_year)
    """Get Location of Year in string
        -instead of finding index of last digit in the year - we use end() method on re.match obj (veh_year_match) to get ending index of the matched string
        -if no match - meaning veh_year_match is none, we default to 0
    """
    last_digit_of_year_index = veh_year_match.end() if veh_year_match else 0
    """Removing year from the title
        -use re.sub() to replace matched year string with an empty string
        -'\b' in regex means word boundaries - ensuring repleacement occurs only for whole words
        -re.escape(veh_year) is used to escape any special chars in the year string
        -re.IGNORECASE flag makes the replacement case-sensitive

        -rf'\b{re.escape(veh_year)}\b': This is an f-string that dynamically inserts the escaped year string into the regular expression pattern. The \b ensures that the replacement is only done for whole words.
        -'': This is the replacement string, which is an empty string, effectively removing the matched year.
        -listing_card_title_text: This is the original title text.
        -flags=re.IGNORECASE: This flag makes the replacement case-insensitive.
    """
    listing_title_year_removed = re.sub(rf'\b{re.escape(veh_year)}\b', '', listing_card_title_text, flags=re.IGNORECASE).strip()
    # print(listing_title_year_removed)

    
    """FINDING MILEAGE (if listed)
        - some listings are in the format: 10K-MILE 2008 MERCEDES-BENZ SLR MCLAREN ROADSTER, 16K-MILE 2013 MCLAREN 12C SPIDER
        - Use regex to find "MILE" and and extract - store this value as mileage for this vehicle entry
        - If listing doesnt have "MILE" in title text, then use 000 for mileage as default value
    """
    
    
    """FINDING MAKE AND MODEL
        -Tokenize string with year removed
        -Go through tokens, check which token exists in NHS_all_veh_makes, this is our 'Make' value
        -Once 'Make' is found, the remaining tokens after where 'Make' was found now pertain to the 'Model'
        Ex.
            tokens = ['MCLAREN', '720S', 'PERFORMANCE', 'COUPE']
            if 'MCLAREN' exists in all_makes, we validate that this token is our MAKE
            The remaining tokens will be joined assigned to MODEL
            

    """

    #tokenize results after year removed
    listing_title_tokens = listing_title_year_removed.split(' ')
 
    
    veh_make = ''
    veh_model = ''
    for token in listing_title_tokens[1:]:
        potential_make = token
        if potential_make in NHS_all_veh_makes_data.get('Results',{}):
            veh_make = potential_make
            veh_model = ' '.join(listing_title_tokens[listing_title_tokens.index(token) + 1:])
            break
    
   

    return veh_year,veh_make,veh_model

    

def extract_sale_price_and_date(content_main):
    """ SECTION FOR SALE PRICE AND SALE DATE from item-results element
        -Contents of this section looks will either be:
            - Bid to $277,277  on 1/16/24
            OR
            - Sold for $234,234 on  1/16/24
        - Need to parse out price and sale date


        -Function is to be called on each listing_card element found
        -Recieves content_main from listing_card element
    """

    item_result_text =  content_main.find('div','item-results').getText().upper()
    sale_price,sale_date = item_result_text.split('  ON ')

    #regex delimiters to check for 'for' and 'to' - because the string can have either one
    delimiters = r'\bTO\b|\bFOR\b'

    #splitting using regex delimiters  
    listing_type,sale_price = (re.split(delimiters,sale_price))

    #remove $ and , from sale_price, then convert to float
    sale_price = float(sale_price.replace('$','').replace(',',''))
    



    return sale_price,sale_date,listing_type


def driver():
    
    csv_headers = 'YEAR,MAKE,MODEL,SALE_PRICE,SALE_DATE,LISTING_TYPE'
    BAT_cleaned_SOLD_Data.write(csv_headers + '\n')
    soup = BeautifulSoup(BAT_raw_SOLD_HTML,'html.parser')
    
    #find all listing_card in auctions-completed-container element
    auction_results_section = soup.find("div","auctions-completed-container")
    listing_card_tags = auction_results_section.find_all("a","listing-card")

    #for each listing_card, extract year,make,model,sale_price,sale_date and write to output file
    for listing in listing_card_tags:
        #find content main from each listing_card
        content_main = listing.find("div","content-main")
        year,make,model =  extract_year_make_model(content_main)
        
        sale_price,sale_date,listing_type = extract_sale_price_and_date(content_main)

        # print(f"{year},{make},{model}")

        # BAT_cleaned_SOLD_Data.write(f"{year},{make},{model},{sale_price},{sale_date},{listing_type}")

# print(missing_year_listings)
if __name__ == '__main__':
    driver()
    


