import requests
from scale import scale
from io import BytesIO
from PIL import Image
import math


def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distanc = math.sqrt(dx * dx + dy * dy)

    return distanc


def response_toponym(apikey, geocoder_api_server, geocode, format, kind=None):
    geocoder_params = {
        "apikey": apikey,
        "geocode": geocode,
        "format": format
    }
    if kind is not None:
        geocoder_params['kind'] = kind
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print('There are no matches(toponym)')
        print(response.url)
        print(f'Http статус: {response.status_code} ({response.reason})')
        exit()
    else:
        return response.json()


def response_org(apikey, search_api_server, ll, object, type):
    search_params = {
        "apikey": apikey,
        "text": object,
        "lang": "ru_RU",
        "ll": ll,
        "results": 10,
        "type": type
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print('There are no matches(organizations)')
        print(response.url)
        print(f'Http статус: {response.status_code} ({response.reason})')
        exit()
    else:
        return response.json()


def response_map(apikey, map_api_server, l, ll, pt):
    map_params = {
        "l": l,
        "ll": ll,
        "pt": pt,
        'apikey': apikey
    }
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print('There are no matches(map)')
        print(response.url)
        print(f'Http статус: {response.status_code} ({response.reason})')
        exit()
    else:
        return response.content


def point_color(coords, meta_data):
    try:
        if meta_data['Hours']['Availabilities']['Everyday']:
            return f'{coords},pm2gnm'
        else:
            return f'{coords},pm2ntm'
    except KeyError:
        return f'{coords},pm2grm'
    except TypeError:
        return f'{coords},pm2ntm'


def main():
    toponym_to_find = input()
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    apikey_toponym = "40d1649f-0493-4b70-98ba-98533de7710b"
    json_toponym = response_toponym(apikey_toponym, geocoder_api_server,
                                    toponym_to_find, 'json')
    toponym = json_toponym["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = ','.join(toponym["Point"]["pos"].split(' '))

    json_toponym_r = response_toponym(apikey_toponym, geocoder_api_server,
                                    toponym_coodrinates, 'json', kind='district')
    district = json_toponym_r['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
    print(district)


if __name__ == '__main__':
    main()