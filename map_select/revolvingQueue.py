import pygame
import numpy as np
import revolvingQueue_utils
from pick_map_stage import PickMapStage
from gameplay.gameplay_stage import GamePlayStage

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

medieval_town_background_image = pygame.image.load('image_reference/map_select/medieval_town_map.png').convert_alpha()
arena_background_image = pygame.image.load('image_reference/map_select/arena_map.png').convert_alpha()
milk_map_background_image = pygame.image.load('image_reference/map_select/milk_map.png').convert_alpha()
space_map_background_image = pygame.image.load('image_reference/map_select/space_map.png').convert_alpha()
space_background_image = pygame.image.load('image_reference/background/space_background.jpg').convert_alpha()

object_list = []
scaled_sheared_list = []

# store maps and current positions. Shift left will subtract 1, shift right will add 1. Only 1-5 will be rendered
map_image_list = [
    {"name": "Town Hall", "idx": 0, "image": medieval_town_background_image},
    {"name": "Arena", "idx": 1, "image": arena_background_image},
    {"name": "Bowl of Milk", "idx": 2, "image": milk_map_background_image},
    {"name": "Starry Space", "idx": 3, "image": space_map_background_image},
    {"name": "map5", "idx": 4, "image": medieval_town_background_image}
]

# track most recent direction for blit order
mostRecentDirection = -1
current_stage = PickMapStage()
running = True

while running:
    current_stage.updateGameplay()