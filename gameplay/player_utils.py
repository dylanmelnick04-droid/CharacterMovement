import pygame
from gameplay.projectile import NewProjectile

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

def handle_event(event, players, ENV, projectile_group):
    if event.type == pygame.KEYDOWN:
        current_time = pygame.time.get_ticks() / 1000  # seconds
        for player in players:
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
            
        if event.key == pygame.K_h:
            match ENV["displayCharacterStats"]:
                case 'off':
                    print("Help Menu Start")
                    ENV["displayCharacterStats"] = 'on'
                case 'on':
                    print("Help Menu Stop")
                    ENV["displayCharacterStats"] = 'off'

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

def checkHealth(player, dt, dropInHeight):
    if player.rect.y == GROUND_Y or player.health <= 0:
        #screen.fill(BLACK)
        player.alive = False
        player.lives -= 1
        if player.lives > 0:
            # respawn
            player.health = player.maxHealth
            player.alive = True
            player.rect.y = dropInHeight
            player.rect.x = 245
        else:
            return False

def apply_physics(player, boundary_list, dt):
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

    if player.hitbox.bottom % 25 != 0:
        player.isOnGround = False

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
        player.isOnGround = False
        player.dash = False
        player.canDash = False


def meleeAttack(player, players):
    for p in players:
        if player != p and player.hitbox.colliderect(p.hitbox):
            if player.dash == True:
                p.health -= player.melee_damage * 2
                player.displayCrit = True
                player.crit_start_time = pygame.time.get_ticks() / 1000
            else:
                p.health -= player.melee_damage
    return


def drawHealthbar(player, screen):
    # update position
    player.healthbar.center = player.rect.center
    player.healthbar.centery -= 30

    # calculate ratio
    health_ratio = player.health / player.maxHealth

    # background
    pygame.draw.rect(screen, (255, 0, 0), player.healthbar)

    # foreground
    current_width = int(player.healthbar.width * health_ratio)
    current_bar = pygame.Rect(
        player.healthbar.x,
        player.healthbar.y,
        current_width,
        player.healthbar.height
    )
    pygame.draw.rect(screen, (0, 255, 0), current_bar)

def displayCharacterStats(screen, font, COLOR, players):
    x_difference = 0

    stats_rect = pygame.Rect(70, 10, 360, 95)
    pygame.draw.rect(screen, (COLOR), stats_rect, 0)
    pygame.draw.rect(screen, (0, 0, 0), stats_rect, 3) # outline

    for idx, player in enumerate(players):
        text_surface = font.render("Player " + str(idx + 1) + " Stats:", True, (0, 0, 0))
        screen.blit(text_surface, (80 + x_difference, 20))
        text_surface = font.render("Health: " + str(player.projectileType["health"]), True, (0, 0, 0))
        screen.blit(text_surface, (80 + x_difference, 40))
        text_surface = font.render("Projectile Damage: " + str(player.projectileType["damage"]), True, (0, 0, 0))
        screen.blit(text_surface, (80 + x_difference, 60))
        text_surface = font.render("Melee Damage: " + str(player.projectileType["character_melee_damage"]), True, (0, 0, 0))
        screen.blit(text_surface, (80 + x_difference, 80))
        x_difference = x_difference + 200
    return

def displayerCharacterLives(screen, font, COLOR, players):
    stats_rect = pygame.Rect(55, 470, 380, 33)
    pygame.draw.rect(screen, (COLOR), stats_rect, 0)
    pygame.draw.rect(screen, (0, 0, 0), stats_rect, 3) # outline
    
    x_difference = 30
    for player in players:
        text_surface = font.render("Lives: " + str(player.lives), True, (0, 0, 0))
        screen.blit(text_surface, (30 + x_difference, 480))
        x_difference = x_difference + 290


    return