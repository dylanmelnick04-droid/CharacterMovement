import pygame
import numpy as np
import revolvingQueue_utils

pygame.init()

WIDTH = 500
HEIGHT = 500
GRAY = (34, 34, 34)
CREME = (255, 255, 220)
BLACK = (0, 0, 0)
SHEAR_X = 0.0
SHEAR_Y = 0.1

SCALE_INT = 150

my_font = pygame.font.SysFont('Veranda', 30)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pick Arena")

medieval_town_background_image = pygame.image.load('image_reference/stage_select/medieval_town_map.png').convert_alpha()
arena_background_image = pygame.image.load('image_reference/stage_select/arena_map.png').convert_alpha()
milk_map_background_image = pygame.image.load('image_reference/stage_select/milk_map.png').convert_alpha()
space_map_background_image = pygame.image.load('image_reference/stage_select/space_map.png').convert_alpha()
space_background_image = pygame.image.load('image_reference/background/space_background.jpg').convert_alpha()

object_list = []
scaled_sheared_list = []

#for i in range(5):

currentMap = 'map1'

#store maps and current positions. Shift left will subtract 1, shift right will add 1. Only 1-5 will be rendered
map_image_list = [
    {"name": "Town Hall", "idx": 0, "image": medieval_town_background_image},
    {"name": "Arena", "idx": 1, "image": arena_background_image},
    {"name": "Bowl of Milk", "idx": 2, "image": milk_map_background_image},
    {"name": "Starry Space", "idx": 3, "image": space_map_background_image},
    {"name": "map5", "idx": 4, "image": medieval_town_background_image}
]

mostRecentDirection = -1

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            
            if event.key == pygame.K_RIGHT:
                revolvingQueue_utils.shift_right(map_image_list)
                print("shift right")
                mostRecentDirection = -1
            if event.key == pygame.K_LEFT:
                revolvingQueue_utils.shift_left(map_image_list)
                print("shift left")
                mostRecentDirection = 0
    
    screen.fill(CREME)

    text_surface = my_font.render("Select a Map", True, (0, 0, 0))
    screen.blit(text_surface, (190, 100))
    
    revolvingQueue_utils.render_maps(screen, map_image_list, object_list, my_font, mostRecentDirection)

    pygame.display.flip()