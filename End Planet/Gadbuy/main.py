import os
import random
import subprocess
import time
import timeit
from math import ceil
from random import randint

import cv2
import pygame

# initialize game window
from Resources.resourcesgadbuy.utils import *

random.seed(time.time())
directions = [randint(0, 3) for _ in range(10)]
sequence_states = [0 for _ in range(10)]
# directions = [0 for i in range(20)]
icon_paths = ["Resources/resourcesgadbuy/up.png", "Resources/resourcesgadbuy/right.png", "Resources/resourcesgadbuy/down.png", "Resources/resourcesgadbuy/left.png"]
icon_active_paths = ["Resources/resourcesgadbuy/upactive.png", "Resources/resourcesgadbuy/rightactive.png", "Resources/resourcesgadbuy/downactive.png",
                     "Resources/resourcesgadbuy/leftactive.png"]
icon_good_paths = ["Resources/resourcesgadbuy/upgood.png", "Resources/resourcesgadbuy/rightgood.png", "Resources/resourcesgadbuy/downgood.png",
                   "Resources/resourcesgadbuy/leftgood.png"]
icon_bad_paths = ["Resources/resourcesgadbuy/upbad.png", "Resources/resourcesgadbuy/rightbad.png", "Resources/resourcesgadbuy/downbad.png", "Resources/resourcesgadbuy/leftbad.png"]

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("End planet")
pygame.display.set_icon(pygame.image.load("Resources/resourcesgadbuy/bg.png"))


def place_bg():
    radio = pygame.image.load("Resources/resourcesgadbuy/bg.png")
    x, y = screen.get_size()
    radio = pygame.transform.scale(radio, (x, y))
    return screen.blit(radio, (0, 0))


def place_gadbuy():
    gadbuy = pygame.image.load("Resources/resourcesgadbuy/Gadbuy2.png")
    imgx, imgy = gadbuy.get_size()
    gadbuy = pygame.transform.scale(gadbuy, (ceil(0.55 * imgx), ceil(0.55 * imgy)))
    return screen.blit(gadbuy, (ceil(0.28 * x), ceil(0.2 * y)))


spacebarlogT = os.path.expanduser("~\\Documents\\spacebarlogT.txt")
spacebarlogP = os.path.expanduser("~\\Documents\\spacebarlogP.txt")
spacebarlogS = os.path.expanduser("~\\Documents\\spacebarlogS.txt")
spacebarlogL = os.path.expanduser("~\\Documents\\spacebarlogL.txt")
global_seconds = 0
local_start = 0
local_end = 0


def write_to_next_planet_file(planet=1):
    with open(spacebarlogP, "w") as f:
        f.write(str(planet))


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
    # font = pygame.font.SysFont("Trebuchet MS", 25)
    font = pygame.font.SysFont("Helvetica", 30)
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
gadbuy_text = ["Hey! What are you doing on my ship?",
               "Stop me from what?",
               "Right, that. Well, I don't have time to fight you, I'm late to a evils anonymous meeting.",
               "Not really. Let's play russian roulette. If you survive, I'll let you figure out on your own how to stop it."]
my_text = ["I'm here to stop you!",
           "You know, the time mechanism...",
           "So, you're just going to let me turn it off that easy?",
           "Fine."]
x, y = pygame.display.get_surface().get_size()
start_q_y = 220
start_o_y = 120


def set_selected_index():
    w, h = pygame.display.get_surface().get_size()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    global start_o_y
    if h - start_o_y <= mouse_y <= h:
        return 1
    return 0


def draw_option_text(text):
    pygame.font.init()
    font = pygame.font.SysFont("Verdana", 28)
    text = font.render(text, True, (255, 255, 255))
    w, h = pygame.display.get_surface().get_size()
    surf_height = 100
    surface = pygame.Surface((w, surf_height))
    surface.fill(DARK2)
    surface.set_alpha(200)
    global start_q_y
    screen.blit(surface, (0, h - start_q_y))
    screen.blit(text, (50, h - start_q_y + surf_height // 3))


def draw_text(text):
    pygame.font.init()
    font = pygame.font.SysFont("Verdana", 28)
    text = font.render(text, True, (255, 255, 255))
    w, h = pygame.display.get_surface().get_size()
    surf_height = 100
    surface = pygame.Surface((w, surf_height))
    surface.fill(DARK)
    surface.set_alpha(80)
    global start_o_y
    screen.blit(surface, (0, h - start_o_y))
    screen.blit(text, (100, h - start_o_y + surf_height // 3))


def draw_text_selected(text):
    pygame.font.init()
    font = pygame.font.SysFont("Verdana", 28)
    text = font.render(text, True, (255, 255, 255))
    w, h = pygame.display.get_surface().get_size()
    surf_height = 100
    surface = pygame.Surface((w, surf_height))
    surface.fill(DARK)
    surface.set_alpha(200)
    global start_o_y
    screen.blit(surface, (0, h - start_o_y))
    screen.blit(text, (100, h - start_o_y + surf_height // 3))


def place_roulette_img():
    revolver = pygame.image.load("Resources/resourcesgadbuy/revolver.png")
    x, y = screen.get_size()
    imgx, imgy = revolver.get_size()
    revolver = pygame.transform.scale(revolver, (ceil(0.35 * imgx), ceil(0.35 * imgy)))
    return screen.blit(revolver, (ceil(0.33 * x), y - 250))


start_button_x = ceil(0.57 * x)
start_button_y = 150


def set_selected_button():
    w, h = pygame.display.get_surface().get_size()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    global start_button_y, start_button_x
    if h - start_button_y <= mouse_y <= h - start_button_y + 80 and w - start_button_x <= mouse_x <= w - start_button_x + 200:
        return 1
    return 0


def place_button():
    pygame.font.init()
    font = pygame.font.SysFont("Candara", 30, bold=True)
    text = font.render("Try your luck", True, (255, 255, 255))
    w, h = pygame.display.get_surface().get_size()
    surf_height = 80
    surface = pygame.Surface((200, surf_height))
    surface.fill((80, 0, 0))
    surface.set_alpha(200)
    global start_button_y, start_button_x
    screen.blit(surface, (w - start_button_x, h - start_button_y))
    screen.blit(text, (20 + w - start_button_x, h - start_button_y + surf_height // 3))


def place_button_selected():
    pygame.font.init()
    font = pygame.font.SysFont("Candara", 30, bold=True)
    text = font.render("Try your luck", True, (255, 255, 255))
    w, h = pygame.display.get_surface().get_size()
    surf_height = 80
    surface = pygame.Surface((200, surf_height))
    surface.fill((80, 0, 0))
    surface.set_alpha(240)
    global start_button_y, start_button_x
    screen.blit(surface, (w - start_button_x, h - start_button_y))
    screen.blit(text, (20 + w - start_button_x, h - start_button_y + surf_height // 3))


text_placement = (ceil(0.48 * screen.get_width()), ceil(0.14 * screen.get_height()))


def place_died_text():
    pygame.font.init()
    font = pygame.font.SysFont("Candara", 40, bold=True)
    text = font.render("You died!", True, (255, 255, 255))
    x, y = screen.get_size()
    textRect = text.get_rect()
    textRect.center = text_placement
    screen.blit(text, textRect)


def place_lucky_text():
    pygame.font.init()
    font = pygame.font.SysFont("Candara", 40, bold=True)
    text = font.render("You survived! I guess you can try to turn off my machine now.", True, (255, 255, 255))
    x, y = screen.get_size()
    textRect = text.get_rect()
    textRect.center = text_placement
    screen.blit(text, textRect)


# background space music
background_music = pygame.mixer.Channel(0)
revolverload_soundeffect = pygame.mixer.Channel(1)
revolvercock_soundeffect = pygame.mixer.Channel(2)
emptyshot_soundeffect = pygame.mixer.Channel(3)
shot_soundeffect = pygame.mixer.Channel(4)
background_music.play(pygame.mixer.Sound("Resources/resourcesgadbuy/bgmusic.mp3"), loops=-1, fade_ms=5000)

if __name__ == '__main__':
    running = True
    read_seconds()
    TIMES_UP = pygame.USEREVENT
    pygame.time.set_timer(TIMES_UP, (300 - global_seconds) * 1000)

    Clock = pygame.time.Clock()
    CLOCKTICK = pygame.USEREVENT + 1
    pygame.time.set_timer(CLOCKTICK, 1000)
    set_clock(global_seconds)

    WON = pygame.USEREVENT + 2
    FINISHED_GOOD = pygame.USEREVENT + 3
    FINISHED_BAD = pygame.USEREVENT + 4

    local_start = timeit.default_timer()
    text_index = 0
    selected_index = 0
    play_roulette = False
    button_selected = 0
    died, lucky = False, False
    while running:
        place_bg()
        place_gadbuy()
        if not play_roulette:
            draw_option_text(gadbuy_text[text_index])
            if selected_index == 1:
                draw_text_selected(my_text[text_index])
            else:
                draw_text(my_text[text_index])
        else:
            place_roulette_img()
            if button_selected == 1:
                place_button_selected()
            else:
                place_button()
        if died:
            place_died_text()
        if lucky:
            place_lucky_text()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == CLOCKTICK:
                current_second = current_second + 1
                if current_second == 60:
                    current_second = 0
                    current_minute = current_minute + 1
            if event.type == TIMES_UP:
                background_music.stop()
                write_to_next_planet_file()
                local_end = local_start - global_seconds
                write_seconds()
                write_state(2)
                write_location()
                pygame.quit()
                running = False
                break
            if event.type == pygame.MOUSEMOTION:
                selected_index = set_selected_index()
                button_selected = set_selected_button()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_CLICK:
                selected_index = set_selected_index()
                button_selected = set_selected_button()
                if selected_index == 1:
                    if text_index + 1 != len(gadbuy_text):
                        text_index += 1
                    else:
                        pygame.time.delay(500)
                        play_roulette = True
                if button_selected == 1:
                    revolverload_soundeffect.play(pygame.mixer.Sound("Resources/resourcesgadbuy/revolverload.mp3"), loops=0)
                    pygame.time.delay(3500)
                    # if not revolverload_soundeffect.get_busy():
                    revolvercock_soundeffect.play(pygame.mixer.Sound("Resources/resourcesgadbuy/revolvercock.mp3"), loops=0)
                    revolvercock_soundeffect.set_volume(1.0)
                    pygame.time.delay(2000)
                    random.seed(time.time())
                    nr = random.randint(1, 6)
                    if nr == 1:
                        died = True
                        pygame.event.post(pygame.event.Event(FINISHED_BAD))
                    else:
                        lucky = True
                        pygame.event.post(pygame.event.Event(FINISHED_GOOD))
            if event.type == FINISHED_BAD:
                place_bg()
                place_gadbuy()
                shot_soundeffect.play(pygame.mixer.Sound("Resources/resourcesgadbuy/shot.mp3"), loops=0)
                place_died_text()
                pygame.display.flip()
                pygame.time.delay(2000)
                background_music.stop()
                revolverload_soundeffect.stop()
                revolvercock_soundeffect.stop()
                shot_soundeffect.stop()
                write_to_next_planet_file()
                local_end = local_start - global_seconds
                write_seconds()
                write_state(2)
                write_location()
                pygame.quit()
                running = False
                break
            if event.type == FINISHED_GOOD:
                place_bg()
                place_gadbuy()
                emptyshot_soundeffect.play(pygame.mixer.Sound("Resources/resourcesgadbuy/emptyshot.wav"), loops=0)
                place_lucky_text()
                pygame.display.flip()
                pygame.time.delay(4000)
                background_music.stop()
                revolverload_soundeffect.stop()
                revolvercock_soundeffect.stop()
                emptyshot_soundeffect.stop()
                write_to_next_planet_file(planet=4)
                local_end = timeit.default_timer() - 8
                write_seconds()
                write_state(1)
                write_location()
                pygame.quit()
                running = False
                break
        if running:
            draw_clock()
            # pygame.display.update()
            pygame.display.flip()
    pygame.quit()
