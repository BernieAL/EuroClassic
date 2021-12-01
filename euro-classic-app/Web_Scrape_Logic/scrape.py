"""
https://stackoverflow.com/questions/49788257/what-is-default-location-of-chromedriver-and-for-installing-chrome-on-windows
from selenium import webdriver

# Optional argument : if not specified WebDriver will search your system PATH environment variable for locating the chromedriver
driver = webdriver.Chrome(executable_path=r'C:\path\to\chromedriver.exe')
driver.get('https://www.google.co.in')
print("Page Title is : %s" %driver.title)
driver.quit()

https://www.selenium.dev/documentation/webdriver/web_element/

https://stackoverflow.com/questions/34315533/can-i-find-an-element-using-regex-with-python-and-selenium
https://stackoverflow.com/questions/12323403/how-do-i-find-an-element-that-contains-specific-text-in-selenium-webdriver-pyth

https://stackoverflow.com/questions/45990851/how-do-i-iterate-through-a-webelements-list-with-python-and-selenium/46001881


UnicodeEncodeError: 'charmap' codec can't encode characters
https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters




"""


from threading import Thread
from typing import ClassVar
from selenium import webdriver
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import time





# make = "audi"
# chassis =""
# model ="rs5"
# year =""
# # 98-03 for m5

#files for current listing data and sold data
current_listing_output = open("CURRENT_LISTINGS.txt","a",encoding="utf-8")
sold_output = open("SOLD_DATA.txt","a",encoding="utf-8")

# Create a new chromedriver
driver = webdriver.Chrome(executable_path=r'C:\Users\balma\Documents\Programming\chromedriver.exe')

# ===========================================================================
# ===========================================================================
# # :::::: BEGIN EBAY SECTION 
def ebay(car):
    driver.get("https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117")
    # driver.implicitly_wait(15)


    #enter model 
    ebay_search_box = driver.find_element_by_css_selector('#gh-ac')
    # WebDriverWait(driver,10)
    time.sleep(1)
    ebay_search_box.send_keys(car + Keys.RETURN)
    time.sleep(1.5)

    # this gets prices of all cars on page
    ebay_items = []
    ebay_listings = driver.find_elements_by_class_name('s-item__info')
    all_descriptions = driver.find_elements_by_class_name('s-item__title')
    all_prices = driver.find_elements_by_class_name('s-item__price')


    for (descrip,price) in zip(all_descriptions,all_prices):
        item_description= descrip.get_attribute('innerText')
        item_description = item_description.replace('NEW LISTING','')
        item_price = price.get_attribute('innerText')
        temp = f'{item_description} {item_price}'
        ebay_items.append(temp)

    
    #write date of scrape to file right before data
    today = date.today()
    # dd/mm/YY
    current_date = today.strftime("%d/%m/%Y")
    date_string = f" :::EBAY - DATA SCRAPED ON: {current_date} \n"
    current_listing_output.write(date_string)   

    #write items to file
    fileWrite(ebay_items,current_listing_output)

    print(ebay_items)

# # :::::: END EBAY SECTION 
# ===========================================================================


# :::::: BEGIN CRAIGLIST SECTION
def CL(car):
    # search route option 1 - longer and more human-like
    # driver.get('https://miami.craigslist.org/mdc/')
    # CL_searchBar = driver.find_element_by_css_selector('#query')
    # time.sleep(2)
    # CL_searchBar.send_keys(vehicle + Keys.RETURN)

    #search route option 2 - more direct
    driver.get(f'https://miami.craigslist.org/d/cars-trucks/search/mdc/cta?query={make}%20{model}&sort=rel')

    CL_prices=[]
    CL_items = []
    CL_items = driver.find_elements_by_class_name('result-info')
    for item in CL_items:
        description = item.find_element_by_class_name('result-heading').get_attribute('innerText')
        price = item.find_element_by_class_name('result-price').get_attribute('innerText')
        temp = f" {description}:{price}"
        CL_prices.append(temp)
        # print(f" {description}:{price}")

    #write date of scrape to file right before data
    today = date.today()
    # dd/mm/YY
    current_date = today.strftime("%d/%m/%Y")
    date_string = f" :::CRAIGLIST - DATA SCRAPED ON: {current_date} \n"
    current_listing_output.write(date_string)   

    #write items to file
    fileWrite(CL_prices,current_listing_output)    

# :::::: END CRAIGLIST SECTION
# ===========================================================================
# :::::: BEGIN BAT SECTION

def bat(car):
        # # #this is to get passed "show notifications prompt"
        # # driver.send_keys(Keys.TAB)
        # # driver.send_keys(Keys.TAB)
        # # driver.send_keys(Keys.RETURN)

        # # driver.find_element_by_class_name('search-open').click()
        # # time.sleep(2)
        # # search_bar = driver.find_element_by_class_name('search-terms')
        # # search_bar.send_keys(vehicle + Keys.RETURN)


        driver.get(f'https://bringatrailer.com/{make}/{model}')
        # # https://bringatrailer.com/bmw/e39-m5/?q=e39%20m5

        # # #CLICK ONCE - To be replaced by repeated click logic
        # show_more = driver.find_element_by_css_selector('body > div.site-content > div.container > div > div > div.filter-group > div.overlayable > div.auctions-footer.auctions-footer-previous > button')
        show_more = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[4]/div[3]/div[4]/button')
        time.sleep(.45)
        # show_more.click()

        # # # LOGIC TO CLICK SHOW MORE REPEATEDLY UNTIL NO 
        while show_more:
            try:
                show_more.click()
                time.sleep(2)
            except ElementNotVisibleException:
                print('NOTHING MORE TO LOAD')
                break
            except NoSuchElementException:
                print('ELEMENT NOT FOUND')
                break
            except StaleElementReferenceException:
                print('NO MORE RESULTS TO LOAD')
                break

        #target parent group that holds individual previous listing items
        prev_listings = driver.find_element_by_class_name('filter-group')
        time.sleep(1)
        #extract all block elements from parents group, this gives each indiv listing
        item_list = prev_listings.find_elements_by_class_name('block')
    
        ## EXTRACT MODEL,YEAR,PRICE from each item
        BAT_items = []
        for item in item_list:
            description = item.find_element_by_class_name('title').get_attribute('innerText')
            price = item.find_element_by_class_name('subtitle').get_attribute('innerText')
            temp = f'{description} {price}'
            BAT_items.append(temp)


        #write date of scrape to file right before data
        today = date.today()
        # dd/mm/YY
        current_date = today.strftime("%d/%m/%Y")
        date_string = f"DATA SCRAPED: {current_date} \n"
        sold_output.write(date_string)

        #write items to sold output file
        fileWrite(BAT_items,sold_output)

        # print(BAT_items)
# :::::: END BAT SECTION
# ==============================================================================

#CALLING ALL SCRAPE FUNCTIONS

def fileWrite(data,fileIn):
    for line in data:
        temp = f"{line} \n"
        fileIn.write(temp)
        fileIn.write("---------------------- \n")



def scrape(car):

   
    vehicle = f"{make} {model}"
    print(vehicle)

    ebay(car)
    CL(car)
    bat(car)


 


# # Get the webelement of the text input box
# search_box = driver.find_element_by_name("q")

# # Send the string "Selenium!" to the input box
# search_box.send_keys("Selenium!")

# # Submit the input, which starts a search
# search_box.submit()

# # Wait to see the results of the search
# time.sleep(5)

# # Close the driver
# driver.quit()

def test():
    print( "hello this is from scrape.py")

"""

ebay raw result:
    '$91,000.00  ', '$40,100.00 NEW LISTING1966 Jaguar E-Type ', '$60,099.00 1969 Jaguar E-Type Roadster ', '$35,100.00 1969 Jaguar E-Type ', '$89,500.00 1969 Jaguar E-Type Convertible ', '$79,900.00 1968 Jaguar E-Type ', '$45,100.00 1970 Jaguar E-Type Convertible ', '$102,000.00 1963 Jaguar E-Type ', '$187,500.00 1964 Jaguar E-Type ', '$84,987.00 1974 Jaguar E-Type ', '$109,500.00 1963 Jaguar E-Type ', '$158,995.00 1966 Jaguar E-Type Series 1 4.2 Liter Fixed-head coupe ', '$89,900.00 1971 Jaguar E-Type Fixed Head Coupe ', '$56,995.00 1969 Jaguar E-Type XK-E 2+2 Series 2 ', '$74,625.00 1968 Jaguar E-Type XKE Series II 4.2L 6 cyl 4 spd Convertible ', '$99,500.00 1973 Jaguar 
E-Type Roadster v12 ', '$69,750.00 1970 Jaguar E-Type 1970 JAGUAR XKE 2+2 E-TYPE ',

CL raw result:

    2012 BMW 5 Series 4dr Sdn 535i RWD 90 Days Car Warranty :$9,800
    2015 BMW 3 Series 328i SKU:FF607643 Sedan :$16,992
    2014 BMW 5 Series 528i with :$15,500
    2013 BMW 7 SERIES 750I XDRIVE SEDAN 4D :$12,950
    2014 BMW 5 Series 528i with :$15,500
    2014 BMW Z4 SDRIVE28I ROADSTER 2D :$21,495
    2010 BMW 3 Series 335i Convertible 2D Convertible Gray - FINANCE :$19,590
    2012 BMW X5 AWD 4dr 35i 90 Days Car Warranty :$11,199
    2014 BMW X3 xDrive28i Sport Utility 4D :$0
    2014 BMW 5 Series 528i with :$15,500
    2013 BMW 3 Series 328i with :$13,639
    2002 HONDA S2000 S CONVERTIBLE :$19,995
    BMW 328i Sedan Sport Package Runs Excellent Clean Title :$9,995
    2014 BMW 3 Series 4dr Sdn 328d RWD 90 Days Car Warranty :$10,499
    2016 DODGE CHARGER R/T ROAD & TRACK SEDAN 4D :$16,950
    2011 Cadillac SRX AWD 4dr Luxury Collection :$8,750

BAT raw result:
    41k-Mile 2004 BMW M3 Coupe 6-Speed Sold for $38,000 on 7/30/21
    43k-Mile 1999 BMW M3 Coupe 5-Speed Sold for $45,000 on 7/29/21
    Modified 1998 BMW M3 Coupe 5-Speed Sold for $34,000 on 7/29/21
    2004 BMW M3 Convertible Sold for $20,000 on 7/28/21


"""