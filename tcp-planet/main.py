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
# mixer.music.load("resources/bg.mp3")
# mixer.music.play(-1)


def place_radio():
    radio = pygame.image.load("resources/radio.png")
    # radio = pygame.transform.scale(radio, (1200, 800))
    screen.blit(radio, (0, 0))


# # opencv2
video = cv2.VideoCapture("resources/radio.mp4")
fps = video.get(cv2.CAP_PROP_FPS)
clock = pygame.time.Clock()


#
#
# def radio_animation():
#     global fps
#     global clock
#     video = cv2.VideoCapture("resources/radio.mp4")
#     fps = video.get(cv2.CAP_PROP_FPS)
#     clock = pygame.time.Clock()
#     success, video_image = video.read()
#     if success:
#         video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
#         screen.blit(video_surf, (0, 0))
#     # video = moviepy.editor.VideoFileClip("resources/radio.mp4")
#     # video.preview()


def draw_option_text(text):
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 30)
    text = font.render(text, True, (255, 255, 255))
    w, h = pygame.display.get_surface().get_size()
    surface = pygame.Surface((w, text.get_size()[1] + 50))
    surface.fill(DARK2)
    surface.set_alpha(200)
    screen.blit(surface, (0, h - 350))
    screen.blit(text, (50, h - 350 + 20))


def draw_text(text, index=1):
    index = 4 - index
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 30)
    text = font.render(text, True, (255, 255, 255))
    w, h = pygame.display.get_surface().get_size()
    surface = pygame.Surface((w, text.get_size()[1] + 45))
    surface.fill(DARK)
    surface.set_alpha(80)
    screen.blit(surface, (0, h - 20 - 80 * index))
    screen.blit(text, (100, h - 20 - 80 * index + 20))


def draw_text_selected(text, index=1):
    index = 4 - index
    pygame.font.init()
    font = pygame.font.SysFont("Helvetica", 30)
    text = font.render(text, True, (255, 255, 255))
    w, h = pygame.display.get_surface().get_size()
    surface = pygame.Surface((w, text.get_size()[1] + 45))
    surface.fill(DARK)
    surface.set_alpha(200)
    screen.blit(surface, (0, h - 20 - 80 * index))
    screen.blit(text, (100, h - 20 - 80 * index + 20))


def set_selected_index():
    w, h = pygame.display.get_surface().get_size()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if h - 20 - 80 * 3 <= mouse_y <= h - 20 - 80 * 2:
        return 1
    elif h - 20 - 80 * 2 <= mouse_y <= h - 20 - 80 * 1:
        return 2
    elif h - 20 - 80 * 1 <= mouse_y <= h - 20 - 80 * 0:
        return 3
    return 0


def template_3_options(textq, text1, text2, text3, selected_index=0):
    screen.fill(DARK)
    place_radio()
    draw_option_text(textq)
    if selected_index == 1:
        draw_text_selected(text1, index=1)
    else:
        draw_text(text1, index=1)
    if selected_index == 2:
        draw_text_selected(text2, index=2)
    else:
        draw_text(text2, index=2)
    if selected_index == 3:
        draw_text_selected(text3, index=3)
    else:
        draw_text(text3, index=3)


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


def get_oid_by_index(option_ids, selected_index):
    return option_ids[selected_index - 1]


if __name__ == '__main__':

    running = True
    selected_index = 0
    qid = 1
    question, options, option_ids = get_data_by_qid(qid)
    while running:
        # clock.tick(fps)
        # template_3_options("The quick brown fox jumps over the lazy dog", "Option 1", "Option 2", "Option 3",
        #                    selected_index)

        if qid != 0:
            template_3_options(question, *options, selected_index)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            #     radio_animation()
            if event.type == pygame.MOUSEMOTION:
                selected_index = set_selected_index()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_CLICK:
                selected_index = set_selected_index()
                if selected_index in (1, 2, 3):
                    video = cv2.VideoCapture("resources/radio.mp4")
                    fps = video.get(cv2.CAP_PROP_FPS)
                    clock = pygame.time.Clock()
                    success, video_image = video.read()
                    if success:
                        video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
                        screen.blit(video_surf, (0, 0))

                    sock = create_connection()
                    oid = get_oid_by_index(option_ids, selected_index)
                    send_option_to_server(sock, oid)
                    qid = get_response_from_server(sock)
                    close_connection(sock)
                    if qid != 0:
                        question, options, option_ids = get_data_by_qid(qid)
        success, video_image = video.read()
        if success:
            video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            screen.blit(video_surf, (0, 0))
        pygame.display.update()
    pygame.quit()
