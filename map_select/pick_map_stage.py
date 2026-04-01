import pygame
import numpy as np
import map_select.revolvingQueue_utils
from gameplay.gameplay_stage import GamePlayStage

class PickMapStage:
    def __init__(self, arena, lives, player1_character, player2_character):
        pygame.init()

        self.arena = arena
        self.lives = lives
        self.player1_character = player1_character
        self.player2_character = player2_character

        self.WIDTH = 500
        self.HEIGHT = 500
        self.GRAY = (34, 34, 34)
        self.CREME = (255, 255, 220)
        self.BLACK = (0, 0, 0)
        self.SHEAR_X = 0.0
        self.SHEAR_Y = 0.1
        self.SCALE_INT = 150

        self.my_font = pygame.font.SysFont('Veranda', 30)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pick Arena")

        self.object_list = []
        self.scaled_sheared_list = []

        self.mostRecentDirection = -1

        self.load_assets()
        
    
    def load_assets(self):

        self.medieval_town_background_image = pygame.image.load('image_reference/stage_select/medieval_town_map.png').convert_alpha()
        self.arena_background_image = pygame.image.load('image_reference/stage_select/arena_map.png').convert_alpha()
        self.milk_map_background_image = pygame.image.load('image_reference/stage_select/milk_map.png').convert_alpha()
        self.space_map_background_image = pygame.image.load('image_reference/stage_select/space_map.png').convert_alpha()
        self.doodle_map_background_image = pygame.image.load('image_reference/background/doodle_map.png').convert_alpha()

        self.map_image_list = [
            {"name": "Town Hall", "idx": 0, "image": self.medieval_town_background_image},
            {"name": "Arena", "idx": 1, "image": self.arena_background_image},
            {"name": "Bowl of Milk", "idx": 2, "image": self.milk_map_background_image},
            {"name": "Starry Space", "idx": 3, "image": self.space_map_background_image},
            {"name": "Doodle", "idx": 4, "image": self.doodle_map_background_image}
        ]
        self.map_pointer_index = next(
            (i for i, m in enumerate(self.map_image_list) if m["name"] == "Bowl of Milk"),
            None
        )
        return


    def updateGameplay(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()
                
                if event.key == pygame.K_RIGHT:
                    map_select.revolvingQueue_utils.shift_right(self.map_image_list)
                    print("shift right")
                    self.map_pointer_index = self.map_pointer_index + 1
                    self.mostRecentDirection = -1
                if event.key == pygame.K_LEFT:
                    map_select.revolvingQueue_utils.shift_left(self.map_image_list)
                    self.map_pointer_index = self.map_pointer_index - 1
                    print("shift left")
                    self.mostRecentDirection = 0
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    print("select")
                    return ("GAMEPLAY", {
                        "player1_character": self.player1_character,
                        "player2_character": self.player2_character,
                        "MAP": self.map_image_list[self.map_pointer_index]["name"],
                        "arena": self.arena,
                        "lives": self.lives
                    })

        self.screen.fill(self.CREME)

        text_surface = self.my_font.render("Select a Map", True, (0, 0, 0))
        self.screen.blit(text_surface, (190, 100))
        
        map_select.revolvingQueue_utils.render_maps(self.screen, self.map_image_list, self.object_list, self.my_font, self.mostRecentDirection)

        pygame.display.flip()
    
        return None