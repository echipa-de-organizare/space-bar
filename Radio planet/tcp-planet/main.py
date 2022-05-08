import os
import subprocess
import timeit
from math import ceil

import cv2
import pygame

from resources.utils import *
from tcp_client import *
from xml_handling import *

# initialize game window
pygame.init()
# screen = pygame.display.set_mode((1200, 800))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Radio tcp planet")
pygame.display.set_icon(pygame.image.load("resources/radio.png"))

# background space music
background_music = pygame.mixer.Channel(0)
radiosoundeffect_music = pygame.mixer.Channel(1)
background_music.play(pygame.mixer.Sound("resources/voyagespaceambientmusic.mp3"), loops=-1, fade_ms=5000)

# mixer.music.load("resources/voyagespaceambientmusic.mp3")
# mixer.music.play(-1)
# current_music_pos = pygame.mixer.music.get_pos()

global_seconds = 0
local_start = 0
local_end = 0
spacebarlogT = os.path.expanduser("~\\Documents\\spacebarlogT.txt")
spacebarlogP= os.path.expanduser("~\\Documents\\spacebarlogP.txt")


def read_seconds():
    global global_seconds
    # with open("../../Core/time_reset.txt", "r") as f:
    with open(spacebarlogT, "r") as f:
        global_seconds = int(f.readline().strip())


def write_seconds():
    global global_seconds, local_start, local_end
    new_seconds = global_seconds + local_end - local_start
    with open(spacebarlogT, "w") as f:
        f.truncate()
        f.write(str(int(new_seconds)))


def place_radio():
    radio = pygame.image.load("resources/radio.png")
    x, y = screen.get_size()
    '''
    460*100/1080=x ====> 42.59 under radio
    
    50*100/460=x =====> text padding 10.8695
    '''
    # print(ceil(0.4259259 * y))
    # print(x, y)
    radio = pygame.transform.scale(radio, (x, y))
    screen.blit(radio, (0, 0))


# # opencv2
x, y = screen.get_size()
video = cv2.VideoCapture("resources/radio.mp4")
fps = video.get(cv2.CAP_PROP_FPS)
clock = pygame.time.Clock()


def get_oid_by_index(option_ids, selected_index):
    return option_ids[selected_index - 1]


'''
both server and client can access xml file
client sends to server selected_index
server keeps count of current level
based on current level and selected index, gets id of next question
server sends back to client that id

client needs function to get question and options by ID OF THE QUESTION FROM XML
server needs to GET ID OF NEXT QUESTION BY GOING TO THE SELECTED OPTION OF THE CURRENT LEVEL AND GET NEXT Q 
1        2
q1
    -o1
        -q2
            -o1
            -o2
            -o3
    -o2
        -q3
            -o1
            -o2
            -o3
    -o3
        -q4
            -o1
            -o2
            -o3
'''
# under_radio = 460
# x, y = screen.get_size()
under_radio = ceil(0.4259259 * y)
upper_limit_options = ceil(0.4259259 * y)
text_padding = ceil(0.108695 * y)
# 460//2,3,4,5,6
# hardcoded_sizes = {5: 75, 4: 93, 3: 100, 2: 100, 1: 100}
# 100*100/460=x ======> 21.7391
hardcoded_sizes = {5: ceil(under_radio / 6), 4: ceil(under_radio / 5), 3: ceil(0.217391 * under_radio),
                   2: ceil(0.217391 * under_radio), 1: ceil(0.217391 * under_radio)}


def set_selected_index(nr_options):
    w, h = pygame.display.get_surface().get_size()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    global upper_limit_options
    listt = [h - upper_limit_options + hardcoded_sizes[nr_options] * i for i in range(nr_options + 1)]
    for i in range(len(listt) - 1):
        if listt[i] <= mouse_y <= listt[i + 1]:
            return i + 1
    return 0


def draw_option_text(text, nr_options):
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 30)
    text = font.render(text, True, (255, 255, 255))
    w, h = pygame.display.get_surface().get_size()
    # surf_height = text.get_size()[1]
    surf_height = hardcoded_sizes[nr_options]
    surface = pygame.Surface((w, surf_height))
    surface.fill(DARK2)
    surface.set_alpha(200)
    global under_radio
    screen.blit(surface, (0, h - under_radio))

    screen.blit(text, (50, h - under_radio + surf_height // 4))
    global upper_limit_options
    upper_limit_options = under_radio - surf_height


def draw_text(text, nr_options, index=1):
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 30)
    text = font.render(text, True, (255, 255, 255))
    w, h = pygame.display.get_surface().get_size()
    surface = pygame.Surface((w, hardcoded_sizes[nr_options]))
    surface.fill(DARK)
    surface.set_alpha(80)
    global upper_limit_options
    screen.blit(surface, (0, h - upper_limit_options + (index - 1) * hardcoded_sizes[nr_options]))
    screen.blit(text, (100, h - upper_limit_options + (index - 1) * hardcoded_sizes[nr_options] +
                       hardcoded_sizes[nr_options] // 4))


def draw_text_selected(text, nr_options, index=1):
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 30)
    text = font.render(text, True, (255, 255, 255))
    w, h = pygame.display.get_surface().get_size()
    # surface = pygame.Surface((w, text.get_size()[1] + 45))
    surface = pygame.Surface((w, hardcoded_sizes[nr_options]))
    surface.fill(DARK)
    surface.set_alpha(200)
    global upper_limit_options
    screen.blit(surface, (0, h - upper_limit_options + (index - 1) * hardcoded_sizes[nr_options]))
    screen.blit(text, (100, h - upper_limit_options + (index - 1) * hardcoded_sizes[nr_options] +
                       hardcoded_sizes[nr_options] // 4))


def template_options(nr_options, textq, *options, selected_index=0):
    screen.fill(DARK)
    place_radio()
    draw_option_text(textq, nr_options)
    if len(options) >= 1:
        if selected_index == 1:
            draw_text_selected(options[0], nr_options, index=1)
        else:
            draw_text(options[0], nr_options, index=1)
    if len(options) >= 2:
        if selected_index == 2:
            draw_text_selected(options[1], nr_options, index=2)
        else:
            draw_text(options[1], nr_options, index=2)
    if len(options) >= 3:
        if selected_index == 3:
            draw_text_selected(options[2], nr_options, index=3)
        else:
            draw_text(options[2], nr_options, index=3)
    if len(options) >= 4:
        if selected_index == 4:
            draw_text_selected(options[3], nr_options, index=4)
        else:
            draw_text(options[3], nr_options, index=4)
    if len(options) >= 5:
        if selected_index == 5:
            draw_text_selected(options[4], nr_options, index=5)
        else:
            draw_text(options[4], nr_options, index=5)


start_music = 0


def write_to_next_planet_file():
    with open(spacebarlogP, "w") as f:
        # f.truncate()
        f.write(str(1))


# Time Info
Time = 0
current_minute = 9
current_second = 7

counter = 0


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


if __name__ == '__main__':
    subprocess.Popen("../tcp-server/main.exe", creationflags=subprocess.DETACHED_PROCESS, close_fds=True)
    running = True
    selected_index = 0
    qid = 100
    question, options, option_ids = get_data_by_qid(qid)
    nr_options = len(options)
    # global global_seconds, local_start, local_end
    read_seconds()
    pygame.time.set_timer(pygame.USEREVENT, (300 - global_seconds) * 1000)

    Clock = pygame.time.Clock()
    CLOCKTICK = pygame.USEREVENT + 1
    pygame.time.set_timer(CLOCKTICK, 1000)
    set_clock(global_seconds)

    local_start = timeit.default_timer()
    while running:
        if qid != 0:
            # print(options)
            template_options(nr_options, question, *options, selected_index=selected_index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                selected_index = set_selected_index(nr_options)
            if event.type == CLOCKTICK:
                current_second = current_second + 1
                if current_second == 60:
                    current_second = 0
                    current_minute = current_minute + 1
            if event.type == pygame.USEREVENT:
                background_music.stop()
                radiosoundeffect_music.stop()
                write_to_next_planet_file()
                local_end = local_start - global_seconds
                write_seconds()
                pygame.quit()
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_CLICK:
                selected_index = set_selected_index(nr_options)
                indexes = (i for i in range(1, nr_options + 1))
                if selected_index in indexes:
                    video = cv2.VideoCapture("resources/radio.mp4")
                    fps = video.get(cv2.CAP_PROP_FPS)
                    clock = pygame.time.Clock()

                    success, video_image = video.read()
                    if success:
                        radiosoundeffect_music.play(pygame.mixer.Sound("resources/radiosoundeffectshorter.mp3"),
                                                    loops=0)
                        radiosoundeffect_music.set_volume(1.0)

                        video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
                        x, y = screen.get_size()
                        video_surf = pygame.transform.scale(video_surf, (x, y))
                        screen.blit(video_surf, (0, 0))

                    sock = create_connection()
                    oid = get_oid_by_index(option_ids, selected_index)
                    send_option_to_server(sock, oid)
                    qid = get_response_from_server(sock)
                    close_connection(sock)
                    if qid != 0:
                        question, options, option_ids = get_data_by_qid(qid)
                        nr_options = len(options)
                    else:
                        background_music.stop()
                        radiosoundeffect_music.stop()
                        write_to_next_planet_file()
                        local_end = timeit.default_timer()
                        write_seconds()
                        pygame.quit()
                        running = False
                        break
        if running:
            success, video_image = video.read()
            if success:
                video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
                x, y = screen.get_size()
                video_surf = pygame.transform.scale(video_surf, (x, y))
                screen.blit(video_surf, (0, 0))
            draw_clock()
            pygame.display.update()
    # pygame.quit()
