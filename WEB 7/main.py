import requests
import os
import pygame
import json

pygame.init()

CITY = input('Input coords:\n').replace(' ', '')
with open('settings.json') as file:
    data = json.load(file)
    data["Coords"] = f'{CITY},round'
    with open("settings.json", "w") as file:
        json.dump(data, file, indent=1)

class Show:
    def __init__(self, img):
        global CITY
        self.size = self.width, self.height = 600, 450
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.img = img
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        buffer = list(map(float, CITY.split(',')))
                        buffer[1] += 0.1
                        buffer = list(map(str, buffer))
                        CITY = ','.join(buffer)
                        with open('map.png', "wb") as file:
                            file.write(create_image(CITY))
                        self.img = 'map.png'
                    if event.key == pygame.K_DOWN:
                        buffer = list(map(float, CITY.split(',')))
                        buffer[1] -= 0.1
                        buffer = list(map(str, buffer))
                        CITY = ','.join(buffer)
                        with open('map.png', "wb") as file:
                            file.write(create_image(CITY))
                        self.img = 'map.png'
                    if event.key == pygame.K_RIGHT:
                        buffer = list(map(float, CITY.split(',')))
                        buffer[0] += 0.1
                        buffer = list(map(str, buffer))
                        CITY = ','.join(buffer)
                        with open('map.png', "wb") as file:
                            file.write(create_image(CITY))
                        self.img = 'map.png'
                    if event.key == pygame.K_LEFT:
                        buffer = list(map(float, CITY.split(',')))
                        buffer[1] -= 0.1
                        buffer = list(map(str, buffer))
                        CITY = ','.join(buffer)
                        with open('map.png', "wb") as file:
                            file.write(create_image(CITY))
                        self.img = 'map.png'
            self.render()

    def render(self):
        self.screen.blit(pygame.image.load(self.img), (0, 0))
        pygame.display.flip()

def response_toponym(apikey, geocoder_api_server, geocode, format):
    geocoder_params = {
        "apikey": apikey,
        "geocode": geocode,
        "format": format
    }
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print('There are no matches(toponym)')
        print(response.url)
        print(f'Http статус: {response.status_code} ({response.reason})')
    else:
        return response.json()


def response_map(apikey, map_api_server, l, ll, spn, pt):
    map_params = {
        "l": l,
        "ll": ll,
        "spn": spn,
        "pt": pt,
        "apikey": apikey
    }
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print('There are no matches(map)')
        print(response.url)
        print(f'Http статус: {response.status_code} ({response.reason})')
    else:
        return response.content


def create_image(toponym_to_find):

    GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
    APIKEY_TOPONYM = "40d1649f-0493-4b70-98ba-98533de7710b"
    json_toponym = response_toponym(APIKEY_TOPONYM, GEOCODER_API_SERVER,
                                    toponym_to_find, 'json')
    toponym = json_toponym["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    size = toponym['boundedBy']['Envelope']

    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_latitude = toponym_coodrinates.split(" ")
    address_ll = ",".join([toponym_longitude, toponym_latitude])

    MAP_API_SERVER = "http://static-maps.yandex.ru/1.x/"
    APIKEY_MAP = '40d1649f-0493-4b70-98ba-98533de7710b'
    size = [list(map(float, size['upperCorner'].split(' '))),
            list(map(float, toponym_coodrinates.split(' ')))]
    longitude = round(abs(size[0][0] - size[1][0]), 4)
    latitude = round(abs(size[0][1] - size[1][1]), 4)
    spn = ','.join((str(longitude), str(latitude)))
    with open("settings.json") as file:
        data = json.load(file)
        pt = data['Coords']
    bite_map = response_map(APIKEY_MAP, MAP_API_SERVER, 'sat', address_ll, spn, pt)
    return bite_map


def main():
    try:
        map_file = ''
        with open(f'map.png', "wb") as file:
            map_file = 'map.png'
            file.write(create_image(CITY))
        Show(map_file)
    except Exception:
        pass
    os.remove(f'map.png')
    with open('settings.json') as file:
        data = json.load(file)
        data["Coords"] = False
        with open("settings.json", "w") as file:
            json.dump(data, file, indent=1)



if __name__ == '__main__':
    main()
