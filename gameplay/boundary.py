import pygame

class Boundary(pygame.sprite.Sprite):
    def __init__(self, module_x, module_y, sheet_image):
        super().__init__()
        self.image = pygame.transform.scale(sheet_image,(25, 25))
        self.rect = self.image.get_rect()
        #self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = module_x
        self.rect.y = module_y