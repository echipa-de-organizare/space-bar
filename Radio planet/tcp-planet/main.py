import multiprocessing
import os

import cv2
import pygame
from pygame import mixer

from resources.utils import *
from tcp_client import *
from xml_handling import *
import subprocess

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


def place_radio():
    radio = pygame.image.load("resources/radio.png")
    # radio = pygame.transform.scale(radio, (1200, 800))
    screen.blit(radio, (0, 0))


# # opencv2
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

upper_limit_options = 460
# 460//2,3,4,5,6
hardcoded_sizes = {5: 75, 4: 93, 3: 100, 2: 100, 1: 100}


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
    surf_height = text.get_size()[1] + 50
    surface = pygame.Surface((w, surf_height))
    surface.fill(DARK2)
    surface.set_alpha(200)
    screen.blit(surface, (0, h - 460))
    screen.blit(text, (50, h - 460 + surf_height // 4))
    global upper_limit_options
    upper_limit_options = 460 - surf_height


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
                       hardcoded_sizes[nr_options] // 3))


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
                       hardcoded_sizes[nr_options] // 3))


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
if __name__ == '__main__':
    subprocess.Popen("../tcp-server/main.exe", creationflags=subprocess.DETACHED_PROCESS, close_fds=True)
    running = True
    selected_index = 0
    qid = 100
    question, options, option_ids = get_data_by_qid(qid)
    nr_options = len(options)
    while running:
        if qid != 0:
            # print(options)
            template_options(nr_options, question, *options, selected_index=selected_index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            #     radio_animation()
            if event.type == pygame.MOUSEMOTION:
                selected_index = set_selected_index(nr_options)
            if event.type == pygame.USEREVENT:
                # mixer.music.load("resources/voyagespaceambientmusic.mp3")
                # mixer.music.play(-1, start_music)
                # pygame.mixer.music.set_pos(current_music_pos / 1000)
                background_music.unpause()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_CLICK:
                selected_index = set_selected_index(nr_options)
                indexes = (i for i in range(1, nr_options + 1))
                if selected_index in indexes:
                    video = cv2.VideoCapture("resources/radio.mp4")
                    fps = video.get(cv2.CAP_PROP_FPS)
                    clock = pygame.time.Clock()
                    success, video_image = video.read()
                    if success:
                        background_music.pause()
                        radiosoundeffect_music.play(pygame.mixer.Sound("resources/radiosoundeffectshorter.mp3"), loops=0,
                                                    fade_ms=5000)
                        radiosoundeffect_music.set_endevent(pygame.USEREVENT)

                        video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
                        screen.blit(video_surf, (0, 0))

                    sock = create_connection()
                    oid = get_oid_by_index(option_ids, selected_index)
                    send_option_to_server(sock, oid)
                    qid = get_response_from_server(sock)
                    close_connection(sock)
                    if qid != 0:
                        question, options, option_ids = get_data_by_qid(qid)
                        nr_options = len(options)
        success, video_image = video.read()
        if success:
            video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            screen.blit(video_surf, (0, 0))
        pygame.display.update()
    pygame.quit()
