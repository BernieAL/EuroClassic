
import pytest
from Web_Scrape_Logic.scrape import ebay
from threading import Thread
from typing import ClassVar
from selenium import webdriver
from unittest.mock import patch, MagicMock


# set up fixture mockdriver function for use in test function
@pytest.fixture
def mock_driver():
    driver = webdriver.Chrome(executable_path=r'C:\browserdrivers\chromedriver\chromedriver.exe')
    with patch(driver) as mock:
        mock.get.return_value = None
        mock.find_element.return_value = MagicMock()
        mock.find_element.return_value.get_attribute.return_value = "Mocked Element"
        yield mock
     
def test_ebay_function_with_mocking(mock_driver):
    car = {'make': 'Toyota', 'model': 'Camry'}
    driver = webdriver.Chrome()
    ebay(car, driver)

    # Make assertions based on the behavior of the mock driver
    mock_driver.get.assert_called_once_with("https://www.ebay.com/b/Cars-Trucks/6001/bn_1865117")
    mock_driver.find_element.assert_called_with('css_selector', '#gh-ac')
    mock_driver.find_element.return_value.get_attribute.assert_called_with('innerText')

    mock_driver.find_elements
    driver.quit()

if __name__ == '__main__':
    pytest.main()
