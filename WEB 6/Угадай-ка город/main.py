import requests
import os
from scale import scale
from io import BytesIO
import pygame
import random

pygame.init()

CITY = ['Санкт-Петербург', 'Москва', 'Казань', 'Калининград',
        'Нижний Новгород', 'Архангельск', 'Суздаль', 'Псков']


class Show:
    def __init__(self, imgs):
        self.size = self.width, self.height = 600, 450
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.imgs = imgs
        self.img = self.imgs[0]
        self.index = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYUP:
                    self.index += 1
                    try:
                        self.img = self.imgs[self.index]
                    except IndexError:
                        self.index = 0
                        self.img = self.imgs[self.index]
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
        exit()
    else:
        return response.json()


def response_map(apikey, map_api_server, l, ll, spn):
    map_params = {
        "l": l,
        "ll": ll,
        "spn": spn,
        "apikey": apikey
    }
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print('There are no matches(map)')
        print(response.url)
        print(f'Http статус: {response.status_code} ({response.reason})')
        exit()
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
    spn = ','.join(scale([list(map(float, size['upperCorner'].split(' '))),
                          list(map(float, toponym_coodrinates.split(' ')))]))
    bite_map = response_map(APIKEY_MAP, MAP_API_SERVER, 'sat', address_ll, spn)
    return bite_map


def main():
    random.shuffle(CITY)
    toponyms = [create_image(city) for city in CITY]
    map_file = []
    for number, value in enumerate(toponyms):
        with open(f'map{number}.png', "wb") as file:
            map_file.append(f'map{number}.png')
            file.write(value)
    Show(map_file)
    for i in range(len(toponyms)):
        os.remove(f'map{i}.png')


if __name__ == '__main__':
    main()
