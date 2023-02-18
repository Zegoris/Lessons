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


toponym_to_find = input()

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    print('There are no matches')
    exit()

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'

address_ll = ",".join([toponym_longitude, toponym_lattitude])

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    print('There are no matches')
else:
    json_response = response.json()
    organization = json_response["features"][0]
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    org_time = organization["properties"]["CompanyMetaData"]['Hours']

    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    size = json_response['properties']['ResponseMetaData']['SearchResponse']['boundedBy']
    size = [[float(toponym_longitude), float(toponym_lattitude)], [size[1][0], size[1][1]]]
    delta_x, delta_y = scale(size)

    map_params = {
        "spn": ",".join([delta_x, delta_y]),
        "l": "map",
        "pt": f"{org_point},pm2dgl~{address_ll},pm2dgl",
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b'
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(response.content)).show()
    snippet = [org_address, org_name,
               org_time, lonlat_distance(toponym_coodrinates.split(' '), [size[0][0], size[0][1]])]
    print(snippet)