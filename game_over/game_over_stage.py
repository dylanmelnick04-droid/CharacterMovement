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


    def updateGameplay(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()
                
                if event.key == pygame.K_r:
                    return ("BOOTSTRAP", {})

        self.screen.fill(self.CREME)

        text_surface = self.game_over_font.render("Player " + str(self.winner + 1) + " wins!", True, self.BLACK)
        self.screen.blit(text_surface, (190, 100))

        text_surface = self.restart_font.render("Press 'r' to restart.", True, self.GRAY)
        self.screen.blit(text_surface, (190, 150))
        text_surface = self.restart_font.render("Press 'q' to quit.", True, self.GRAY)
        self.screen.blit(text_surface, (190, 175))

        pygame.display.flip()
    
        return None