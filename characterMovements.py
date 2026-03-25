import pygame
import math
import player_utils
import projectile_utils
import boundary
import map_create
from projectile import NewProjectile
from player import NewPlayer

pygame.init()

# coin clip jpg is 1369p x 360p
# add attacks and health bar depletion next

devtools = 'on'
healthbars = 'on'
MAP = 'map1'
# colors
WIDTH, HEIGHT = 500, 500
WHITE = (255, 255, 255)
GRAY = (34, 34, 34)
BLACK = (0, 0, 0)
GREEN = (0, 122, 122)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Mechanics")

clock = pygame.time.Clock()
sprite_sheet_image = pygame.image.load('character.png').convert_alpha()
brick_sheet_image = pygame.image.load('square_brick.jpg').convert_alpha()
throwing_knife_sheet_image = pygame.image.load('throwing_knife.png').convert_alpha()
fireball_sheet_image = pygame.image.load('fireball.png').convert_alpha()
name_of_the_wind_sheet_image = pygame.image.load('name_of_the_wind.png').convert_alpha()

GRAVITY = 1500
ACCELERATION = 1500
DASH_ACCELERATION = 3000
FRICTION = 1200
MAX_SPEED = 400
MAX_DASH_SPEED = 700
JUMP_STRENGTH = -500
GROUND_Y = 450
KNIFE_THROWING_VELOCITY = 2000
FIREBALL_THROWING_VELOCITY = 1000
THROWING_KNIFE_DAMAGE = 10
FIREBALL_DAMAGE = 33

FIREBALL = {
    "damage": 33,
    "speed": 200,
    "upward_force": -50,
    "image": fireball_sheet_image,
    "image_offset": 220,
    "character_melee_damage": 3,
    "melee_cooldown": .5
}
THROWING_KNIFE = {
    "damage": 10,
    "speed": 600,
    "upward_force": -50,
    "image": throwing_knife_sheet_image,
    "image_offset": 40,
    "character_melee_damage": 24,
    "melee_cooldown": .5
}
NAME_OF_THE_WIND = {
    "damage": 100,
    "speed": 1000,
    "upward_force": -20,
    "image": name_of_the_wind_sheet_image,
    "image_offset": 0,
    "character_melee_damage": 5,
    "melee_cooldown": 8
}
THOR = {
    "damage": 50,
    "speed": 800,
    "upward_force": -20,
    "image": throwing_knife_sheet_image,
    "image_offset": 0,
    "character_melee_damage": 80,
    "melee_cooldown": 10
}

PLAYER_LEFT_LIMIT = 100
PLAYER_RIGHT_LIMIT = 376

projectile_group = []

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
    "dash": pygame.K_LSHIFT,
    "throw": pygame.K_1,
    "melee": pygame.K_2
}

player2_controls = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "jump": pygame.K_UP,
    "dash": pygame.K_RSHIFT,
    "throw": pygame.K_p,
    "melee": pygame.K_o
}

def handle_event(player, event, players):
    if event.type == pygame.KEYDOWN:
        current_time = pygame.time.get_ticks() / 1000  # seconds

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
        
        if event.key == player.controls["throw"] and not player.hasThrown and player.canDash:
            
            p = NewProjectile(player.rect.x, player.rect.y, player.mostRecentXDirection, player.projectileType)
            projectile_group.append(p)
            player.projectiles.append(p)
            player.hasThrown = True
        
        if event.key == player.controls["melee"]:
            print("melee")
            player.hasMeleed = True

boundary_list = []

MAP = 'map1'

map_create.create_map(boundary_list, MAP, brick_sheet_image)

player1 = NewPlayer(245, GROUND_Y, walk_frames, player1_controls, WIDTH, HEIGHT, NAME_OF_THE_WIND)
player2 = NewPlayer(400, GROUND_Y, walk_frames, player2_controls, WIDTH, HEIGHT, FIREBALL)

players = []
players.append(player1)
players.append(player2)
running = True

while running:
    dt = clock.tick(60) / 1000  # seconds per frame
    player1.update(dt, BLACK)
    player2.update(dt, BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

        handle_event(player1, event, players)
        handle_event(player2, event, players)

    keys = pygame.key.get_pressed()

    player_utils.handle_player(player1, keys, dt)
    player_utils.handle_player(player2, keys, dt)
    
    for player in players:
        for p in player.projectiles[:]:
            if p.rect.bottom >= GROUND_Y:
                player.projectiles.remove(p)
                projectile_group.remove(p)
                player.hasThrown = False
        if player.hasMeleed == True:
            player_utils.meleeAttack(player, players)
            player.hasMeleed = False
        
    for projectile in projectile_group[:]:
        if projectile.rect.bottom >= GROUND_Y:
            projectile_group.remove(projectile)

    player_utils.apply_physics(player1, boundary_list, dt)
    player_utils.apply_physics(player2, boundary_list, dt)
    
    screen.fill(WHITE)
    
    for projectile in projectile_group:
        projectile.update(dt)
    
    for projectile in projectile_group:
        if projectile_utils.checkCollision(projectile, players) == True:
            screen.fill(BLACK)

    for player in players:
        if player_utils.checkHealth(player, dt) == False:
            running = False

    #screen.blit(frame_standing, (0, 0))
    screen.blit(player1.image, player1.rect)
    screen.blit(player2.image, player2.rect)
    for boundary in boundary_list:
        screen.blit(boundary.image, boundary.rect)
    for projectile in projectile_group:
        screen.blit(projectile.image, projectile.rect)
    if devtools == 'on':
        #print(player1.hitbox)
        pygame.draw.rect(screen, (255,0,0), player1.hitbox, 2)
        pygame.draw.rect(screen, (255,0,0), player2.hitbox, 2)
    if healthbars == 'on':
        #print(player1.healthbar)
        pygame.draw.rect(screen, (0, 122, 122), player1.healthbar)
        pygame.draw.rect(screen, (0, 122, 122), player2.healthbar)
    pygame.display.flip()

pygame.quit()