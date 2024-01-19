import os
from bs4 import BeautifulSoup



BAT_raw_SOLD_html_file_path = os.path.join(os.path.dirname(__file__),'..','Scraped_data_output/BAT_RAW_SOLD_HTML.html')

BAT_raw_SOLD_HTML = open(BAT_raw_SOLD_html_file_path,"r",encoding="utf-8")


soup = BeautifulSoup(BAT_raw_SOLD_HTML,'html.parser')



listing_card_tag = soup.find("a","listing-card")

content_main = listing_card_tag.find("div","content-main")
listing_card_title_text = content_main.select_one("h3[data-bind='html: title']").getText()

item_results_text = listing_card_tag.find("div","item-results").getText()
print(item_results_text)

