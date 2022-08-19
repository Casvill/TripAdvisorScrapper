import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# --- Scrapping city list
cities_list = []

def extract_cities(page) -> BeautifulSoup:
    
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    url = f'https://www.tripadvisor.com.mx/Restaurants-g150768-oa{page}-Mexico.html#LOCATION_LIST'
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    return soup

def transform_cities(soup) -> list:
    
    cities_list = []
    items = soup.find_all('div', class_='geo_wrap')

    for item in items:
        city =  item.find('a').text
        city = city.lstrip('Restaurantes en').split('\n-')[0]
        href =  item.find('a')['href']

        city = {'city': city, 'href': href}
        cities_list.append(city)

    return cities_list

def transform_cities2(soup) -> list:
    
    cities_list = []
    items = soup.find_all('ul', {'class': 'geoList'})

    for ultag in items:
        for litag in ultag.find_all('li'):
            city = litag.text
            city = city.lstrip('Restaurantes en').split('\n-')[0]
            href = litag.find('a')['href']
            
            city = {'city':city,'href':href}
            cities_list.append(city)

    return cities_list


max_city_page = 45 # one page contains 20 cities, max = 54

cities = transform_cities(extract_cities(0))

for i in range(20,(max_city_page*20),20):
    cities_list = transform_cities2(extract_cities(i))
    cities += cities_list

cities = pd.DataFrame(cities)

cities['city'] = cities['city'].str.lstrip('Restaurantes en')

cities.to_csv('data/city_list.csv')