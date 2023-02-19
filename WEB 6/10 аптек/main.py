import requests
from scale import scale
import sys
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


def response_toponym(apikey, geocoder_api_server, geocode, format):
    geocoder_params = {
        "apikey": apikey,
        "geocode": geocode,
        "format": format
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print('There are no matches(toponym)')
        exit()
    else:
        return response.json()


def response_org(apikey, search_api_server, ll, org):
    search_params = {
        "apikey": apikey,
        "text": org,
        "lang": "ru_RU",
        "ll": ll,
        "results": 10,
        "type": "biz"
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print('There are no matches(organizations)')
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

    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_latitude = toponym_coodrinates.split(" ")
    search_api_server = "https://search-maps.yandex.ru/v1/"
    apikey_org = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    address_ll = ",".join([toponym_longitude, toponym_latitude])
    json_orgs = response_org(apikey_org, search_api_server,
                             address_ll, 'аптека')

    organizations = json_orgs["features"]
    points, snippets = [f'{address_ll},round'], []
    for organization in organizations:
        coord = organization["geometry"]["coordinates"]
        meta_data = organization["properties"]["CompanyMetaData"]
        org_name = organization["properties"]["CompanyMetaData"]["name"]
        org_address = organization["properties"]["CompanyMetaData"]["address"]
        org_time = organization["properties"]["CompanyMetaData"]['Hours']
        point = organization["geometry"]["coordinates"]
        points.append(point_color(f'{coord[0]},{coord[1]}', meta_data))
        snippets.append([org_address, org_name,
                         org_time, lonlat_distance([float(toponym_longitude),
                                                    float(toponym_latitude)], point)])
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    apikey_map = '40d1649f-0493-4b70-98ba-98533de7710b'
    bite_map = response_map(apikey_map, map_api_server,
                            'map', address_ll, '~'.join(points))

    Image.open(BytesIO(bite_map)).show()
    print(snippets)


if __name__ == '__main__':
    main()
