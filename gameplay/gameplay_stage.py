import pygame
import math
import gameplay.player_utils
import gameplay.projectile_utils
import gameplay.boundary
import gameplay.map_create
from gameplay.projectile import NewProjectile
from gameplay.player import NewPlayer
from game_over.game_over_stage import GameOverStage

class GamePlayStage:
    def __init__(self, player1_character, player2_character, MAP, arena, lives):
        pygame.init()

        self.ENV = {
            "STAGE": 'gamePlay',
            "devtools": 'off',
            "healthbars": 'on',
            "backgroundArt": 'on',
            "player_lives": lives,
            "displayCharacterStats": 'off',
            "arena": arena
        }

        self.WIDTH, self.HEIGHT = 500, 500
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Character Mechanics")

        self.drop_in_height = 100

        self.MAP = MAP

        self.players = []

        self.clock = pygame.time.Clock()

        self.load_assets()

        self.boundary_list = []
        self.boundary_list.clear()
        gameplay.map_create.create_map(self.boundary_list, self.MAP, self.block_types, self.ENV["arena"])

        self.projectile_group = []

        self.player1_character = player1_character
        self.player2_character = player2_character

        self.character_stats_font = pygame.font.SysFont('Veranda', 20)
        self.character_lives_font = pygame.font.SysFont('Veranda', 30)

        self.create_players(self.player1_character, self.player2_character)

        
    
    def load_assets(self):
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.GRAY = (34, 34, 34)

        self.sprite_sheet_image = pygame.image.load('image_reference/sprite_sheet/fireball_sprite_sheet.png').convert_alpha()
        self.thor_sprite_sheet_image = pygame.image.load('image_reference/sprite_sheet/thor_sprite_sheet.png').convert_alpha()
        self.knife_sprite_sheet_image = pygame.image.load('image_reference/sprite_sheet/throwing_knife_sprite_sheet.png').convert_alpha()
        self.brick_sheet_image = pygame.image.load('image_reference/boundary/square_brick.jpg').convert_alpha()
        self.translucent_block_sheet_image = pygame.image.load('image_reference/boundary/translucent_block.jpg').convert_alpha()
        self.rainbow_brick_sheet_image = pygame.image.load('image_reference/boundary/rainbow_brick.jpg').convert_alpha()
        self.throwing_knife_sheet_image = pygame.image.load('image_reference/entity/throwing_knife.png').convert_alpha()
        self.fireball_sheet_image = pygame.image.load('image_reference/entity/fireball.png').convert_alpha()
        self.name_of_the_wind_sheet_image = pygame.image.load('image_reference/entity/name_of_the_wind.png').convert_alpha()
        self.thor_hammer_sheet_image = pygame.image.load('image_reference/entity/thor-hammer.png').convert_alpha()
        self.crit_sheet_image = pygame.image.load('image_reference/entity/crit.jpg').convert_alpha()
        self.medieval_town_background_image = pygame.image.load('image_reference/background/medieval_town_background.jpg').convert_alpha()
        self.bowl_of_milk_background_image = pygame.image.load('image_reference/background/bowl_of_milk.jpg').convert_alpha()
        self.space_background_image = pygame.image.load('image_reference/background/space_background.jpg').convert_alpha()
        self.doodle_background_image = pygame.image.load('image_reference/background/doodle_map.png').convert_alpha()

        self.fireball_walk_frames = [
            self.getImage(self.sprite_sheet_image, 0, 24, 24, 2, self.BLACK),
            self.getImage(self.sprite_sheet_image, 5, 24, 24, 2, self.BLACK),
            self.getImage(self.sprite_sheet_image, 6, 24, 24, 2, self.BLACK),
            self.getImage(self.sprite_sheet_image, 7, 24, 24, 2, self.BLACK),
            self.getImage(self.sprite_sheet_image, 8, 24, 24, 2, self.BLACK),
            self.getImage(self.sprite_sheet_image, 9, 24, 24, 2, self.BLACK),
            self.getImage(self.sprite_sheet_image, 10, 24, 24, 2, self.BLACK),
            self.getImage(self.sprite_sheet_image, 23, 24, 24, 2, self.BLACK)
        ]

        self.thor_walk_frames = [
            self.getImage(self.thor_sprite_sheet_image, 0, 158, 129, .35, self.BLACK),
            self.getImage(self.thor_sprite_sheet_image, 1, 228, 129, .35, self.BLACK),
            self.getImage(self.thor_sprite_sheet_image, 2, 214, 129, .35, self.BLACK),
            self.getImage(self.thor_sprite_sheet_image, 3, 170, 129, .35, self.BLACK),
            self.getImage(self.thor_sprite_sheet_image, 4, 157, 129, .35, self.BLACK),
            self.getImage(self.thor_sprite_sheet_image, 5, 147, 129, .35, self.BLACK),
            self.getImage(self.thor_sprite_sheet_image, 6, 117, 129, .35, self.BLACK),
            self.getImage(self.thor_sprite_sheet_image, 7, 170, 129, .35, self.BLACK)
        ]

        self.knife_walk_frames = [
            self.getImage(self.knife_sprite_sheet_image, 3, 77, 100, .45, self.BLACK),
            self.getImage(self.knife_sprite_sheet_image, 0, 77, 100, .45, self.BLACK),
            self.getImage(self.knife_sprite_sheet_image, 1, 77, 100, .45, self.BLACK),
            self.getImage(self.knife_sprite_sheet_image, 2, 77, 100, .45, self.BLACK),
            self.getImage(self.knife_sprite_sheet_image, 3, 77, 100, .45, self.BLACK),
            self.getImage(self.knife_sprite_sheet_image, 0, 77, 100, .45, self.BLACK),
            self.getImage(self.knife_sprite_sheet_image, 1, 77, 100, .45, self.BLACK),
            self.getImage(self.knife_sprite_sheet_image, 2, 77, 100, .45, self.BLACK)
        ]

        self.player1_controls = {
            "left": pygame.K_a,
            "right": pygame.K_d,
            "jump": pygame.K_w,
            "dash": pygame.K_LSHIFT,
            "throw": pygame.K_1,
            "melee": pygame.K_2
        }

        self.player2_controls = {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "jump": pygame.K_UP,
            "dash": pygame.K_RSHIFT,
            "throw": pygame.K_p,
            "melee": pygame.K_o
        }

        self.FIREBALL = {
            "damage": 33,
            "speed": 200,
            "health": 150,
            "upward_force": -50,
            "image": self.fireball_sheet_image,
            "image_offset": 220,
            "walk_frames": self.fireball_walk_frames,
            "character_melee_damage": 3,
            "character_melee_distance": 0.04,
            "melee_cooldown": .5
        }
        self.THROWING_KNIFE = {
            "damage": 10,
            "speed": 600,
            "health": 80,
            "upward_force": -50,
            "image": self.throwing_knife_sheet_image,
            "image_offset": 40,
            "walk_frames": self.knife_walk_frames,
            "character_melee_damage": 24,
            "character_melee_distance": 0.02,
            "melee_cooldown": .5
        }
        self.NAME_OF_THE_WIND = {
            "damage": 100,
            "speed": 1000,
            "health": 100,
            "upward_force": -20,
            "image": self.name_of_the_wind_sheet_image,
            "image_offset": 0,
            "walk_frames": self.knife_walk_frames,
            "character_melee_damage": 5,
            "character_melee_distance": 0.03,
            "melee_cooldown": 8
        }
        self.THOR = {
            "damage": 50,
            "speed": 800,
            "health": 200,
            "upward_force": -20,
            "image": self.thor_hammer_sheet_image,
            "image_offset": 90,
            "walk_frames": self.thor_walk_frames,
            "character_melee_damage": 80,
            "character_melee_distance": 0.04,
            "melee_cooldown": 10
        }

        self.block_types = [
            self.brick_sheet_image,
            self.translucent_block_sheet_image,
            self.rainbow_brick_sheet_image
        ]

        self.GRAVITY = 1500
        self.ACCELERATION = 1500
        self.DASH_ACCELERATION = 3000
        self.FRICTION = 1200
        self.MAX_SPEED = 400
        self.MAX_DASH_SPEED = 700
        if self.MAP == 'Starry Space':
            self.JUMP_STRENGTH = -750
        else:
            self.JUMP_STRENGTH = -500
        self.GROUND_Y = 475
        self.KNIFE_THROWING_VELOCITY = 2000
        self.FIREBALL_THROWING_VELOCITY = 1000
        self.THROWING_KNIFE_DAMAGE = 10
        self.FIREBALL_DAMAGE = 33

        self.PLAYER_LEFT_LIMIT = 100
        self.PLAYER_RIGHT_LIMIT = 376

        self.MAP_LIST = {
            "map1": "town_hall",
            "map2": "arena",
            "map3": "bowl_of_milk",
            "map4": "starry_space"
        }


    def updateGameplay(self):
        dt = self.clock.tick(60) / 1000
        for player in self.players:
            player.update(dt, self.BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()
                if event.key == pygame.K_r and self.ENV["STAGE"] == 'gameOver':
                    self.reset()
            if self.ENV["STAGE"] == 'gamePlay':
                gameplay.player_utils.handle_event(event, self.players, self.ENV, self.projectile_group)

        keys = pygame.key.get_pressed()

        for player in self.players:
            gameplay.player_utils.handle_player(player, keys, dt)

        for player in self.players:
            for p in self.projectile_group[:]:
                if p.rect.bottom >= self.GROUND_Y:
                    self.projectile_group.remove(p)
                    player.hasThrown = False
                    print("hasthrown = false")
            if player.hasMeleed == True:
                gameplay.player_utils.meleeAttack(player, self.players)
                #player.hasMeleed = False
            
            for projectile in self.projectile_group[:]:
                if projectile.rect.bottom >= self.GROUND_Y:
                    self.projectile_group.remove(projectile)

            for player in self.players:
                gameplay.player_utils.apply_physics(player, self.boundary_list, dt)
                
            for projectile in self.projectile_group:
                projectile.update(dt)
            
            for projectile in self.projectile_group:
                if gameplay.projectile_utils.checkCollision(projectile, self.players) == True and self.ENV["devtools"] == 'on':
                    self.screen.fill(self.BLACK)

        for idx, player in enumerate(self.players):
            if gameplay.player_utils.checkHealth(player, dt, self.drop_in_height) == False:
                self.ENV["STAGE"] = 'gameOver'
                print("gg")
                return ("GAME_OVER", {"winner": (idx + 1) % 2})
                exit()
       
        self.draw()
        pygame.display.flip()
        return None

    def draw(self):
        if self.ENV["backgroundArt"] == 'on':
            self.draw_background()
        else:
            self.screen.fill(self.WHITE)

        for player in self.players:
            self.screen.blit(player.image, player.rect)

        for boundary in self.boundary_list:
            self.screen.blit(boundary.image, boundary.rect)

        for projectile in self.projectile_group:
            self.screen.blit(projectile.image, projectile.rect)

        if self.ENV["devtools"] == 'on':
            pygame.draw.rect(self.screen, (255,0,0), self.players[0].hitbox, 2)
            pygame.draw.rect(self.screen, (255,0,0), self.players[1].hitbox, 2)
        
        if self.ENV["healthbars"] == 'on':
            for player in self.players:
                gameplay.player_utils.drawHealthbar(player, self.screen)

        current_time = pygame.time.get_ticks() / 1000

        for player in self.players:
            if current_time - player.crit_start_time > player.crit_duration:
                player.displayCrit = False
            else:
                # scale the image
                small_crit = pygame.transform.scale(self.crit_sheet_image, 
                                                    (self.crit_sheet_image.get_width() // 10, 
                                                    self.crit_sheet_image.get_height() // 10))

                # calculate position above the player
                x = player.hitbox.centerx - small_crit.get_width() // 2
                y = player.hitbox.top - small_crit.get_height() + 10

                # draw it
                self.screen.blit(small_crit, (x, y))
                print("crit")
        for player in self.players:
            if player.hasMeleed:
                # scale up the knife (e.g., 2x the original size)
                knife = pygame.transform.scale(
                    self.throwing_knife_sheet_image,
                    (self.throwing_knife_sheet_image.get_width() // 15,
                    self.throwing_knife_sheet_image.get_height() // 15)
                )

                # calculate position above the player
                if player.mostRecentXDirection == 'Left':
                    x = player.hitbox.centerx - knife.get_width() // 2 - 5
                else:
                    x = player.hitbox.centerx - 15
                y = player.hitbox.top - knife.get_height() + 30

                # draw the knife
                if player.mostRecentXDirection == 'Left':
                    flippedKnife = pygame.transform.flip(knife, True, False)
                    self.screen.blit(flippedKnife, (x, y))
                else:
                    self.screen.blit(knife, (x, y))
                player.hasMeleed = False
        if self.ENV["devtools"] == 'on':
            for player in self.players:
                pygame.draw.rect(self.screen, (255,0,0), player.meleeHitbox, 2)
        
        if self.ENV.get("displayCharacterStats") == 'on':
            gameplay.player_utils.displayCharacterStats(self.screen, self.character_stats_font, self.WHITE, self.players)
        
        gameplay.player_utils.displayerCharacterLives(self.screen, self.character_lives_font, self.WHITE, self.players)

    def draw_background(self):
        match self.MAP:
            case 'Town Hall':
                self.screen.blit(self.medieval_town_background_image, (0, 0))
            case 'Arena':
                self.screen.blit(self.space_background_image, (0, 0))
            case 'Bowl of Milk':
                self.screen.blit(self.bowl_of_milk_background_image, (0, 0))
            case 'Starry Space':
                self.screen.blit(self.space_background_image, (0, 0))
            case 'Doodle':
                self.screen.blit(self.doodle_background_image, (0, 0))

    def reset(self):
        self.boundary_list.clear()
        gameplay.map_create.create_map(self.boundary_list, self.MAP, self.block_types, False)

        self.projectile_group.clear()

        self.create_players(self.player1_character, self.player2_character)
        self.ENV["STAGE"] = 'gamePlay'

    def create_players(self, player1_character, player2_character):
        match player1_character:
            case 'fireball':
                player1 = NewPlayer(150, self.drop_in_height, self.player1_controls, self.WIDTH, self.HEIGHT, self.FIREBALL, self.ENV)
            case 'throwing_knife':
                player1 = NewPlayer(150, self.drop_in_height, self.player1_controls, self.WIDTH, self.HEIGHT, self.THROWING_KNIFE, self.ENV)
            case 'thor':
                player1 = NewPlayer(150, self.drop_in_height, self.player1_controls, self.WIDTH, self.HEIGHT, self.THOR, self.ENV)
            case 'name_of_the_wind':
                player1 = NewPlayer(150, self.drop_in_height, self.player1_controls, self.WIDTH, self.HEIGHT, self.NAME_OF_THE_WIND, self.ENV)

        match player2_character:
            case 'fireball':
                player2 = NewPlayer(350, self.drop_in_height, self.player2_controls, self.WIDTH, self.HEIGHT, self.FIREBALL, self.ENV)
            case 'throwing_knife':
                player2 = NewPlayer(350, self.drop_in_height, self.player2_controls, self.WIDTH, self.HEIGHT, self.THROWING_KNIFE, self.ENV)
            case 'thor':
                player2 = NewPlayer(350, self.drop_in_height, self.player2_controls, self.WIDTH, self.HEIGHT, self.THOR, self.ENV)
            case 'name_of_the_wind':
                player2 = NewPlayer(350, self.drop_in_height, self.player2_controls, self.WIDTH, self.HEIGHT, self.NAME_OF_THE_WIND, self.ENV)

        self.players.append(player1)
        self.players.append(player2)
    
    def getImage(self, sheet, frame, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(sheet, (0, 0), (frame*width, 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image