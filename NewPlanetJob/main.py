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
    line = pygame.transform.scale(line, (ceil(0.01 * line.get_size()[0]), mousey))
    return screen.blit(line, (ceil(0.4569 * x), (ceil(0.05 * y))))


def place_bait(mousex, mousey):
    bait = pygame.image.load("Resources/resourcesnewplanetjob/bait.png")
    x, y = screen.get_size()
    bait = pygame.transform.scale(bait, (ceil(0.7 * bait.get_size()[0]), ceil(0.7 * bait.get_size()[1])))
    return screen.blit(bait, (ceil(0.43 * x), mousey))


fish_lr_paths = ["Resources/resourcesnewplanetjob/fishlr1.png"]
fish_rl_paths = ["Resources/resourcesnewplanetjob/fishrl1.png"]
obstacle_paths = ["Resources/resourcesnewplanetjob/papuc.png"]


def place_fish_on_rod(mousex, mousey):
    caught = pygame.image.load("Resources/resourcesnewplanetjob/caught.png")
    x, y = screen.get_size()
    caught = pygame.transform.scale(caught, (ceil(0.7 * caught.get_size()[0]), ceil(0.7 * caught.get_size()[1])))
    return screen.blit(caught, (ceil(0.4165 * x), mousey + 80))


def place_obstacle(x_pos, y_pos):
    obstacle = pygame.image.load(random.choice(obstacle_paths))
    x, y = screen.get_size()
    obstacle = pygame.transform.scale(obstacle,
                                      (ceil(0.9 * obstacle.get_size()[0]), ceil(0.9 * obstacle.get_size()[1])))
    screen.blit(obstacle, (x_pos, y_pos))
    return obstacle, (x_pos, y_pos)


def place_fish_lr(x_pos, y_pos):
    fish = pygame.image.load(random.choice(fish_lr_paths))
    x, y = screen.get_size()
    fish = pygame.transform.scale(fish, (ceil(0.9 * fish.get_size()[0]), ceil(0.9 * fish.get_size()[1])))
    screen.blit(fish, (x_pos, y_pos))
    return fish, (x_pos, y_pos)


def place_fish_rl(x_pos, y_pos):
    fish = pygame.image.load(random.choice(fish_rl_paths))
    x, y = screen.get_size()
    fish = pygame.transform.scale(fish, (ceil(0.8 * fish.get_size()[0]), ceil(0.8 * fish.get_size()[1])))
    screen.blit(fish, (x_pos, y_pos))
    return fish, (x_pos, y_pos)


fish_list = []
obstacle_list = []


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
spacebarlogDLCL = os.path.expanduser("~\\Documents\\spacebarlogDLCL.txt")


def write_to_next_planet_file():
    with open(spacebarlogP, "w") as f:
        f.write(str(1))
    content = ""
    last_val = ""
    with open(spacebarlogDLCL, "r") as f:
        for line in f:
            if last_val == "WARPER\n":
                content += "1\n"
            else:
                content += line
            last_val = line
    with open(spacebarlogDLCL, "w") as f:
        f.write(content)


def write_state(state):
    with open(spacebarlogS, "w") as f:
        f.truncate()
        f.write(str(state))


def write_location():
    with open(spacebarlogL, "w") as f:
        f.truncate()
        f.write("0\n0")


cash = 0


def gimme_my_cash():
    pygame.font.init()
    font = pygame.font.SysFont("Candara", 30, bold=True)
    cash_text = font.render("Cash: " + str(cash) + "/420", True, BLACK)
    placement = (100, 100)
    screen.blit(cash_text, placement)


def place_earned_enough():
    x, y = screen.get_size()
    surface = pygame.Surface((x, y))
    surface.fill(BLACK)
    surface.set_alpha(200)
    screen.blit(surface, (0, 0))

    surface = pygame.Surface((ceil(0.5 * x), ceil(0.5 * y)))
    surface.fill(WHITE)
    surface.set_alpha(250)
    screen.blit(surface, (ceil(0.25 * x), ceil(0.25 * y)))

    pygame.font.init()
    font = pygame.font.SysFont("Candara", 50, bold=True)
    final_text = font.render("You have earned enough money.", True, BLACK)
    text_rect = final_text.get_rect(center=(x / 2, ceil(0.37 * y)))
    screen.blit(final_text, text_rect)

    final_text = font.render("You can now go back.", True, BLACK)
    text_rect = final_text.get_rect(center=(x / 2, ceil(0.47 * y)))
    screen.blit(final_text, text_rect)

    final_text = font.render("Congrats!", True, BLACK)
    text_rect = final_text.get_rect(center=(x / 2, ceil(0.57 * y)))
    screen.blit(final_text, text_rect)


def place_intro():
    x, y = screen.get_size()
    surface = pygame.Surface((x, y))
    surface.fill(BLACK)
    surface.set_alpha(200)
    screen.blit(surface, (0, 0))

    surface = pygame.Surface((ceil(0.5 * x), ceil(0.5 * y)))
    surface.fill(WHITE)
    surface.set_alpha(250)
    screen.blit(surface, (ceil(0.25 * x), ceil(0.25 * y)))

    pygame.font.init()
    font = pygame.font.SysFont("Candara", 50, bold=True)
    final_text = font.render("You warped to a new dimension", True, BLACK)
    text_rect = final_text.get_rect(center=(x / 2, ceil(0.37 * y)))
    screen.blit(final_text, text_rect)

    final_text = font.render("and you have no more fuel.", True, BLACK)
    text_rect = final_text.get_rect(center=(x / 2, ceil(0.47 * y)))
    screen.blit(final_text, text_rect)

    final_text = font.render("You need money for fuel, ", True, BLACK)
    text_rect = final_text.get_rect(center=(x / 2, ceil(0.57 * y)))
    screen.blit(final_text, text_rect)

    final_text = font.render("so work for it!", True, BLACK)
    text_rect = final_text.get_rect(center=(x / 2, ceil(0.67 * y)))
    screen.blit(final_text, text_rect)


# background space music
background_music = pygame.mixer.Channel(0)
background_music.play(pygame.mixer.Sound("Resources/resourcesnewplanetjob/bgmusic.mp3"), loops=-1, fade_ms=5000)

# # opencv2
x, y = screen.get_size()
video = cv2.VideoCapture("")
fps = video.get(cv2.CAP_PROP_FPS)
clock = pygame.time.Clock()
video_size = (ceil(0.5 * x), ceil(0.5 * y))
video_placement = (ceil(0.24 * x), ceil(0.15 * y))

caught = False


def check_fish_caught(mousex, mousey):
    x, y = screen.get_size()
    global fish_list, caught, cash
    i = 0
    while i < len(fish_list):
        fish, coords = fish_list[i][1]
        if not caught and ceil(0.43 * x) - 60 <= coords[0] <= ceil(0.43 * x) + 60 and mousey - 60 <= coords[
            1] <= mousey + 60:
            # if abs(coords[0] - ceil(0.43 * x)) <= 250 and abs(coords[1] - mousey) <= 250:
            del fish_list[i]
            i -= 1
            caught = True
        i += 1


def check_caught_fish_up(mousex, mousey):
    global cash, caught
    if caught and mousey <= 60:
        caught = False
        cash += 35


def place_all_obstacles():
    global obstacle_list
    i = 0
    while i < len(obstacle_list):
        state = obstacle_list[i][0]
        if state == 0:
            coords_copy = (obstacle_list[i][1][1][0] + 28, obstacle_list[i][1][1][1])
            obstacle, coords = obstacle_list[i][1]
            screen.blit(obstacle, coords)
            del obstacle_list[i]
            x, y = screen.get_size()
            if coords_copy[0] <= x + 200:
                obstacle_list.insert(i, (state, (obstacle, coords_copy)))
            else:
                i -= 1
        else:
            coords_copy = (obstacle_list[i][1][1][0] - 28, obstacle_list[i][1][1][1])
            obstacle, coords = obstacle_list[i][1]
            screen.blit(obstacle, coords)
            del obstacle_list[i]
            if coords_copy[0] > -200:
                obstacle_list.insert(i, (state, (obstacle, coords_copy)))
            else:
                i -= 1
        i += 1


def check_obstacle_hitting(mousex, mousey):
    global obstacle_list, caught
    if caught:
        x, y = screen.get_size()
        i = 0
        while i < len(obstacle_list):
            obstacle, coords = obstacle_list[i][1]
            if ceil(0.43 * x) - 80 <= coords[0] <= ceil(0.43 * x) + 80 and mousey - 80 <= coords[1] <= mousey + 80:
                del obstacle_list[i]
                i -= 1
                caught = False
            i += 1


won = False
if __name__ == '__main__':
    running = True

    WON = pygame.USEREVENT + 3

    PLACE_FISH = pygame.USEREVENT + 4
    CHECK_CAUGHT = pygame.USEREVENT + 5

    pygame.time.set_timer(CHECK_CAUGHT, 100)
    pygame.time.set_timer(PLACE_FISH, 1500)

    local_start = timeit.default_timer()
    mousex, mousey = 0, 0
    run_intro = True
    while running:
        random.seed(time.time())
        place_bg()
        place_line(mousex, mousey)
        place_bait(mousex, mousey)

        if caught:
            place_fish_on_rod(mousex, mousey)
        place_all_fish()
        place_all_obstacles()
        gimme_my_cash()
        if run_intro:
            place_intro()
            pygame.display.flip()
            time.sleep(5)
            run_intro = False
        if won:
            place_earned_enough()
            pygame.display.flip()
            time.sleep(5)
            background_music.stop()
            write_to_next_planet_file()
            # write_state(3)
            # pygame.quit()
            running = False
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = pygame.mouse.get_pos()
                check_fish_caught(mousex, mousey)
                check_obstacle_hitting(mousex, mousey)
            if event.type == CHECK_CAUGHT:
                mousex, mousey = pygame.mouse.get_pos()
                check_fish_caught(mousex, mousey)
                check_caught_fish_up(mousex, mousey)
                check_obstacle_hitting(mousex, mousey)
                if cash >= 420:
                    won = True
            if event.type == PLACE_FISH:
                x, y = screen.get_size()
                r = random.random()
                if r < 0.30:
                    fish_list.append((0, place_fish_lr(-200, random.randint(ceil(0.2 * y), ceil(0.9 * y)))))
                elif r < 0.60:
                    fish_list.append((1, place_fish_rl(x + 200, random.randint(ceil(0.2 * y), ceil(0.9 * y)))))
                elif r < 0.80:
                    obstacle_list.append((0, place_obstacle(-200, random.randint(ceil(0.2 * y), ceil(0.9 * y)))))
                else:
                    obstacle_list.append((1, place_obstacle(x + 200, random.randint(ceil(0.2 * y), ceil(0.9 * y)))))
            if event.type == pygame.KEYDOWN:
                pass
        if running:
            pygame.display.flip()
    pygame.quit()
