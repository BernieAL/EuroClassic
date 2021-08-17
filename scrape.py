"""
https://stackoverflow.com/questions/49788257/what-is-default-location-of-chromedriver-and-for-installing-chrome-on-windows
from selenium import webdriver

# Optional argument : if not specified WebDriver will search your system PATH environment variable for locating the chromedriver
driver = webdriver.Chrome(executable_path=r'C:\path\to\chromedriver.exe')
driver.get('https://www.google.co.in')
print("Page Title is : %s" %driver.title)
driver.quit()
"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time





make = "bmw"
chassis ="e39"
model ="m5"
# 98-03 for m5








vehicle = f"{make} {chassis} {model}"
print(vehicle)
# Create a new chromedriver
driver = webdriver.Chrome(executable_path=r'C:\Users\balma\Documents\Programming\chromedriver.exe')




# section to get production years from wikipedia
wikiString = f"https://en.wikipedia.org/wiki/{make}_{model}"
print(wikiString)
driver.get(wikiString)
specific_model_production = driver.find_element_by_link_text("BMW M5 (E39)")
specific_model_production.find_element_by_css_selector("#content-collapsible-block-1 > table > tbody > tr:nth-child(4) > td")




# #then enter years in ebay to get accurate results instead of chasis




# # Go to ebay
# driver.get("https://www.ebay.com/b/Auto-Parts-and-Vehicles/6000/bn_1865334")
# driver.implicitly_wait(15)

# #enter model 
# search_box = driver.find_element_by_css_selector('#gh-ac')
# driver.implicitly_wait(15)
# search_box.send_keys(vehicle + Keys.RETURN)





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