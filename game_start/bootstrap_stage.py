import pygame

class BootStrapStage:
    def __init__(self):
        pygame.init()

        self.arena = False
        self.lives = 3

        self.selectedIdx = 0

        self.WIDTH = 500
        self.HEIGHT = 500
        self.GRAY = (34, 34, 34)
        self.CREME = (255, 255, 220)
        self.BLACK = (0, 0, 0)

        self.welcome_font = pygame.font.SysFont('Veranda', 35)
        self.arena_message_font = pygame.font.SysFont('Veranda', 20)
        self.description_font = pygame.font.SysFont('Veranda', 15)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Welcome, Players!")


    def updateGameplay(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()
                
                if event.key == pygame.K_a:
                    self.arena = not self.arena
                
                if event.key == pygame.K_RIGHT:
                    self.lives = self.lives + 1

                if event.key == pygame.K_LEFT:
                    self.lives = self.lives - 1
                
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    return ("PICK_CHARACTERS", {"arena": self.arena, "lives": self.lives})

        self.draw()

    def draw(self):
        self.screen.fill(self.CREME)

        text_surface = self.welcome_font.render("Welcome to my game, Teeth and Nails!", True, self.GRAY)
        self.screen.blit(text_surface, (20, 100))

        text_surface = "This is my second game. I mostly write epic fantasy, but apps are coming soon.\nMy next game will be much more involved, with plot, character, and emotion.\n\nUntil then,\nD."
        lines = text_surface.split("\n")

        y = 150
        for line in lines:
            rendered = self.description_font.render(line, True, self.GRAY)
            self.screen.blit(rendered, (45, y))
            y += (rendered.get_height() + 5)

        text_surface = self.arena_message_font.render("Each character has " + str(self.lives) + " lives (use R_ARROW and L_ARROW to change).", True, self.GRAY)
        self.screen.blit(text_surface, (30, 400))

        if self.arena == True:
            text_surface = self.arena_message_font.render("Press 'a' to disable arena mode.", True, self.GRAY)
        else:
            text_surface = self.arena_message_font.render("Press 'a' to enable arena mode.", True, self.GRAY)
        self.screen.blit(text_surface, (30, 425))
        
        text_surface = self.arena_message_font.render("Press 'q' to quit.", True, self.GRAY)
        self.screen.blit(text_surface, (30, 450))

        text_surface = self.arena_message_font.render("Press 'enter' to proceed to character select.", True, self.GRAY)
        self.screen.blit(text_surface, (30, 475))

        pygame.display.flip()
    
        return None