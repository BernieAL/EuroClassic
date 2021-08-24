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
"""


from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time





make = "audi"
chassis ="r8"
model ="r8"
# 98-03 for m5








vehicle = f"{make} {model}"
print(vehicle)
# Create a new chromedriver
driver = webdriver.Chrome(executable_path=r'C:\Users\balma\Documents\Programming\chromedriver.exe')




# """
# wikiString = f"https://en.wikipedia.org/wiki/{make}_{model}"
# print(wikiString)
# driver.get(wikiString)
# filterString = f"{make} {model} ("
# specific_model_production = driver.find_elements_by_xpath("//*[contains(text(),'E39 M5 (')]")
# for i in specific_model_production:
#     r = i.text
    


# # Go to ebay
driver.get("https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117")
driver.implicitly_wait(15)

#enter model 
search_box = driver.find_element_by_css_selector('#gh-ac')
# WebDriverWait(driver,10)
time.sleep(1)
search_box.send_keys(vehicle + Keys.RETURN)


# this gets prices of all cars on page
prices = []
test = driver.find_elements_by_class_name('s-item__price')
for i in test:
    price = (i.get_attribute('innerHTML'))
    prices.append(price)

time.sleep(1)
print(prices)



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