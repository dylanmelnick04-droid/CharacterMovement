import pygame
import math

class NewProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, PROJECTILE_TYPE):
        super().__init__()

        self.original_image = pygame.transform.scale(PROJECTILE_TYPE["image"], (28, 28))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))

        self.damage = PROJECTILE_TYPE["damage"]

        self.hasHit = False

        # Float position (IMPORTANT)
        self.pos = pygame.Vector2(x, y)
        self.image_offset = PROJECTILE_TYPE["image_offset"]

        self.speed = PROJECTILE_TYPE["speed"]
        upward_force = PROJECTILE_TYPE["upward_force"]
        gravity = 1000

        # Direction-based velocity
        if direction == 'Right':
            self.vel = pygame.Vector2(self.speed, upward_force)
        else:
            self.vel = pygame.Vector2(-self.speed, upward_force)

        self.gravity = gravity
    def update(self, dt):
        # Apply gravity
        self.vel.y += self.gravity * dt

        # Move projectile
        self.pos += self.vel * dt

        angle = math.degrees(math.atan2(-self.vel.y, self.vel.x))

        self.image = pygame.transform.rotate(self.original_image, angle-self.image_offset)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))