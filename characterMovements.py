import pygame

pygame.init()

devtools = 'on'
# Constants
WIDTH, HEIGHT = 500, 500
WHITE = (255, 255, 255)
GRAY = (34, 34, 34)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Mechanics")

clock = pygame.time.Clock()
sprite_sheet_image = pygame.image.load('character.png').convert_alpha()
brick_sheet_image = pygame.image.load('square_brick.jpg').convert_alpha()

GRAVITY = 1500
ACCELERATION = 1500
DASH_ACCELERATION = 3000
FRICTION = 1200
MAX_SPEED = 400
MAX_DASH_SPEED = 700
JUMP_STRENGTH = -450
GROUND_Y = 450
BLACK = (0, 0, 0)

PLAYER_LEFT_LIMIT = 100
PLAYER_RIGHT_LIMIT = 376

def getImage(sheet, frame, width, height, scale, color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (frame*width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image


walk_frames = [
    getImage(sprite_sheet_image, 0, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 5, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 6, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 7, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 8, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 9, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 10, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 23, 24, 24, 2, BLACK)
]


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walk_frame = walk_frames
        self.walk_frame_index = 0
        self.image = self.walk_frame[self.walk_frame_index]
        #self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = 245
        self.rect.y = GROUND_Y
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

        self.animation_timer = 0
        self.animation_speed = 0.1

        self.hitbox = self.rect.inflate(WIDTH * -0.06, HEIGHT * -0.02)
        self.hitbox.center = self.rect.center
        self.hitbox.centerx -= 1
        self.hitbox.centery += 1

    def update (self, dt):
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
        self.image.set_colorkey(BLACK)
        return

class Boundary(pygame.sprite.Sprite):
    def __init__(self, module_x, module_y):
        super().__init__()
        self.image = pygame.transform.scale(brick_sheet_image,(50, 50))
        self.rect = self.image.get_rect()
        #self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = module_x
        self.rect.y = module_y
    def update(self, x_offset):
        self.rect.x -= x_offset

boundary_list = []
for i in range(10):
    boundary = Boundary(-250 + 50 * i, 50 * i)
    boundary_list.append(boundary)

for i in range(5):
    boundary = Boundary(500 - (50 * i), 250 + 50 * i)
    boundary_list.append(boundary)

player = Player()
x_offset = 0
running = True

while running:
    dt = clock.tick(60) / 1000  # seconds per frame
    player.update(dt)
    x_offset = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            if event.key == pygame.K_UP and player.isOnGround:
                player.velocity_y = JUMP_STRENGTH
                player.isOnGround = False
                player.canDash = True
            
            if event.key == pygame.K_d and not player.isOnGround and player.canDash:
                player.dash = True
                player.dashTime = player.dashDuration
                player.canDash = False
                if player.mostRecentXDirection == 'Right':
                    player.velocity_x = player.dashSpeed
                if player.mostRecentXDirection == 'Left':
                    player.velocity_x = -player.dashSpeed
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.velocity_x -= ACCELERATION * dt
        player.mostRecentXDirection = 'Left'

    if keys[pygame.K_RIGHT]:
        player.velocity_x += ACCELERATION * dt
        player.mostRecentXDirection = 'Right'

    if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]: # friction
        if player.velocity_x > 0:
            player.velocity_x -= FRICTION * dt
            if player.velocity_x < 0:
                player.velocity_x = 0
        elif player.velocity_x < 0:
            player.velocity_x += FRICTION * dt
            if player.velocity_x > 0:
                player.velocity_x = 0
    if player.dash:
        player.dashTime -= dt
        #player.velocity_y = 0

        if player.dashTime <= 0:
            player.dash = False
    # clamp horizontal speed
    if not player.dash:
        player.velocity_x = max(-MAX_SPEED, min(MAX_SPEED, player.velocity_x))
    if player.dash:
        player.velocity_x = max(-MAX_DASH_SPEED, min(MAX_DASH_SPEED, player.velocity_x))

    # apply gravity
    player.velocity_y += GRAVITY * dt

    # apply movement
    if player.hitbox.right <= PLAYER_RIGHT_LIMIT and player.hitbox.left >= PLAYER_LEFT_LIMIT:
        # Horizontal movement
        player.hitbox.x += player.velocity_x * dt
        for boundary in boundary_list:
            if player.hitbox.colliderect(boundary.rect):
                if player.velocity_x > 0:
                    player.hitbox.right = boundary.rect.left
                elif player.velocity_x < 0:
                    player.hitbox.left = boundary.rect.right
                player.velocity_x = 0

        #player.rect.center = player.hitbox.center
        #player.rect.x += 1
        #player.rect.y -= 1

        player.isOnEdgeOfScreen = False
    elif player.hitbox.right > PLAYER_RIGHT_LIMIT:
        player.hitbox.right = PLAYER_RIGHT_LIMIT
        x_offset += player.velocity_x * dt
        player.isOnEdgeOfScreen = True
    elif player.hitbox.left < PLAYER_LEFT_LIMIT:
        player.hitbox.left = PLAYER_LEFT_LIMIT
        x_offset += player.velocity_x * dt
        player.isOnEdgeOfScreen = True
    
    # Vertical movement
    player.hitbox.y += player.velocity_y * dt
    for boundary in boundary_list:
        if player.hitbox.colliderect(boundary.rect):
            if player.velocity_y > 0:
                player.hitbox.bottom = boundary.rect.top
                player.velocity_y = 0
                player.isOnGround = True
            elif player.velocity_y < 0:
                player.hitbox.top = boundary.rect.bottom
                player.velocity_y = 0

    # Sync sprite rect to hitbox
    player.rect.center = player.hitbox.center
    player.rect.x += 1
    player.rect.y -= 1

    for boundary in boundary_list:
        boundary.update(x_offset)

    # ground collision
    if player.rect.y >= GROUND_Y:
        player.rect.y = GROUND_Y
        player.velocity_y = 0
        player.isOnGround = True
        player.dash = False
        player.canDash = False

    screen.fill(WHITE)
    #screen.blit(frame_standing, (0, 0))
    screen.blit(player.image, player.rect)
    for boundary in boundary_list:
        screen.blit(boundary.image, boundary.rect)
    if devtools == 'on':
        print(player.hitbox)
        pygame.draw.rect(screen, (255,0,0), player.hitbox, 2)
    pygame.display.flip()

pygame.quit()