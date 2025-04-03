import pygame
import sys

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
###---------- Game Window -------------
# ------starting Variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  ## display surface
pygame.display.set_caption("Arktoid")

### ------------------ texte
text_font1 = pygame.font.Font("resources/font/Pixeltype.ttf", 100)
text_font2 = pygame.font.Font("resources/font/Pixeltype.ttf", 40)

# -----------Music
pygame.mixer.music.load("resources/audio/music.wav")
pygame.mixer.music.play(-1)

#--- score
score = 0
level = 1
lives_init = 3
lives = lives_init

def display_score():
    score_surf = text_font1.render(f"{score}",
                                   False,
                                      "Pink")
    score_surf2 = text_font1.render(f"level: {level}/4",
                                   False,
                                   "Pink")
    score_surf3 = text_font2.render(f"lives: {lives}/{lives_init}",
                                    False,
                                    "Pink")
    # TODO nach oben links verschieben
    score_rect = score_surf.get_rect(center=(SCREEN_WIDTH / 2, 250))
    screen.blit(score_surf, score_rect)

    score_rect2 = score_surf2.get_rect(center=(SCREEN_WIDTH / 2, score_rect.bottom + 80))
    screen.blit(score_surf2, score_rect2)

    score_rect3 = score_surf3.get_rect(topleft=(0, 0))
    screen.blit(score_surf3, score_rect3)

# regular surfaces
#### paddle--------------------------------
paddle_rect = pygame.Rect(350, SCREEN_HEIGHT-50, 100, 20)
paddle_speed = 5

#### ball------------------------------
ball_pos_x = int(SCREEN_WIDTH / 2)
ball_pos_y = int(SCREEN_HEIGHT / 2)
# ball_v_x = 4
# ball_v_y = 4
ball_v = [4, 4]
ball_size = 25
ball_rect = pygame.Rect(ball_pos_x, ball_pos_y, ball_size, ball_size)

#### bricks -----------------------------
brick_width = 80
brick_height = 20
brick_gap = 10
bricks = []
num_bricks = 6

total_bricks_width = num_bricks * brick_width
total_gaps_width = (num_bricks - 1) * brick_gap
total_width = total_bricks_width + total_gaps_width

left_margin = (SCREEN_WIDTH - total_width) // 2
class Brick:
    def __init__(self, brick_rect, value):
        self.rect = brick_rect
        self.value = value

def calc_value(i):
    if i <= 1:
        return 5
    if i <= 3:
        return 10
    return 15

def getColor(value):
    if value <= 5:
        return (144, 238, 144) #self.color = (144, 238, 144) # (50, 205, 50) (34, 139, 34)
    elif value <= 10:
        return (50, 205, 50)
    return (34, 139, 34)


def bricks_init():
    bricks.clear()
    for idx_level in range(level):
        for idx_bricks in range(num_bricks):
            # x position: shift each brick horizontally by brick_width + spacing
            x = left_margin + idx_bricks * (brick_width + brick_gap)#i * (brick_width + brick_gap)
            y = 50 * (idx_level+1)  # all bricks aligned to the top of the window

            brick_rect = pygame.Rect(x, y, brick_width, brick_height)

            brick_tmp = Brick(brick_rect, calc_value(idx_bricks))
            bricks.append(brick_tmp)


def ball_init():
    global ball_v
    global ball_pos_x
    global ball_pos_y
    ball_pos_x = int(SCREEN_WIDTH / 2)
    ball_pos_y = int(SCREEN_HEIGHT / 2)
    ball_v = [4, 4]
    ball_rect.center = (ball_pos_x, ball_pos_y)

def reset_paddle():
    paddle_rect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT -50))


## ---------- game variable
running = True
game_active = True

def victory():
    screen.fill((255, 255, 255))
    global game_active
    game_active = False
    win_surf = text_font1.render(f"Victoire !   {score}", False, "Black")
    win_rect = win_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    play_again_surf = text_font2.render("press  <SPACE>  to play again", False, "Black")
    play_again_rect = play_again_surf.get_rect(center=(SCREEN_WIDTH / 2, 500))
    screen.blit(play_again_surf, play_again_rect)
    screen.blit(win_surf, win_rect)

def game_over():
    screen.fill((255, 255, 255))
    global game_active
    game_active = False
    game_over_surf = text_font1.render(f"Game Over!   {score}", False, "Black")
    game_over_rect = game_over_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    play_again_surf = text_font2.render("press  <SPACE>  to play again", False, "Black")
    play_again_rect = play_again_surf.get_rect(center=(SCREEN_WIDTH / 2, 500))
    screen.blit(play_again_surf, play_again_rect)
    screen.blit(game_over_surf, game_over_rect)

def level_up():
    global level
    level += 1

def ball_color(lev):
    if lev == 2:
        return ""


bricks_init()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle_rect.x -= 1
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score = 0
                game_active = True

    if game_active:
        key = pygame.key.get_pressed()

        screen.fill((0, 0, 0))
        display_score()
        pygame.draw.rect(screen, (255, 255, 255), paddle_rect, border_radius=5)
        pygame.draw.ellipse(screen, "Red", ball_rect)

        ## Bricks ----------------
        for brick in bricks:
            pygame.draw.rect(screen, getColor(brick.value), brick.rect)

        ## Paddle-------------------------------------------
        if key[pygame.K_LEFT] == True and paddle_rect.left >= 0:
            paddle_rect.x -= paddle_speed
        if key[pygame.K_RIGHT] == True and paddle_rect.right <= SCREEN_WIDTH:
            paddle_rect.x += paddle_speed

        ## ball ----------------------------------
        ball_pos_x += ball_v[0]
        ball_pos_y += ball_v[1]
        ball_rect.center = (ball_pos_x, ball_pos_y)
        if ball_rect.right >= SCREEN_WIDTH:
            ball_v[0] = -ball_v[0]
        if ball_rect.left <= 0:
            ball_v[0] = -ball_v[0]
        if ball_rect.top <= 0:
            ball_v[1] = -ball_v[1]

        ## ---- check Game Over
        if ball_rect.bottom >= SCREEN_HEIGHT:
            if lives > 1:
                screen.fill("Red")
                lives -= 1
                ball_v[1] = -ball_v[1]

            else:
                lives = lives_init
                level = 1
                ball_init()
                bricks_init()
                reset_paddle()
                game_over()

        ## --- check win
        if not bricks:
            if level < 3:
                level += 1
                paddle_speed += 2
                ball_size -= 5
                ball_v[0] *= 1.2
                ball_v[1] *= 1.2
                bricks_init()
            else:
                victory()

        ## --- collisions --------------------------
        if ball_rect.colliderect(paddle_rect):
            # TODO rebound multidirectional for corners and sides
            ball_v[1] = -ball_v[1]

        for brick in bricks:
            if brick.rect.colliderect(ball_rect):
                bricks.remove(brick)
                score+=brick.value
            # TODO rebound multidirectional
                ball_v[1] = -ball_v[1]



    pygame.display.flip()  # Mettre à jour l'écran
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
