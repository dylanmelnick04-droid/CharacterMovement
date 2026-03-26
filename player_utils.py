import pygame

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

def checkHealth(player, dt):
    if player.rect.y == GROUND_Y or player.health <= 0:
        #screen.fill(BLACK)
        player.alive = False
        player.lives -= 1
        if player.lives != 0:
            # respawn
            player.health = player.maxHealth
            player.alive = True
            player.rect.y = 0
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