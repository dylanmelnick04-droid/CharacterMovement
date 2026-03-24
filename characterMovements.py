import pygame

pygame.init()

# coin clip jpg is 1369p x 360p
# should add health bar next

devtools = 'on'
healthbars = 'on'
MAP = 'map1'
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
JUMP_STRENGTH = -500
GROUND_Y = 450
BLACK = (0, 0, 0)
GREEN = (0, 122, 122)

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

player1_controls = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "jump": pygame.K_w,
    "dash": pygame.K_LSHIFT
}

player2_controls = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "jump": pygame.K_UP,
    "dash": pygame.K_RSHIFT
}

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, walk_frames, controls):
        super().__init__()
        self.walk_frame = walk_frames
        self.walk_frame_index = 0
        self.image = self.walk_frame[self.walk_frame_index]
        #self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
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
        self.health = 100

        self.controls = controls

        self.animation_timer = 0
        self.animation_speed = 0.1

        self.hitbox = self.rect.inflate(WIDTH * -0.06, HEIGHT * -0.02)
        self.hitbox.center = self.rect.center
        self.hitbox.centerx -= 1
        self.hitbox.centery += 1

        self.healthbar = self.rect.inflate(WIDTH * 0.02, HEIGHT * -0.075)
        self.healthbar.center = self.rect.center
        self.healthbar.centerx -= 1
        self.healthbar.centery -= 30

        self.lives = 3

        self.alive = True
        
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

def handle_player(player, keys, dt):
    if keys[player.controls["left"]]:
        player.velocity_x -= ACCELERATION * dt
        player.mostRecentXDirection = 'Left'

    if keys[player.controls["right"]]:
        player.velocity_x += ACCELERATION * dt
        player.mostRecentXDirection = 'Right'

    if not keys[player.controls["left"]] and not keys[player.controls["right"]]:
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
        if player.dashTime <= 0:
            player.dash = False
    
    # apply gravity
    player.velocity_y += GRAVITY * dt

    # clamp horizontal speed
    if not player.dash:
        player.velocity_x = max(-MAX_SPEED, min(MAX_SPEED, player.velocity_x))
    if player.dash:
        player.velocity_x = max(-MAX_DASH_SPEED, min(MAX_DASH_SPEED, player.velocity_x))

def handle_event(player, event):
    if event.type == pygame.KEYDOWN:
        if event.key == player.controls["jump"] and player.isOnGround:
            player.velocity_y = JUMP_STRENGTH
            player.isOnGround = False
            player.canDash = True

        if event.key == player.controls["dash"] and not player.isOnGround and player.canDash:
            player.dash = True
            player.dashTime = player.dashDuration
            player.canDash = False

            if player.mostRecentXDirection == 'Right':
                player.velocity_x = player.dashSpeed
            else:
                player.velocity_x = -player.dashSpeed

def checkHealth(player, dt):
    if player.rect.y == GROUND_Y:
        screen.fill(BLACK)
        player.alive = False
        player.lives -= 1
        if player.lives != 0:
            # respawn
            player.health = 100
            player.alive = True
            player.rect.y = 0
            player.rect.x = 245
        else:
            return False

def apply_physics(player, dt):
    global x_offset

    #if player.hitbox.right <= PLAYER_RIGHT_LIMIT and player.hitbox.left >= PLAYER_LEFT_LIMIT:
    player.hitbox.x += player.velocity_x * dt
    for boundary in boundary_list:
        if player.hitbox.colliderect(boundary.rect):
            if player.velocity_x > 0:
                player.hitbox.right = boundary.rect.left
            elif player.velocity_x < 0:
                player.hitbox.left = boundary.rect.right
            player.velocity_x = 0

    player.isOnEdgeOfScreen = False

    # Vertical
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

    # Sync
    player.rect.center = player.hitbox.center
    player.rect.x += 1
    player.rect.y -= 1

    player.healthbar.center = player.rect.center
    player.healthbar.centerx -= 1
    player.healthbar.centery -= 30

    if player.rect.y >= GROUND_Y:
        player.rect.y = GROUND_Y
        player.velocity_y = 0
        player.isOnGround = True
        player.dash = False
        player.canDash = False

class Boundary(pygame.sprite.Sprite):
    def __init__(self, module_x, module_y):
        super().__init__()
        self.image = pygame.transform.scale(brick_sheet_image,(25, 25))
        self.rect = self.image.get_rect()
        #self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.rect.x = module_x
        self.rect.y = module_y
    def update(self, x_offset):
        self.rect.x -= x_offset

boundary_list = []
if MAP == 'map1':

    for i in range(16):
        boundary = Boundary(50 + 25 * i, 450)
        boundary_list.append(boundary)
    
    for i in range (3):
        boundary = Boundary(100 + 25 * i, 375)
        boundary_list.append(boundary)

    for i in range (6):
        boundary = Boundary(225 + 25 * i, 375)
        boundary_list.append(boundary)
    
    for i in range (2):
        boundary = Boundary(375 + 25 * i, 300)
        boundary_list.append(boundary)

    for i in range (4):
        boundary = Boundary(150 + 25 * i, 225)
        boundary_list.append(boundary)
    
    for i in range (2):
        boundary = Boundary(275 + 125 * i, 150)
        boundary_list.append(boundary)

player1 = Player(245, GROUND_Y, walk_frames, player1_controls)
player2 = Player(400, GROUND_Y, walk_frames, player2_controls)

players = []
players.append(player1)
players.append(player2)
x_offset = 0
running = True

while running:
    dt = clock.tick(60) / 1000  # seconds per frame
    player1.update(dt)
    player2.update(dt)
    x_offset = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

        handle_event(player1, event)
        handle_event(player2, event)

    keys = pygame.key.get_pressed()

    handle_player(player1, keys, dt)
    handle_player(player2, keys, dt)

    
    apply_physics(player1, dt)
    apply_physics(player2, dt)
    
    for boundary in boundary_list:
        boundary.update(x_offset)

    screen.fill(WHITE)
    for player in players:
        if checkHealth(player, dt) == False:
            running = False

    #screen.blit(frame_standing, (0, 0))
    screen.blit(player1.image, player1.rect)
    screen.blit(player2.image, player2.rect)
    for boundary in boundary_list:
        screen.blit(boundary.image, boundary.rect)
    if devtools == 'on':
        print(player1.hitbox)
        pygame.draw.rect(screen, (255,0,0), player1.hitbox, 2)
        pygame.draw.rect(screen, (255,0,0), player2.hitbox, 2)
    if healthbars == 'on':
        print(player1.healthbar)
        pygame.draw.rect(screen, (0, 122, 122), player1.healthbar)
        pygame.draw.rect(screen, (0, 122, 122), player2.healthbar)
    pygame.display.flip()

pygame.quit()