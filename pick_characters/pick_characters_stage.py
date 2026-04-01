import pygame

class PickCharactersStage:
    def __init__(self, arena, lives):
        pygame.init()

        self.arena = arena
        self.lives = lives

        self.playerOneIndex = 0
        self.playerTwoIndex = 0

        self.playerOptions = ['fireball', 'throwing_knife', 'thor', 'name_of_the_wind']

        self.WIDTH = 500
        self.HEIGHT = 500
        self.GRAY = (34, 34, 34)
        self.CREME = (255, 255, 220)
        self.BLACK = (0, 0, 0)

        self.arena_message_font = pygame.font.SysFont('Veranda', 50)
        self.player_font = pygame.font.SysFont('Veranda', 30)

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
                    print(self.playerOptions[self.playerOneIndex])
                    print(self.playerOptions[self.playerTwoIndex])
                    return ("PICK_MAP", {"arena": self.arena, "lives": self.lives, "player1_character": self.playerOptions[self.playerOneIndex], "player2_character": self.playerOptions[self.playerTwoIndex]})
                if event.key == pygame.K_UP:
                    self.playerTwoIndex = (self.playerTwoIndex + 1) % 4
                if event.key == pygame.K_DOWN:
                    if self.playerTwoIndex == 0:
                        self.playerTwoIndex = 3
                    else:
                        self.playerTwoIndex -= 1
                if event.key == pygame.K_w:
                    self.playerOneIndex = (self.playerOneIndex + 1) % 4
                if event.key == pygame.K_s:
                    if self.playerOneIndex == 0:
                        self.playerOneIndex = 3
                    else:
                        self.playerOneIndex -= 1

        self.draw()

    def draw(self):
        self.screen.fill(self.CREME)

        
        text_surface = self.arena_message_font.render("Pick characters", True, self.GRAY)
        self.screen.blit(text_surface, (120, 100))

        text_surface = self.player_font.render("Player 1 character: " + self.playerOptions[self.playerOneIndex], True, self.GRAY)
        self.screen.blit(text_surface, (120, 250))
        text_surface = self.player_font.render("Player 2 character: " + self.playerOptions[self.playerTwoIndex], True, self.GRAY)
        self.screen.blit(text_surface, (120, 300))

        pygame.display.flip()
    
        return None