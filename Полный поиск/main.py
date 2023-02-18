import requests
from scale import scale

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'

address_ll = "37.588392,55.734036"

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

    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    size = json_response['properties']['ResponseMetaData']['SearchResponse']['boundedBy']
    delta_x, delta_y = scale(size)

    map_params = {
        "ll": address_ll,
        "spn": ",".join([delta_x, delta_y]),
        "l": "map",
        "pt": "{0},pm2dgl".format(org_point),
        'apikey': '40d1649f-0493-4b70-98ba-98533de7710b'
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
