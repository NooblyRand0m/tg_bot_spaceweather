import requests
from bs4 import BeautifulSoup


def get_eclipse_data():
    url = 'https://www.timeanddate.com/eclipse/list.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    eclipse_info = soup.find_all('a', {'class': 'ec-link'})
    result = []
    for i in range(2):
        eclipse_type = eclipse_info[i].find('span', {'class': 'ec-type'}).text
        eclipse_date = eclipse_info[i].find('span', {'class': 'ec-date'}).text
        eclipse_location = eclipse_info[i].find('span', {'class': 'ec-where'}).text
        result.append(f'{eclipse_type}, on {eclipse_date}, location {eclipse_location}')
    return '\n'.join(result)


def get_solar_activity():
    url = 'https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json'
    response = requests.get(url)
    data = response.json()
    solar_flare_class = data[0]['max_class']
    solar_flare_date = data[0]['time_tag']
    return [solar_flare_class, solar_flare_date]


def get_geo_activity():
    url = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'
    response = requests.get(url)
    data = response.json()
    kp_index = data[-1]['kp_index']
    kp_date = data[-1]['time_tag']
    return [kp_index, kp_date]
