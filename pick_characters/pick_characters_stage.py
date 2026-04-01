import pygame

class PickCharactersStage:
    def __init__(self, arena, lives):
        pygame.init()

        self.arena = arena
        self.lives = lives

        self.selectedIdx = 0

        self.WIDTH = 500
        self.HEIGHT = 500
        self.GRAY = (34, 34, 34)
        self.CREME = (255, 255, 220)
        self.BLACK = (0, 0, 0)

        self.game_over_font = pygame.font.SysFont('Veranda', 30)
        self.arena_message_font = pygame.font.SysFont('Veranda', 50)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Welcome, Players!")


    def updateGameplay(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()
                
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    return ("PICK_MAP", {"arena": self.arena, "lives": self.lives})

        self.draw()

    def draw(self):
        self.screen.fill(self.CREME)

        
        text_surface = self.arena_message_font.render("Pick characters", True, self.GRAY)
        self.screen.blit(text_surface, (190, 450))

        pygame.display.flip()
    
        return None