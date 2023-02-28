import os
import sys
import pygame

pygame.init()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


FPS = 50

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    level_map = list(map(lambda x: x.ljust(max_width, '.'), level_map))
    return [[char for char in line.strip()] for line in level_map]


def moving(x0, y0):
    global player, level_x, level_y, level_map
    for y in range(len(level_map)):
        for x in range(len(level_map[y])):
            if level_map[y][x] == '@' and level_map[y + y0][x + x0] != '#':
                level_map[y][x] = '.'
                level_map[y + y0][x + x0] = '@'
                if y0 == 1:
                    level_map.insert(-1, level_map[0])
                    level_map.pop(0)
                elif y0 == -1:
                    level_map.insert(0, level_map[-1])
                    level_map.pop(-1)
                elif x0 == 1:
                    buffer = []
                    for y in range(len(level_map)):
                        buf = level_map[y]
                        buf.insert(-1, buf[0])
                        buf.pop(0)
                        buffer.append(buf)
                    level_map = buffer
                elif x0 == -1:
                    buffer = []
                    for y in range(len(level_map)):
                        buf = level_map[y]
                        buf.insert(0, buf[-1])
                        buf.pop(-1)
                        buffer.append(buf)
                    level_map = buffer
                player, level_x, level_y = generate_level(level_map)
                return


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
level_map = load_level('map.txt')

if __name__ == '__main__':
    size = width, height = 550, 500
    screen = pygame.display.set_mode(size)
    screen.fill('blue')
    clock = pygame.time.Clock()
    start_screen()
    player, level_x, level_y = generate_level(level_map)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    moving(0, 1)
                if event.key == pygame.K_UP:
                    moving(0, -1)
                if event.key == pygame.K_LEFT:
                    moving(-1, 0)
                if event.key == pygame.K_RIGHT:
                    moving(1, 0)
        screen.fill('black')
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
