import extract
import transform
import pandas as pd



for i in range(1,4):
    soup,page = extract.extract_cities(i)
    df_cities = transform.transform_cities( soup,page )
    print('1')


for href in df_cities['href'][:4]:
    soup,page = extract.extract_restaurants_name(href)
    df_restaurants = transform.transform_restaurants_name(soup,page,df_cities)
    print('2')

for i in range(2):
    href = df_restaurants['href'][i]
    restaurant = df_restaurants['restaurant'][i]
    city = df_restaurants['city'][i]
    state =df_restaurants['state'][i]

    df_restaurants_info = transform.transform_restaurants_info(extract.extract_restaurants_info(href), restaurant, city, state)
    print('3')


df_cities.to_csv('cities.csv', index=False)
df_restaurants.to_csv('restaurants.csv', index=False)
df_restaurants_info.to_csv('restaurants_info.csv', index=False)