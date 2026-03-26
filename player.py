import pygame

class NewPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y, walk_frames, controls, WIDTH, HEIGHT, projectileType):
        super().__init__()
        self.walk_frame = walk_frames
        self.walk_frame_index = 0
        self.image = self.walk_frame[self.walk_frame_index]
        #self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y-50
        self.velocity_x = 0
        self.velocity_y = 0
        self.isOnGround = True
        self.dash = False
        self.canDash = True
        self.mostRecentXDirection = 'Right'
        self.dashTime = 0
        self.dashDuration = 0.15
        self.dashSpeed = 800
        self.isOnEdgeOfScreen = False
        self.maxHealth = projectileType["health"]
        self.health = self.maxHealth
        self.crit_start_time = 0      # time when crit appears
        self.crit_duration = 0.5      # seconds
        self.displayCrit = False

        self.hasThrown = False
        self.hasMeleed = False

        self.projectiles = []
        self.projectileType = projectileType
        self.melee_damage = projectileType["character_melee_damage"]
        self.melee_cooldown = projectileType["melee_cooldown"]

        self.last_melee_time = 0

        self.controls = controls

        self.animation_timer = 0
        self.animation_speed = 0.1

        self.hitbox = self.rect.inflate(WIDTH * -0.06, HEIGHT * -0.02)
        self.hitbox.center = self.rect.center
        self.hitbox.centerx -= 1
        self.hitbox.centery += 1

        health_ratio = self.health / self.maxHealth

        self.healthbar = self.rect.inflate(WIDTH * 0.02, HEIGHT * -0.075)
        self.healthbar.center = self.rect.center
        self.healthbar.centerx -= 1
        self.healthbar.centery -= 30

        current_width = int(self.healthbar.width * health_ratio)
        current_bar = pygame.Rect(self.healthbar.x, self.healthbar.y, current_width, self.healthbar.height)

        self.lives = 3

        self.alive = True
        
    def update (self, dt, COLORKEY):
        self.animation_timer += dt
        self.hitbox.center = self.rect.center
        self.hitbox.centerx -= 1
        self.hitbox.centery += 1

        frame = self.walk_frame[self.walk_frame_index]
        if self.velocity_x == 0:
            frame = self.walk_frame[0]
        if self.dash:
            frame = self.walk_frame[7]
        elif self.animation_timer > self.animation_speed and self.velocity_x != 0:
            self.walk_frame_index = (self.walk_frame_index + 1) % (len (self.walk_frame) - 1)
            self.animation_timer = 0
            frame = self.walk_frame[self.walk_frame_index]

        if self.mostRecentXDirection == 'Left':
            frame = pygame.transform.flip(frame, True, False)
            
        self.image = frame
        self.image.set_colorkey(COLORKEY)
        return