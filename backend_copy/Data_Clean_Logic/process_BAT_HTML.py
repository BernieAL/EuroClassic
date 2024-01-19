import os
from bs4 import BeautifulSoup
import re
import json



BAT_raw_SOLD_html_file_path = os.path.join(os.path.dirname(__file__),'..','Scraped_data_output/BAT_RAW_SOLD_HTML.html')
BAT_raw_SOLD_HTML = open(BAT_raw_SOLD_html_file_path,"r",encoding="utf-8")


NHS_all_veh_makes_data_file_path = os.path.join(os.path.dirname(__file__),'..','Resources/NHS_all_veh_makes.json')
NHS_all_veh_makes_file = open(NHS_all_veh_makes_data_file_path,"r",encoding="utf-8")
NHS_all_veh_makes_data = json.load(NHS_all_veh_makes_file)


soup = BeautifulSoup(BAT_raw_SOLD_HTML,'html.parser')



listing_card_tag = soup.find("a","listing-card")

content_main = listing_card_tag.find("div","content-main")
listing_card_title_text = content_main.select_one("h3[data-bind='html: title']").getText()

item_results_text = listing_card_tag.find("div","item-results").getText()
# print(item_results_text)


"""CLEANING LISTING_CARD TITLE
   -From title text find vehicle year using regex
   -wherever the year starts up, add 4 to this index, this is the indexes of year in the string
   -After year, the remainder of string will be the vehicle make and model
   -To extract the make, we will need to run the 
"""

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
target_make = listing_title_tokens[0].upper()
for result in NHS_all_veh_makes_data.get("Results",[]):
    if result.get("Make_Name") == target_make:
        print(True)

#once we confirm the first token is the make,
#split the string from this end of the make, the remaining is the model
# we will now have parsed out year,make,model successfully
