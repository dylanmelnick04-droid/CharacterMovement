import pygame

class GameOverStage:
    def __init__(self, winner):
        pygame.init()

        self.winner = winner

        self.WIDTH = 500
        self.HEIGHT = 500
        self.GRAY = (34, 34, 34)
        self.CREME = (255, 255, 220)
        self.BLACK = (0, 0, 0)

        self.game_over_font = pygame.font.SysFont('Veranda', 30)
        self.restart_font = pygame.font.SysFont('Veranda', 30)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game Over")
        
    
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
                
                if event.key == pygame.K_r:
                    return ("PICK_MAP", {"arena": True})

        self.screen.fill(self.CREME)

        text_surface = self.game_over_font.render("Player " + str(self.winner + 1) + " wins!", True, self.BLACK)
        self.screen.blit(text_surface, (190, 100))

        text_surface = self.restart_font.render("Press 'r' to restart.", True, self.GRAY)
        self.screen.blit(text_surface, (190, 150))
        text_surface = self.restart_font.render("Press 'q' to quit.", True, self.GRAY)
        self.screen.blit(text_surface, (190, 175))

        pygame.display.flip()
    
        return None