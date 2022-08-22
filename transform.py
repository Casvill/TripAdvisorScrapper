import pandas as pd

__cities_list = []
__restaurant_list = []
__restaurant_info_list = []

#-----------------------------------------------------------------------------------------------------------------------

def __transform_cities_firts_page(soup):
    #print('transform_cities_firts_page')
    divs = soup.find_all('div', class_='geo_wrap')

    for item in divs:
        city =  item.find('a').text
        href =  item.find('a')['href']

        city ={'city': city, 'href': href}
        __cities_list.append(city)



def __transform_cities_2(soup):
    #print('transform_cities_2')
    for ultag in soup.find_all('ul', {'class': 'geoList'}):
        for litag in ultag.find_all('li'):
            city= litag.text
            href= litag.find('a')['href']
            city = {'city':city,'href':href}
            __cities_list.append(city)



def transform_cities(soup,page) -> list:
    #print('transform_cities')
    if page == 1:
        __transform_cities_firts_page(soup)
    else:
        __transform_cities_2(soup)


    df_cities = pd.DataFrame(__cities_list)

    df_cities['city'] = df_cities['city'].str.lstrip('Restaurantes en ')
    df_cities['state'] =''

    for i in range(len(df_cities)):
        if '\n-' in df_cities['city'][i]:
            df_cities['state'][i] = df_cities['city'][i].split('\n-')[1]
            df_cities['city'][i] = df_cities['city'][i].split('\n-')[0]


    return df_cities
#-----------------------------------------------------------------------------------------------------------------------


def transform_restaurant_names(soup,page,df_cities):
    #print('transform_restaurant_names')
    #print('page:',page)
    divs = soup.find_all('div', class_='zdCeB Vt o')

    for item in divs:
        if '.' in item.find('a', class_='Lwqic Cj b').text:

            restaurant =  item.find('a', class_='Lwqic Cj b').text.split('.')[1]
            href = item.find('a', class_='Lwqic Cj b')['href']
            

            restaurants ={'id':page,
                          'restaurant': restaurant, 
                          'href':href}
                        
            __restaurant_list.append(restaurants)

    df_restaurant = pd.DataFrame(__restaurant_list)
    df_restaurant = df_restaurant.merge(df_cities, left_on='id', right_on='href')
    df_restaurant.drop(columns=['id','href_y'], inplace=True)
    df_restaurant.rename(columns={'href_x':'href'}, inplace=True)

    return df_restaurant

#-----------------------------------------------------------------------------------------------------------------------


def transform_restaurants_info(soup,restaurant,city,state):
    print('\nrestaurante:', restaurant, '\nciudad:', city)

    calification = ''
    number_of_reviwes = ''
    ranking = ''
    address = ''
    web_site = ''
    latitude = ''
    longitude = ''

    div = soup.find('div', class_='YDAvY R2 F1 e k')
    for item in div:
        try:
            calification = item.find('span', class_='ZDEqb').text
            # print('calification:',calification)
        except:
            pass

        try:
            number_of_reviwes = item.find('a', class_='IcelI').text.rstrip(' opiniones')
            # print('number_of_reviwes:',number_of_reviwes)
        except:
            pass


    div = soup.find_all('div', class_='vQlTa H3')
    for item in div:
        try:
            ranking = item.find('span', class_='DsyBj cNFrA').text.split(' ')[0]
            # print('ranking:',ranking)
            break
        except:
            pass


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
            pass


    items = soup.find_all('div', class_='kDZhm IdiaP Me')
    for item in items:
        try:
            coordinates = item.find('a', class_='YnKZo Ci Wc _S C FPPgD')['href']
            coordinates = coordinates.split('@')[-1]
            latitude = coordinates.split(',')[0]
            longitude = coordinates.split(',')[1]
            # print('latitude:',latitude)
            # print('longite:',longitude)
        except:
            pass


    restaurants_info= {'city':city,
                       'state':state,
                       'restaurant':restaurant,
                       'calification': calification,
                       'number_of_reviwes': number_of_reviwes,
                       'ranking': ranking,
                       'address': address,
                       'web_site': web_site,
                       'latitude': latitude,
                       'longitude': longitude}

    __restaurant_info_list.append(restaurants_info)

    df_restaurant_info = pd.DataFrame(__restaurant_info_list)

    return df_restaurant_info