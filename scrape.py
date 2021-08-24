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
"""


from threading import Thread
from typing import ClassVar
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import NoSuchElementException
import time





make = "bmw"
chassis =""
model ="m3"
# 98-03 for m5








vehicle = f"{make} {model}"
print(vehicle)
# Create a new chromedriver
driver = webdriver.Chrome(executable_path=r'C:\Users\balma\Documents\Programming\chromedriver.exe')

# ===========================================
# :::::: BEGIN WIKI SECTION 
# """
# wikiString = f"https://en.wikipedia.org/wiki/{make}_{model}"
# print(wikiString)
# driver.get(wikiString)
# filterString = f"{make} {model} ("
# specific_model_production = driver.find_elements_by_xpath("//*[contains(text(),'E39 M5 (')]")
# for i in specific_model_production:
#     r = i.text
# :::::: END WIKI SECTION  

# ===========================================
# :::::: BEGIN EBAY SECTION 
# driver.get("https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117")
# driver.implicitly_wait(15)

# #enter model 
# search_box = driver.find_element_by_css_selector('#gh-ac')
# # WebDriverWait(driver,10)
# time.sleep(1)
# search_box.send_keys(vehicle + Keys.RETURN)


# # this gets prices of all cars on page
# prices = []
# test = driver.find_elements_by_class_name('s-item__price')
# for i in test:
#     price = (i.get_attribute('innerHTML'))
#     prices.append(price)
# time.sleep(1)
# print(prices)

# :::::: END EBAY SECTION 
# ===========================================


# :::::: BEGIN CRAIGLIST SECTION
# search route option 1 - longer and more human-like
# driver.get('https://miami.craigslist.org/mdc/')
# CL_searchBar = driver.find_element_by_css_selector('#query')
# time.sleep(2)
# CL_searchBar.send_keys(vehicle + Keys.RETURN)

# #search route option 2 - more direct
# driver.get(f'https://miami.craigslist.org/d/cars-trucks/search/mdc/cta?query={make}%20{model}&sort=rel')

# CL_prices = []
# CL_items = driver.find_elements_by_class_name('result-info')
# for item in CL_items:
#     description = item.find_element_by_class_name('result-heading').get_attribute('innerText')
#     price = item.find_element_by_class_name('result-price').get_attribute('innerText')
#     print(f" {description}:{price}")

# :::::: END CRAIGLIST SECTION
# ===========================================
# :::::: BEGIN BAT SECTION
driver.get('https://bringatrailer.com/')

#this is to get passed "show notifications prompt"
# driver.send_keys(Keys.TAB)
# driver.send_keys(Keys.TAB)
# driver.send_keys(Keys.RETURN)

driver.find_element_by_class_name('search-open').click()
time.sleep(2)
search_bar = driver.find_element_by_class_name('search-terms')
search_bar.send_keys(vehicle + Keys.RETURN)

#CLICK ONCE - To be replaced by repeated click logic
show_more = driver.find_element_by_css_selector('body > div.site-content > div.container > div > div > div.filter-group > div.overlayable > div.auctions-footer.auctions-footer-previous > button')
show_more.click()


# LOGIC TO CLICK SHOW MORE REPEATEDLY UNTIL NO 
# while True:
#     try:
#         show_more = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div/div[13]/div[3]/div[4]/button')
#         show_more.click()
#     except ElementNotVisibleException:
#         print('NOTHING MORE TO LOAD')
#         break
#     except NoSuchElementException:
#         print('ELEMENT NOT FOUND')
#         break

## EXTRACT MODEL,YEAR,PRICE from each itme
# model_list = driver.find_elements_by_class_name('previous-listing previous-listing-notext')
# for model in model_list:
#     model_name = driver.find_element_by_className('previous-listing-image-link').get_Attribute('alt')
#     print(model_name)


model_list = driver.find_elements_by_class_name('block')

for model in model_list:
    t = model.find_element_by_class_name('title').get_attribute('innerText')
    r = model.find_element_by_class_name('subtitle').get_attribute('innerText')
    print (f'{t} {r}')
    


"""
driver.find_by-xpath('/html/body/div[2]/div[2]/div/div/div[1]).get_attributes

"""
# :::::: END BAT SECTION

# # Get the webelement of the text input box
# search_box = driver.find_element_by_name("q")

# # Send the string "Selenium!" to the input box
# search_box.send_keys("Selenium!")

# # Submit the input, which starts a search
# search_box.submit()

# Wait to see the results of the search
time.sleep(5)

# # Close the driver
# driver.quit()