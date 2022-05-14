import os
import random
import time
import timeit
from math import ceil
from random import randint

import cv2
import pygame

# initialize game window
from Resources.resourcesendplanet.utils import *

random.seed(time.time())
directions = [randint(0, 3) for _ in range(10)]
sequence_states = [0 for _ in range(10)]
# directions = [0 for i in range(20)]
icon_paths = ["Resources/resourcesendplanet/up.png", "Resources/resourcesendplanet/right.png",
              "Resources/resourcesendplanet/down.png", "Resources/resourcesendplanet/left.png"]
icon_active_paths = ["Resources/resourcesendplanet/upactive.png", "Resources/resourcesendplanet/rightactive.png",
                     "Resources/resourcesendplanet/downactive.png",
                     "Resources/resourcesendplanet/leftactive.png"]
icon_good_paths = ["Resources/resourcesendplanet/upgood.png", "Resources/resourcesendplanet/rightgood.png",
                   "Resources/resourcesendplanet/downgood.png",
                   "Resources/resourcesendplanet/leftgood.png"]
icon_bad_paths = ["Resources/resourcesendplanet/upbad.png", "Resources/resourcesendplanet/rightbad.png",
                  "Resources/resourcesendplanet/downbad.png", "Resources/resourcesendplanet/leftbad.png"]

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("End planet")
pygame.display.set_icon(pygame.image.load("Resources/resourcesendplanet/bg.png"))


def place_bg():
    radio = pygame.image.load("Resources/resourcesendplanet/bgdarkest.png")
    x, y = screen.get_size()
    radio = pygame.transform.scale(radio, (x, y))
    return screen.blit(radio, (0, 0))


def place_arrow(direction, state, y_pos):
    arrow = pygame.image.load(icon_active_paths[direction])
    # if state == 0:
    #     arrow = pygame.image.load(icon_active_paths[direction])
    if state == 1:
        arrow = pygame.image.load(icon_good_paths[direction])
    elif state == 2:
        arrow = pygame.image.load(icon_bad_paths[direction])
    x, y = screen.get_size()
    arrow = pygame.transform.scale(arrow, (70, 70))
    return screen.blit(arrow, (ceil(0.478 * x), y_pos))


def place_circle():
    circle = pygame.image.load("Resources/resourcesendplanet/circle.png")
    x, y = screen.get_size()
    circle = pygame.transform.scale(circle, (80, 80))
    return screen.blit(circle, (ceil(0.475 * x), ceil(0.85 * y)))


def place_score(score, score_villain):
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 40)
    text1 = font.render("Your score: " + str(score), True, (255, 255, 255))
    text2 = font.render("Gadbuy's score: " + str(score_villain), True, (255, 255, 255))
    x, y = screen.get_size()
    textRect1 = text1.get_rect()
    textRect1.center = (ceil(0.85 * x), ceil(0.3 * y))
    screen.blit(text1, textRect1)
    textRect2 = text2.get_rect()
    textRect2.center = (ceil(0.85 * x), ceil(0.38 * y))
    screen.blit(text2, textRect2)


text_placement = (ceil(0.48 * screen.get_width()), ceil(0.16 * screen.get_height()))


def place_perfect():
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 50)
    text = font.render("Perfect!", True, (255, 255, 255))
    x, y = screen.get_size()
    textRect = text.get_rect()
    textRect.center = text_placement
    screen.blit(text, textRect)


def place_good():
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 50)
    text = font.render("Good!", True, (255, 255, 255))
    x, y = screen.get_size()
    textRect = text.get_rect()
    textRect.center = text_placement
    screen.blit(text, textRect)


def place_sequence():
    x, y = screen.get_size()
    surface = pygame.Surface((550, 55))
    surface.fill((0, 5, 0))
    surface.set_alpha(240)
    screen.blit(surface, (ceil(0.345 * x), ceil(0.05 * y)))

    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 30)
    text = font.render("Code sequence: ", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (ceil(0.28 * x), ceil(0.07 * y))
    screen.blit(text, textRect)

    for i in range(len(directions)):
        arrow = pygame.image.load(icon_active_paths[directions[i]])
        if sequence_states[i] == 1:
            arrow = pygame.image.load(icon_good_paths[directions[i]])
        elif sequence_states[i] == 2:
            arrow = pygame.image.load(icon_bad_paths[directions[i]])
        x, y = screen.get_size()
        arrow = pygame.transform.scale(arrow, (30, 30))
        screen.blit(arrow, (ceil(0.34 * x) + (i + 1) * 50, ceil(0.06 * y)))


def place_bad():
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 50)
    text = font.render("Bad!", True, (255, 255, 255))
    x, y = screen.get_size()
    textRect = text.get_rect()
    textRect.center = text_placement
    screen.blit(text, textRect)


def place_wrong():
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 50)
    text = font.render("Wrong key!", True, (255, 255, 255))
    x, y = screen.get_size()
    textRect = text.get_rect()
    textRect.center = text_placement
    screen.blit(text, textRect)


def place_use_arrows():
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 40)
    text = font.render("Use keyboard arrows ->", True, (0, 255, 0))
    x, y = screen.get_size()
    textRect = text.get_rect()
    textRect.center = ceil(0.3 * screen.get_width()), ceil(0.87 * screen.get_height())
    screen.blit(text, textRect)


def place_timemachine():
    timemachine = pygame.image.load("Resources/resourcesendplanet/timemachine.png")
    imgx, imgy = timemachine.get_size()
    timemachine = pygame.transform.scale(timemachine, (ceil(0.6 * imgx), ceil(0.6 * imgy)))
    return screen.blit(timemachine, (ceil(0.19 * x), ceil(0.11 * y)))


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


def write_seconds():
    global global_seconds, local_start, local_end
    new_seconds = global_seconds + local_end - local_start
    with open(spacebarlogT, "w") as f:
        f.truncate()
        f.write(str(int(new_seconds)))


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
background_music.play(pygame.mixer.Sound("Resources/resourcesendplanet/bgmusic.mp3"), loops=-1, fade_ms=5000)

# # opencv2
x, y = screen.get_size()
video = cv2.VideoCapture("")
fps = video.get(cv2.CAP_PROP_FPS)
clock = pygame.time.Clock()
video_size = (ceil(0.5 * x), ceil(0.5 * y))
video_placement = (ceil(0.24 * x), ceil(0.15 * y))


def read_seconds():
    global global_seconds
    with open(spacebarlogT, "r") as f:
        global_seconds = int(f.readline().strip())


def set_clock(global_seconds):
    global current_minute, current_second
    new_sec = (global_seconds + current_second) % 60
    new_min = current_minute + (global_seconds + current_second) // 60
    current_second = new_sec
    current_minute = new_min


def draw_clock():
    pygame.font.init()
    font = pygame.font.SysFont("Trebuchet MS", 25)
    day_text = font.render("Date: 19 January 2038", True, WHITE)
    hour_text = font.render("Time: 03", True, WHITE)  # zero-pad hours to 2 digits
    minute_text = font.render(":{0:02}".format(current_minute), True, WHITE)  # zero-pad minutes to 2 digits
    second_text = font.render(":{0:02}".format(current_second), True, WHITE)  # zero-pad minutes to 2 digits
    day_placement = (50, 50)
    hour_placement = (day_placement[0], day_placement[1] + day_text.get_size()[1])
    minute_placement = (hour_placement[0] + hour_text.get_size()[0], hour_placement[1])
    second_placement = (minute_placement[0] + second_text.get_size()[0], minute_placement[1])
    screen.blit(day_text, day_placement)
    screen.blit(hour_text, hour_placement)
    screen.blit(minute_text, minute_placement)
    screen.blit(second_text, second_placement)


# Time Info
Time = 0
current_minute = 9
current_second = 7

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

    read_seconds()
    TIMES_UP = pygame.USEREVENT + 1
    # pygame.time.set_timer(TIMES_UP, (300 - global_seconds) * 1000)

    Clock = pygame.time.Clock()
    CLOCKTICK = pygame.USEREVENT + 2
    # pygame.time.set_timer(CLOCKTICK, 1000)
    set_clock(global_seconds)

    WON = pygame.USEREVENT + 3

    # SLIDE_DOWN = pygame.USEREVENT + 4
    # pygame.time.set_timer(SLIDE_DOWN, 1)

    local_start = timeit.default_timer()
    delay_arrow_event = True
    while running:
        # clock.tick(60)
        y_pos += 8
        place_bg()
        place_timemachine()
        place_sequence()
        place_circle()
        place_arrow(directions[arr_index], arrow_state, y_pos)
        if delay_arrow_event:
            place_use_arrows()
            pygame.display.flip()
            pygame.time.delay(4000)
            pygame.time.set_timer(PLACE_RANDOM_ARROW_EVENT, 3500)
            pygame.time.set_timer(TIMES_UP, (300 - global_seconds) * 1000)
            pygame.time.set_timer(CLOCKTICK, 1000)
            delay_arrow_event = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == SLIDE_DOWN:
            #     pass
            # y_pos += 0.1
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
            if event.type == CLOCKTICK:
                current_second = current_second + 1
                if current_second == 60:
                    current_second = 0
                    current_minute = current_minute + 1
            if event.type == TIMES_UP:
                place_arrow(directions[arr_index], arrow_state, y_pos)
                place_sequence()
                draw_clock()
                pygame.display.flip()
                pygame.time.delay(1000)
                background_music.stop()
                validsoundeffect_music.stop()
                errorsoundeffect_music.stop()
                write_to_next_planet_file()
                local_end = local_start - global_seconds
                write_seconds()
                write_state(2)
                write_location()
                pygame.quit()
                running = False
                break
            if event.type == PLACE_RANDOM_ARROW_EVENT:
                # score_villain += random.choice(
                #     [5, 5, 5, 5, 5, 5, 5, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, -1,
                #      -2])
                if not score_put:
                    sequence_states[arr_index] = 2
                    errorsoundeffect_music.play(pygame.mixer.Sound("Resources/resourcesendplanet/error_se.mp3"),
                                                loops=0)
                    pygame.event.post(pygame.event.Event(TIMES_UP))
                else:
                    y_pos = ceil(0.75 * screen.get_size()[1])
                    arrow_state = 0
                    if dec_index:
                        arr_index -= 1
                        dec_index = False
                    if arr_index == len(directions) - 1:
                        pygame.event.post(pygame.event.Event(WON))
                        # background_music.stop()
                        # validsoundeffect_music.stop()
                        # errorsoundeffect_music.stop()
                        # write_to_next_planet_file()
                        # # local_end = local_start - global_seconds
                        # # write_seconds()
                        # write_state(3)
                        # # write_location()
                        # pygame.quit()
                        # running = False
                        # break
                    if arr_index < len(directions) - 1 and score_put:
                        arr_index += 1
                    score_put = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT]:
                    # print(ceil(0.85 * screen.get_size()[1]) - 40, y_pos, ceil(0.85 * screen.get_size()[1]) + 40)
                    if (event.key == pygame.K_UP and directions[arr_index] == UP) or (
                            event.key == pygame.K_LEFT and directions[arr_index] == LEFT) or (
                            event.key == pygame.K_DOWN and directions[arr_index] == DOWN) or (
                            event.key == pygame.K_RIGHT and directions[arr_index] == RIGHT):
                        if ceil(0.85 * screen.get_size()[1]) - 40 <= y_pos <= ceil(0.85 * screen.get_size()[1]) + 40:
                            if ceil(0.85 * screen.get_size()[1]) - 10 <= y_pos <= ceil(
                                    0.85 * screen.get_size()[1]) + 10:
                                if not score_put:
                                    score += 10
                                    score_put = True
                                    arrow_state = 1
                                    show_good = False
                                    show_bad = False
                                    show_wrong = False
                                    show_perfect = True
                                    sequence_states[arr_index] = 1
                                    validsoundeffect_music.play(pygame.mixer.Sound(
                                        "Resources/resourcesendplanet/valid_se.mp3"), loops=0)
                            else:
                                if not score_put:
                                    score += 5
                                    score_put = True
                                    arrow_state = 1
                                    show_good = True
                                    show_bad = False
                                    show_wrong = False
                                    show_perfect = False
                                    sequence_states[arr_index] = 1
                                    validsoundeffect_music.play(pygame.mixer.Sound(
                                        "Resources/resourcesendplanet/valid_se.mp3"), loops=0)
                        else:
                            if not score_put:
                                score -= 1
                                score_put = True
                                arrow_state = 2
                                show_good = False
                                show_bad = True
                                show_wrong = False
                                show_perfect = False
                                dec_index = True
                                sequence_states[arr_index] = 2
                                errorsoundeffect_music.play(pygame.mixer.Sound(
                                    "Resources/resourcesendplanet/error_se.mp3"), loops=0)
                                pygame.event.post(pygame.event.Event(TIMES_UP))
                        if event.key == pygame.K_UP:
                            video = cv2.VideoCapture("Resources/resourcesendplanet/up.mp4")
                            fps = video.get(cv2.CAP_PROP_FPS)
                        elif event.key == pygame.K_RIGHT:
                            video = cv2.VideoCapture("Resources/resourcesendplanet/right.mp4")
                            fps = video.get(cv2.CAP_PROP_FPS)
                        elif event.key == pygame.K_DOWN:
                            video = cv2.VideoCapture("Resources/resourcesendplanet/down.mp4")
                            fps = video.get(cv2.CAP_PROP_FPS)
                        elif event.key == pygame.K_LEFT:
                            video = cv2.VideoCapture("Resources/resourcesendplanet/left.mp4")
                            fps = video.get(cv2.CAP_PROP_FPS)
                    else:
                        if not score_put:
                            score -= 2
                            score_put = True
                            arrow_state = 2
                            show_wrong = True
                            show_bad = False
                            show_good = False
                            show_perfect = False
                            dec_index = True
                            sequence_states[arr_index] = 2
                            errorsoundeffect_music.play(pygame.mixer.Sound("Resources/resourcesendplanet/error_se.mp3"),
                                                        loops=0)
                            pygame.event.post(pygame.event.Event(TIMES_UP))
        if running:
            draw_clock()
            # pygame.display.update()
            pygame.display.flip()
    pygame.quit()
