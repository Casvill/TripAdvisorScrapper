import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# read city list 
cities = pd.read_csv('data/city_list.csv')
cities = cities[['city', 'href']]

# --- Scrapping restaurant list
def extract_restaurant_list(href_city) -> BeautifulSoup:
    
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

    url = f'https://www.tripadvisor.com.mx/{href_city}'
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    return soup

def transform_restaurant_list(soup) -> list:
    
    restaurant_ = []
    items = soup.find_all('div', class_='RfBGI')
    
    for item in items:
        restaurant =  item.find('a', class_='Lwqic Cj b').text
        href =  item.find('a')['href']

        restaurant = {'restaurant': restaurant, 'href': href}
        restaurant_.append(restaurant)

    return restaurant_

# --- Scrapping restaurants info
def extract_restaurant_info(page) -> BeautifulSoup:

    url = f'https://www.tripadvisor.com.mx{page}'

    browser = webdriver.Chrome(executable_path=r"/Users/rosaarzabala/Documents/Projects/TripAdvisorScrapper/chromedriver")
    browser.get(url)
    html = browser.page_source

    soup = BeautifulSoup(html, 'html.parser')

    return soup

restaurants_info_list = []

def transform_restaurant_info(soup,restaurant) -> list:

    div = soup.find('ul', class_='breadcrumbs')
    
    i = 0
    for item in div:
        try:
            if i == 0:
                state = item.find('a').text
            if i == 1:
                region = item.find('a').text
            if i == 2:
                city = item.find('a').text
                break
            i += 1
        except:
            pass

    div = soup.find('div', class_='YDAvY R2 F1 e k')
    for item in div:
        try:
            points = item.find('span', class_='ZDEqb').text
            # print('points:',points)
        except:
            pass

        try:
            reviews = item.find('a', class_='IcelI').text
            reviews = reviews.rstrip('opiniones')
            # print('reviews:',reviews)
        except:
            pass

    div = soup.find_all('div', class_='vQlTa H3')
    for item in div:
        try:
            ranking = item.find('span', class_='DsyBj cNFrA').text
            ranking = ranking.split(' ')[0]
            # print('ranking:',ranking)
            break
        except:
            ranking = ''              

    div = soup.find('div', class_='kDZhm IdiaP Me')
    for item in div:
        try:
            address = item.find('span', class_='yEWoV').text
            # print('address:',address)
        except:
            pass

    div = soup.find('div', class_='IdiaP Me sNsFa')
    for item in div:
        try:
            web_site = item.find('a', class_='YnKZo Ci Wc _S C FPPgD')['href']
            # print('web_site:',web_site)
        except:
            web_site = ''

    div = soup.find_all('div', class_='kDZhm IdiaP Me')
    for item in div:
        try:
            coordinates = item.find('a', class_='YnKZo Ci Wc _S C FPPgD')['href']
            coordinates = coordinates.split('@')[-1]
            latitude = coordinates.split(',')[0]
            longitude = coordinates.split(',')[1]
        except:
            pass

    restaurants_info = {'restaurant':restaurant,
                        'city': city,
                        'state': state,
                        'region': region,
                        'points': points,
                        'reviews': reviews,
                        'ranking': ranking,
                        'address': address,
                        'web_site': web_site,
                        'latitude': latitude,
                        'longitude': longitude}

    restaurants_info_list.append(restaurants_info)


# first 2 cities 
for city in cities.href[:2]:
    restaurant_list = transform_restaurant_list(extract_restaurant_list(city))
    restaurant_list = pd.DataFrame(restaurant_list)

    # new feature 
    restaurant_list['sponsored'] = ''
    for i in range(len(restaurant_list)):
        if '.' in restaurant_list['restaurant'][i]:
            restaurant_list['restaurant'][i] = restaurant_list['restaurant'][i].split('.')[1]
            restaurant_list['sponsored'][i] = restaurant_list['restaurant'][i].split('.')[0]
    restaurant_list['sponsored'] = ~restaurant_list.sponsored.astype('bool')

    # list without sponsored restaurants
    restaurant_list = restaurant_list[restaurant_list['sponsored'] == False]
    restaurant_list.reset_index(inplace=True)
    restaurant_list.drop(columns=['index'], inplace=True)

    # first 30 restaurants
    for i in range(30):
        href,restaurant = restaurant_list['href'][i],restaurant_list['restaurant'][i]
        transform_restaurant_info(extract_restaurant_info(href), restaurant)

# final df to csv
df_restaurants = pd.DataFrame(restaurants_info_list)
df_restaurants.to_csv('data/restaurants.csv')

# avg time: 