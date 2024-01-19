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
NHS_all_veh_makes_file = open(NHS_all_veh_makes_data_file_path,"a",encoding="utf-8")




def extract_year_make_model(content_main):
    """CLEANING LISTING_CARD TITLE
       -From title text find vehicle year using regex
       -wherever the year starts up, add 4 to this index, this is the indexes of year in the string
       -After year, the remainder of string will be the vehicle make and model
       -To extract the make, we will need to run the 


       -Function is to be called on each listing_card element found
       -Recieves content_main from listing_card element
    """
    listing_card_title_text = content_main.select_one("h3[data-bind='html: title']").getText()
    veh_year_match = re.search(r'\b\d{4}\b', listing_card_title_text)
    veh_year = veh_year_match.group()
    last_digit_of_year_index = listing_card_title_text.find(veh_year[-1])

    # +2 handles last skipping over last digit and space before getting to vehicle make
    #using position of last_digit in veh_year, get rest of string - this will be make and model
    listing_title_year_removed = listing_card_title_text[last_digit_of_year_index+2:]
    # print(listing_title_year_removed)

    #tokenize
    listing_title_tokens = listing_title_year_removed.split(' ')
    # print(listing_title_tokens)

    #take first token, which should be the make, search for this token in list of manufacturers
    #if we find a match, this token is the manufacturer and the remaining of the string is the model
    veh_make = listing_title_tokens[0].upper()
    for result in NHS_all_veh_makes_data.get('Results',[]):
        if result.get('Make_Name') == veh_make:
            print(True)

    #once we confirm the first token is the make,
    #combine rest of tokens from listing_title_tokens and combine into a single string - this is the model
    # we will now have parsed out year,make,model successfully
    veh_model = ' '.join(listing_title_tokens[1:])
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

    return sale_price,sale_date


def driver():
    soup = BeautifulSoup(BAT_raw_SOLD_HTML,'html.parser')

    #find all listing_card in auctions-completed-container element
    auction_results_section = soup.find("div","auctions-completed-container")
    listing_card_tags = auction_results_section.find_all("a","listing-card")

    #for each listing_card, extract year,make,model,sale_price,sale_date and write to output file
    for listing in listing_card_tags:
        #find content main from each listing_card
        content_main = listing_card_tags.find("div","content-main")
        year,make,model =  extract_year_make_model(content_main)
        sale_price,sale_date = extract_sale_price_and_date(content_main)

        #file.write(f"{year},{make},{model},{sale_price},{sale_date}")


    csv_headers = ['YEAR','MAKE','MODEL','SALE_PRICE','SALE_DATE']
    

#convert sale date to date object before writing in csv - date object makes working with dates easier
