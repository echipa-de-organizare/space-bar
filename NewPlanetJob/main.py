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


fish_paths = ["Resources/resourcesnewplanetjob/fish1.png"]


def place_fish(x_pos, y_pos):
    fish = pygame.image.load(random.choice(fish_paths))
    x, y = screen.get_size()
    fish = pygame.transform.scale(fish, (ceil(0.7 * fish.get_size()[0]), ceil(0.7 * fish.get_size()[1])))
    # surface = pygame.Surface(fish.get_size())
    # surface.blit(fish, (0, 0))
    screen.blit(fish, (x_pos, y_pos))
    return fish, (x_pos, y_pos)


fish_list = []


def place_all_fish():
    global fish_list
    for i in range(len(fish_list)):
        coords_copy = (fish_list[i][1][0] + 8, fish_list[i][1][1])
        fish, coords = fish_list[i]
        screen.blit(fish, coords)
        fish_list.pop(i)
        fish_list.insert(i, (fish, coords_copy))


# def place_arrow(direction, state, y_pos):
#     arrow = pygame.image.load(icon_active_paths[direction])
#     # if state == 0:
#     #     arrow = pygame.image.load(icon_active_paths[direction])
#     if state == 1:
#         arrow = pygame.image.load(icon_good_paths[direction])
#     elif state == 2:
#         arrow = pygame.image.load(icon_bad_paths[direction])
#     x, y = screen.get_size()
#     arrow = pygame.transform.scale(arrow, (70, 70))
#     return screen.blit(arrow, (ceil(0.478 * x), y_pos))
#
#
# def place_circle():
#     circle = pygame.image.load("Resources/resourcesendplanet/circle.png")
#     x, y = screen.get_size()
#     circle = pygame.transform.scale(circle, (80, 80))
#     return screen.blit(circle, (ceil(0.475 * x), ceil(0.85 * y)))


spacebarlogT = os.path.expanduser("~\\Documents\\spacebarlogT.txt")
spacebarlogP = os.path.expanduser("~\\Documents\\spacebarlogP.txt")
spacebarlogS = os.path.expanduser("~\\Documents\\spacebarlogS.txt")
spacebarlogL = os.path.expanduser("~\\Documents\\spacebarlogL.txt")
global_seconds = 0
local_start = 0
local_end = 0


def write_to_next_planet_file():
    with open(spacebarlogP, "w") as f:
        f.write(str(1))


# def write_seconds():
#     global global_seconds, local_start, local_end
#     new_seconds = global_seconds + local_end - local_start
#     with open(spacebarlogT, "w") as f:
#         f.truncate()
#         f.write(str(int(new_seconds)))


def write_state(state):
    with open(spacebarlogS, "w") as f:
        f.truncate()
        f.write(str(state))


def write_location():
    with open(spacebarlogL, "w") as f:
        f.truncate()
        f.write("0\n0")


# background space music
background_music = pygame.mixer.Channel(0)
errorsoundeffect_music = pygame.mixer.Channel(1)
validsoundeffect_music = pygame.mixer.Channel(2)
background_music.play(pygame.mixer.Sound("Resources/resourcesnewplanetjob/bgmusic.mp3"), loops=-1, fade_ms=5000)

# # opencv2
x, y = screen.get_size()
video = cv2.VideoCapture("")
fps = video.get(cv2.CAP_PROP_FPS)
clock = pygame.time.Clock()
video_size = (ceil(0.5 * x), ceil(0.5 * y))
video_placement = (ceil(0.24 * x), ceil(0.15 * y))


# def read_seconds():
#     global global_seconds
#     with open(spacebarlogT, "r") as f:
#         global_seconds = int(f.readline().strip())


# def set_clock(global_seconds):
#     global current_minute, current_second
#     new_sec = (global_seconds + current_second) % 60
#     new_min = current_minute + (global_seconds + current_second) // 60
#     current_second = new_sec
#     current_minute = new_min
#
#
# def draw_clock():
#     pygame.font.init()
#     font = pygame.font.SysFont("Trebuchet MS", 25)
#     day_text = font.render("Date: 19 January 2038", True, BLACK)
#     hour_text = font.render("Time: 03", True, BLACK)  # zero-pad hours to 2 digits
#     minute_text = font.render(":{0:02}".format(current_minute), True, BLACK)  # zero-pad minutes to 2 digits
#     second_text = font.render(":{0:02}".format(current_second), True, BLACK)  # zero-pad minutes to 2 digits
#     day_placement = (50, 50)
#     hour_placement = (day_placement[0], day_placement[1] + day_text.get_size()[1])
#     minute_placement = (hour_placement[0] + hour_text.get_size()[0], hour_placement[1])
#     second_placement = (minute_placement[0] + second_text.get_size()[0], minute_placement[1])
#     screen.blit(day_text, day_placement)
#     screen.blit(hour_text, hour_placement)
#     screen.blit(minute_text, minute_placement)
#     screen.blit(second_text, second_placement)


# Time Info
# Time = 0
# current_minute = 9
# current_second = 7
if __name__ == '__main__':
    running = True
    arr_index = 0
    y_pos = ceil(0.75 * screen.get_size()[1])
    PLACE_RANDOM_ARROW_EVENT = pygame.USEREVENT
    # pygame.time.set_timer(PLACE_RANDOM_ARROW_EVENT, 3500)

    # SHOW_SCORE = pygame.USEREVENT + 1
    show_good, show_perfect, show_bad, show_wrong, arrow_state = False, False, False, False, 0
    score, score_put, score_villain = 0, False, 0
    dec_index = False
    END_IT_ALL = False

    # read_seconds()
    # TIMES_UP = pygame.USEREVENT + 1
    # pygame.time.set_timer(TIMES_UP, (300 - global_seconds) * 1000)

    Clock = pygame.time.Clock()
    CLOCKTICK = pygame.USEREVENT + 2
    # set_clock(global_seconds)

    WON = pygame.USEREVENT + 3

    PLACE_FISH = pygame.USEREVENT + 4
    pygame.time.set_timer(PLACE_FISH, 2000)

    local_start = timeit.default_timer()
    pygame.time.set_timer(PLACE_RANDOM_ARROW_EVENT, 3500)
    # pygame.time.set_timer(TIMES_UP, (300 - global_seconds) * 1000)
    # pygame.time.set_timer(CLOCKTICK, 1000)
    mousex, mousey = 0, 0
    while running:
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
                # place_bait(mousex, mousey)
                pass
            if event.type == WON:
                background_music.stop()
                validsoundeffect_music.stop()
                errorsoundeffect_music.stop()
                write_to_next_planet_file()
                # local_end = local_start - global_seconds
                # write_seconds()
                write_state(3)
                # write_location()
                pygame.quit()
                running = False
                break
            if event.type == PLACE_FISH:
                x, y = screen.get_size()
                fish_list.append(place_fish(0, random.randint(ceil(0.2 * y), ceil(0.9 * y))))
            # if event.type == CLOCKTICK:
            #     current_second = current_second + 1
            #     if current_second == 60:
            #         current_second = 0
            #         current_minute = current_minute + 1
            # if event.type == TIMES_UP:
            #     draw_clock()
            #     pygame.display.flip()
            #     pygame.time.delay(1000)
            #     background_music.stop()
            #     validsoundeffect_music.stop()
            #     errorsoundeffect_music.stop()
            #     write_to_next_planet_file()
            #     local_end = local_start - global_seconds
            #     write_seconds()
            #     write_state(2)
            #     write_location()
            #     pygame.quit()
            #     running = False
            #     break
            if event.type == PLACE_RANDOM_ARROW_EVENT:
                pass
            if event.type == pygame.KEYDOWN:
                pass
        if running:
            # draw_clock()
            pygame.display.flip()
    pygame.quit()
