from lib2to3.pgen2 import driver
from config import *
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#----------------------------------------------------------------------------------------------------------------------

def __formula(num:int) -> int:
    #print('__formula')
    return int(num-1)*20


def extract_cities(page) -> BeautifulSoup:
    print('extract_cities')
    page_transformed = __formula(page)
    
    url = URL+f'/Restaurants-g150768-oa{page_transformed}-Mexico.html#LOCATION_LIST'

    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.content, 'html.parser')

    return soup,page

#-----------------------------------------------------------------------------------------------------------------------

def extract_restaurant_names(page) -> BeautifulSoup:
    print('extract_restaurant_names')
    #print('page:',page)
    url = URL+page

    r = requests.get(url, headers=HEADERS)

    soup = BeautifulSoup(r.content, 'html.parser')

    return soup,page

#-----------------------------------------------------------------------------------------------------------------------

def driver_connection():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')  
    chrome_options.add_argument('--disable-dev-shm-usage')  
    chrome_options.add_argument('--headless')
    driver = webdriver.Remote('http://selenium:4444/wd/hub', 
                                desired_capabilities=DesiredCapabilities.CHROME,
                                options=chrome_options)
    return driver 


def extract_restaurant_info(page, driver) -> BeautifulSoup:
    #print('extract_restaurant_info')
    url = URL+page

    #options = Options()
    #options.headless = True
    #driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
    
    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html , 'html.parser')

    return soup

#-----------------------------------------------------------------------------------------------------------------------