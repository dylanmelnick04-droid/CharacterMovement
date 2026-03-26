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
# add lives and character stats in corner

devtools = 'on'
healthbars = 'on'
backgroundArt = 'on'
player1_character = 'fireball'
player2_character = 'throwing_knife'
arena = False
drop_in_height = 100

MAP = 'map2'

MAP_LIST = {
    "map1": "town_hall",
    "map2": "arena",
    "map3": "bowl_of_milk",
    "map4": "starry_space"
}

# colors
WIDTH, HEIGHT = 500, 500
WHITE = (255, 255, 255)
GRAY = (34, 34, 34)
BLACK = (0, 0, 0)
GREEN = (0, 122, 122)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Character Mechanics")

clock = pygame.time.Clock()
sprite_sheet_image = pygame.image.load('image_reference/sprite_sheet/fireball_sprite_sheet.png').convert_alpha()
thor_sprite_sheet_image = pygame.image.load('image_reference/sprite_sheet/thor_sprite_sheet.png').convert_alpha()
knife_sprite_sheet_image = pygame.image.load('image_reference/sprite_sheet/throwing_knife_sprite_sheet.png').convert_alpha()
brick_sheet_image = pygame.image.load('image_reference/boundary/square_brick.jpg').convert_alpha()
translucent_block_sheet_image = pygame.image.load('image_reference/boundary/translucent_block.jpg').convert_alpha()
rainbow_brick_sheet_image = pygame.image.load('image_reference/boundary/rainbow_brick.jpg').convert_alpha()
throwing_knife_sheet_image = pygame.image.load('image_reference/entity/throwing_knife.png').convert_alpha()
fireball_sheet_image = pygame.image.load('image_reference/entity/fireball.png').convert_alpha()
name_of_the_wind_sheet_image = pygame.image.load('image_reference/entity/name_of_the_wind.png').convert_alpha()
thor_hammer_sheet_image = pygame.image.load('image_reference/entity/thor-hammer.png').convert_alpha()
crit_sheet_image = pygame.image.load('image_reference/entity/crit.jpg').convert_alpha()
medieval_town_background_image = pygame.image.load('image_reference/background/medieval_town_background.jpg').convert_alpha()
bowl_of_milk_background_image = pygame.image.load('image_reference/background/bowl_of_milk.jpg').convert_alpha()
space_background_image = pygame.image.load('image_reference/background/space_background.jpg').convert_alpha()

block_types = [
    brick_sheet_image,
    translucent_block_sheet_image,
    rainbow_brick_sheet_image
]

GRAVITY = 1500
ACCELERATION = 1500
DASH_ACCELERATION = 3000
FRICTION = 1200
MAX_SPEED = 400
MAX_DASH_SPEED = 700
if MAP == 'map4':
    JUMP_STRENGTH = -750
else:
    JUMP_STRENGTH = -500
GROUND_Y = 450
KNIFE_THROWING_VELOCITY = 2000
FIREBALL_THROWING_VELOCITY = 1000
THROWING_KNIFE_DAMAGE = 10
FIREBALL_DAMAGE = 33

PLAYER_LEFT_LIMIT = 100
PLAYER_RIGHT_LIMIT = 376

projectile_group = []

def getImage(sheet, frame, width, height, scale, color):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (frame*width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image


fireball_walk_frames = [
    getImage(sprite_sheet_image, 0, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 5, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 6, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 7, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 8, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 9, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 10, 24, 24, 2, BLACK),
    getImage(sprite_sheet_image, 23, 24, 24, 2, BLACK)
]

thor_walk_frames = [
    getImage(thor_sprite_sheet_image, 0, 158, 129, .35, BLACK),
    getImage(thor_sprite_sheet_image, 1, 228, 129, .35, BLACK),
    getImage(thor_sprite_sheet_image, 2, 214, 129, .35, BLACK),
    getImage(thor_sprite_sheet_image, 3, 170, 129, .35, BLACK),
    getImage(thor_sprite_sheet_image, 4, 157, 129, .35, BLACK),
    getImage(thor_sprite_sheet_image, 5, 147, 129, .35, BLACK),
    getImage(thor_sprite_sheet_image, 6, 117, 129, .35, BLACK),
    getImage(thor_sprite_sheet_image, 7, 170, 129, .35, BLACK)
]

knife_walk_frames = [
    getImage(knife_sprite_sheet_image, 3, 77, 100, .45, BLACK),
    getImage(knife_sprite_sheet_image, 0, 77, 100, .45, BLACK),
    getImage(knife_sprite_sheet_image, 1, 77, 100, .45, BLACK),
    getImage(knife_sprite_sheet_image, 2, 77, 100, .45, BLACK),
    getImage(knife_sprite_sheet_image, 3, 77, 100, .45, BLACK),
    getImage(knife_sprite_sheet_image, 0, 77, 100, .45, BLACK),
    getImage(knife_sprite_sheet_image, 1, 77, 100, .45, BLACK),
    getImage(knife_sprite_sheet_image, 2, 77, 100, .45, BLACK)
]

FIREBALL = {
    "damage": 33,
    "speed": 200,
    "health": 150,
    "upward_force": -50,
    "image": fireball_sheet_image,
    "image_offset": 220,
    "walk_frames": fireball_walk_frames,
    "character_melee_damage": 3,
    "melee_cooldown": .5
}
THROWING_KNIFE = {
    "damage": 10,
    "speed": 600,
    "health": 80,
    "upward_force": -50,
    "image": throwing_knife_sheet_image,
    "image_offset": 40,
    "walk_frames": knife_walk_frames,
    "character_melee_damage": 24,
    "melee_cooldown": .5
}
NAME_OF_THE_WIND = {
    "damage": 100,
    "speed": 1000,
    "health": 100,
    "upward_force": -20,
    "image": name_of_the_wind_sheet_image,
    "image_offset": 0,
    "walk_frames": knife_walk_frames,
    "character_melee_damage": 5,
    "melee_cooldown": 8
}
THOR = {
    "damage": 50,
    "speed": 800,
    "health": 200,
    "upward_force": -20,
    "image": thor_hammer_sheet_image,
    "image_offset": 90,
    "walk_frames": thor_walk_frames,
    "character_melee_damage": 80,
    "melee_cooldown": 10
}

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

map_create.create_map(boundary_list, MAP, block_types, arena)
match player1_character:
    case 'fireball':
        player1 = NewPlayer(150, drop_in_height, player1_controls, WIDTH, HEIGHT, FIREBALL)
    case 'throwing_knife':
        player1 = NewPlayer(150, drop_in_height, player1_controls, WIDTH, HEIGHT, THROWING_KNIFE)
    case 'thor':
        player1 = NewPlayer(150, drop_in_height, player1_controls, WIDTH, HEIGHT, THOR)
    case 'name_of_the_wind':
        player1 = NewPlayer(150, drop_in_height, player1_controls, WIDTH, HEIGHT, NAME_OF_THE_WIND)

match player2_character:
    case 'fireball':
        player2 = NewPlayer(350, drop_in_height, player2_controls, WIDTH, HEIGHT, FIREBALL)
    case 'throwing_knife':
        player2 = NewPlayer(350, drop_in_height, player2_controls, WIDTH, HEIGHT, THROWING_KNIFE)
    case 'thor':
        player2 = NewPlayer(350, drop_in_height, player2_controls, WIDTH, HEIGHT, THOR)
    case 'name_of_the_wind':
        player2 = NewPlayer(350, drop_in_height, player2_controls, WIDTH, HEIGHT, NAME_OF_THE_WIND)


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
    
    if backgroundArt == 'on':
        match MAP:
            case 'map1':
                screen.blit(medieval_town_background_image, (0, 0))
            case 'map2':
                screen.blit(space_background_image, (0, 0))
            case 'map3':
                screen.blit(bowl_of_milk_background_image, (0, 0))
            case 'map4':
                screen.blit(space_background_image, (0, 0))
    else:
        screen.fill(WHITE)
    
    for projectile in projectile_group:
        projectile.update(dt)
    
    for projectile in projectile_group:
        if projectile_utils.checkCollision(projectile, players) == True and devtools == 'on':
            screen.fill(BLACK)

    for player in players:
        if player_utils.checkHealth(player, dt, drop_in_height) == False:
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
        player_utils.drawHealthbar(player1, screen)
        player_utils.drawHealthbar(player2, screen)
    
    current_time = pygame.time.get_ticks() / 1000

    for player in players:
        if current_time - player.crit_start_time > player.crit_duration:
            player.displayCrit = False
        else:
            # scale the image
            small_crit = pygame.transform.scale(crit_sheet_image, 
                                                (crit_sheet_image.get_width() // 10, 
                                                crit_sheet_image.get_height() // 10))

            # calculate position above the player
            x = player.hitbox.centerx - small_crit.get_width() // 2
            y = player.hitbox.top - small_crit.get_height() + 10

            # draw it
            screen.blit(small_crit, (x, y))
            print("crit")
    pygame.display.flip()

pygame.quit()