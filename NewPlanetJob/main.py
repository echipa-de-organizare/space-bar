import os
import random
import time
import timeit
from math import ceil
from random import randint

import cv2
import pygame

# initialize game window
from Resources.resourcesnewplanetjob.utils import *

random.seed(time.time())

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("New planet job")
pygame.display.set_icon(pygame.image.load("Resources/resourcesnewplanetjob/bg2.png"))


def place_bg():
    radio = pygame.image.load("Resources/resourcesnewplanetjob/bg2.png")
    x, y = screen.get_size()
    radio = pygame.transform.scale(radio, (x, y))
    return screen.blit(radio, (0, 0))


def place_line(mousex, mousey):
    line = pygame.image.load("Resources/resourcesnewplanetjob/line.png")
    x, y = screen.get_size()
    bait = pygame.transform.scale(line, (ceil(0.01 * line.get_size()[0]), mousey))
    return screen.blit(bait, (ceil(0.4569 * x), (ceil(0.05 * y))))


def place_bait(mousex, mousey):
    bait = pygame.image.load("Resources/resourcesnewplanetjob/bait.png")
    x, y = screen.get_size()
    bait = pygame.transform.scale(bait, (ceil(0.7 * bait.get_size()[0]), ceil(0.7 * bait.get_size()[1])))
    return screen.blit(bait, (ceil(0.43 * x), mousey))


fish_lr_paths = ["Resources/resourcesnewplanetjob/fishlr1.png"]
fish_rl_paths = ["Resources/resourcesnewplanetjob/fishrl1.png"]


def place_fish_lr(x_pos, y_pos):
    fish = pygame.image.load(random.choice(fish_lr_paths))
    x, y = screen.get_size()
    fish = pygame.transform.scale(fish, (ceil(0.9 * fish.get_size()[0]), ceil(0.9 * fish.get_size()[1])))
    # surface = pygame.Surface(fish.get_size())
    # surface.blit(fish, (0, 0))
    screen.blit(fish, (x_pos, y_pos))
    return fish, (x_pos, y_pos)


def place_fish_rl(x_pos, y_pos):
    fish = pygame.image.load(random.choice(fish_rl_paths))
    x, y = screen.get_size()
    fish = pygame.transform.scale(fish, (ceil(0.8 * fish.get_size()[0]), ceil(0.8 * fish.get_size()[1])))
    # surface = pygame.Surface(fish.get_size())
    # surface.blit(fish, (0, 0))
    screen.blit(fish, (x_pos, y_pos))
    return fish, (x_pos, y_pos)


fish_list = []


def place_all_fish():
    global fish_list
    i = 0
    while i < len(fish_list):
        state = fish_list[i][0]
        if state == 0:
            coords_copy = (fish_list[i][1][1][0] + 28, fish_list[i][1][1][1])
            fish, coords = fish_list[i][1]
            screen.blit(fish, coords)
            del fish_list[i]
            x, y = screen.get_size()
            if coords_copy[0] <= x + 200:
                fish_list.insert(i, (state, (fish, coords_copy)))
            else:
                i -= 1
        else:
            coords_copy = (fish_list[i][1][1][0] - 28, fish_list[i][1][1][1])
            fish, coords = fish_list[i][1]
            screen.blit(fish, coords)
            del fish_list[i]
            if coords_copy[0] > -200:
                fish_list.insert(i, (state, (fish, coords_copy)))
            else:
                i -= 1
        i += 1


spacebarlogT = os.path.expanduser("~\\Documents\\spacebarlogT.txt")
spacebarlogP = os.path.expanduser("~\\Documents\\spacebarlogP.txt")
spacebarlogS = os.path.expanduser("~\\Documents\\spacebarlogS.txt")
spacebarlogL = os.path.expanduser("~\\Documents\\spacebarlogL.txt")


def write_to_next_planet_file():
    with open(spacebarlogP, "w") as f:
        f.write(str(1))


def write_state(state):
    with open(spacebarlogS, "w") as f:
        f.truncate()
        f.write(str(state))


def write_location():
    with open(spacebarlogL, "w") as f:
        f.truncate()
        f.write("0\n0")


# background space music
# todo: uncomment bgmusic
# background_music = pygame.mixer.Channel(0)
# background_music.play(pygame.mixer.Sound("Resources/resourcesnewplanetjob/bgmusic.mp3"), loops=-1, fade_ms=5000)
# background_music.set_volume(0)

# # opencv2
x, y = screen.get_size()
video = cv2.VideoCapture("")
fps = video.get(cv2.CAP_PROP_FPS)
clock = pygame.time.Clock()
video_size = (ceil(0.5 * x), ceil(0.5 * y))
video_placement = (ceil(0.24 * x), ceil(0.15 * y))


def check_fish_caught(mousex, mousey):
    x, y = screen.get_size()
    global fish_list
    i = 0
    while i < len(fish_list):
        fish, coords = fish_list[i][1]
        if ceil(0.43 * x) - 100 <= coords[0] <= ceil(0.43 * x) + 100 and mousey - 100 <= coords[1] <= mousey + 100:
            # if abs(coords[0] - ceil(0.43 * x)) <= 250 and abs(coords[1] - mousey) <= 250:
            del fish_list[i]
            i -= 1
        i += 1


if __name__ == '__main__':
    running = True
    arr_index = 0
    y_pos = ceil(0.75 * screen.get_size()[1])

    show_good, show_perfect, show_bad, show_wrong, arrow_state = False, False, False, False, 0
    score, score_put, score_villain = 0, False, 0
    dec_index = False
    END_IT_ALL = False

    WON = pygame.USEREVENT + 3

    PLACE_FISH = pygame.USEREVENT + 4
    pygame.time.set_timer(PLACE_FISH, 1500)

    local_start = timeit.default_timer()
    mousex, mousey = 0, 0
    while running:
        random.seed(time.time())
        # clock.tick(60)
        y_pos += 8
        place_bg()
        place_line(mousex, mousey)
        place_bait(mousex, mousey)
        place_all_fish()
        # draw_clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = pygame.mouse.get_pos()
                check_fish_caught(mousex, mousey)
            if event.type == WON:
                # todo: uncomment music
                # background_music.stop()
                write_to_next_planet_file()
                write_state(3)
                pygame.quit()
                running = False
                break
            if event.type == PLACE_FISH:
                x, y = screen.get_size()
                if random.random() < 0.5:
                    fish_list.append((0, place_fish_lr(-200, random.randint(ceil(0.2 * y), ceil(0.9 * y)))))
                else:
                    fish_list.append((1, place_fish_rl(x + 200, random.randint(ceil(0.2 * y), ceil(0.9 * y)))))
            if event.type == pygame.KEYDOWN:
                pass
        if running:
            pygame.display.flip()
    pygame.quit()
