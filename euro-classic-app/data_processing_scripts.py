
"""
This script runs the scraping then the cleaning
and returns the clean result back to main app 
clean data is then sent and  displayed in data.html template


scrape takes car object in and performs search on 3 sources
takes resutls and writes to 2 files, one current listing and one for already sold listings

after scrape runs, we pass the file with dirty data to the clean_data function
this reads in the dirty data and cleans it, writing it a new file

to get the clean data back to main app 
we can read it from file here and convert to an array
read it from a file back in main app

"""


from Web_Scrape_Logic import scrape
from Data_Clean_Logic import clean_data


#after running scrape, the files will be populated with dirty data
# current_listing_unclean = open("CURRENT_LISTINGS.txt","a",encoding="utf-8")
# sold_listings_unclean = open("SOLD_DATA.txt","a",encoding="utf-8")





def handle_data(car):
    scrape.scrapeFunc(car)

    clean_data.clean_the_data("CURRENT_LISTINGS.txt",car['year'],car['make'],car['model'])
    clean_data.clean_the_data("SOLD_DATA.txt",car['year'],car['make'],car['model'])
    
     

# car = {
#     'year':2001,
#     'make':'BMW',
#     'model':'M5'
# }
# handle_data(car)