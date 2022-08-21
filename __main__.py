import extract
import transform
import pandas as pd
import time 

total_pages = 54 
cities = 3

# city list
for i in range(1,total_pages):
    soup,page = extract.extract_cities(i)
    df_cities = transform.transform_cities(soup,page)
    time.sleep(0.1)
print('\nLista de ciudades cargada')


# restaurants per city
for href in df_cities['href'][:cities]:
    #print('href:',href)
    soup,page = extract.extract_restaurant_names(href)
    df_restaurants = transform.transform_restaurant_names(soup,page,df_cities)
    time.sleep(0.5)
print('\nLista de restaurantes por ciudad cargada')


# restaurant info
for i in range(30*cities):
    href = df_restaurants['href'][i]
    restaurant = df_restaurants['restaurant'][i]
    city = df_restaurants['city'][i]
    state =df_restaurants['state'][i]
    df_restaurants_info = transform.transform_restaurants_info(extract.extract_restaurant_info(href), restaurant, city, state)
    time.sleep(1)
print('\nInformación de restaurantes completa')


df_cities.to_csv('Data/cities.csv', index=True)
df_restaurants.to_csv('Data/restaurants.csv', index=True)
df_restaurants_info.to_csv('Data/restaurants_info.csv', index=True)