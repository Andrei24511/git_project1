import sys
import pygame
import requests


def geocoder(tf):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": tf,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    return json_response


def load_map(mp):
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(mp)
    return map_file


def select_params(js, n):
    toponym = js["response"]["GeoObjectCollection"]["featureMember"][n]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    upper = list(map(float, toponym['boundedBy']["Envelope"]["upperCorner"].split()))
    lower = list(map(float, toponym['boundedBy']["Envelope"]["lowerCorner"].split()))
    s1 = str(upper[0] - lower[0])
    s2 = str(upper[1] - lower[1])
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([s1, s2]),
        "l": "map"
    }
    return map_params


def main():
    pygame.init()
    pygame.display.set_caption('Maps API')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    toponym_to_find = 'Москва, ул. Ак. Королева, 12'
    map_params = select_params(geocoder(toponym_to_find), 0)
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    im = pygame.image.load(load_map(response.content))
    x, y = im.get_rect().size
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(im, ((width - x) / 2, (height - y) / 2))
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
