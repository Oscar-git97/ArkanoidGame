import pygame
import sys
import random

# ---------- Constants ----------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BRICK_WIDTH = 80
BRICK_HEIGHT = 20
BRICK_GAP = 10
NUM_BRICKS = 6
LIVES_INIT = 3

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arktoid")
clock = pygame.time.Clock()

pygame.mixer.music.load("resources/audio/music.wav")
pygame.mixer.music.play(-1)

# ---------- Fonts ----------
text_font1 = pygame.font.Font("resources/font/Pixeltype.ttf", 100)
text_font2 = pygame.font.Font("resources/font/Pixeltype.ttf", 40)

# ---------- Classes ----------
class Paddle:
    def __init__(self):
        self.end_message = ""
        self.rect = pygame.Rect(350, SCREEN_HEIGHT - 50, 100, 20)
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=5)

    def reset(self):
        self.end_message = ""
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)


class Ball:
    def __init__(self):
        self.size = 25
        self.rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.size, self.size)
        self.v = [4, 4]

    def update(self):
        self.rect.x += self.v[0]
        self.rect.y += self.v[1]

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.v[0] = -self.v[0]
        if self.rect.top <= 0:
            self.v[1] = -self.v[1]

    def draw(self, surface):
        pygame.draw.ellipse(surface, "Red", self.rect)

    def reset(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.v = [4, 4]


class Brick:
    def __init__(self, x, y, value):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.value = value

    def draw(self, surface):
        color = self.get_color()
        pygame.draw.rect(surface, color, self.rect)

    def get_color(self):
        if self.value <= 5:
            return (144, 238, 144)
        elif self.value <= 10:
            return (50, 205, 50)
        return (34, 139, 34)


class BrickManager:
    def __init__(self, level):
        self.bricks = []
        self.level = level
        self.init_bricks()

    def init_bricks(self):
        self.bricks.clear()
        total_width = NUM_BRICKS * BRICK_WIDTH + (NUM_BRICKS - 1) * BRICK_GAP
        left_margin = (SCREEN_WIDTH - total_width) // 2

        for row in range(self.level):
            for i in range(NUM_BRICKS):
                x = left_margin + i * (BRICK_WIDTH + BRICK_GAP)
                y = 50 * (row + 1)
                value = self.calc_value(i)
                self.bricks.append(Brick(x, y, value))

    def calc_value(self, i):
        if i <= 1:
            return 5
        elif i <= 3:
            return 10
        return 15

    def draw(self, surface):
        for brick in self.bricks:
            brick.draw(surface)


class Game:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.lives = LIVES_INIT
        self.running = True
        self.active = True

        self.paddle = Paddle()
        self.ball = Ball()
        self.brick_manager = BrickManager(self.level)

    def display_ui(self):
        score_surf = text_font1.render(f"{self.score}", False, "Pink")
        level_surf = text_font1.render(f"level: {self.level}/4", False, "Pink")
        lives_surf = text_font2.render(f"lives: {self.lives}/{LIVES_INIT}", False, "Pink")

        screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, 250)))
        screen.blit(level_surf, level_surf.get_rect(center=(SCREEN_WIDTH // 2, 330)))
        screen.blit(lives_surf, (10, 10))

    def check_collisions(self):
        if self.ball.rect.colliderect(self.paddle.rect):
            self.ball.v[1] = -self.ball.v[1]

        for brick in self.brick_manager.bricks[:]:
            if brick.rect.colliderect(self.ball.rect):
                self.brick_manager.bricks.remove(brick)
                self.score += brick.value
                self.ball.v[1] = -self.ball.v[1]

    def check_game_over(self):
        if self.ball.rect.bottom >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives > 0:
                screen.fill("Red")
                self.ball.v[1] = -self.ball.v[1]
            else:
                self.show_end_screen("Game Over!")

    def check_level_complete(self):
        if not self.brick_manager.bricks:
            if self.level < 3:
                self.level += 1
                self.paddle.speed += 2
                self.ball.size -= 5
                self.ball.v[0] *= 1.2
                self.ball.v[1] *= 1.2
                self.ball.reset()
                self.paddle.reset()
                self.brick_manager = BrickManager(self.level)
            else:
                self.show_end_screen("Victoire !")

    def show_end_screen(self, message):
        self.active = False
        self.end_message = message

    def reset(self):
        self.score = 0
        self.level = 1
        self.lives = LIVES_INIT
        self.paddle = Paddle()
        self.ball = Ball()
        self.brick_manager = BrickManager(self.level)
        self.active = True

    def run(self):
        while self.running:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if not self.active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.reset()

            screen.fill((0, 0, 0))

            if self.active:
                self.paddle.update(keys)
                self.ball.update()
                self.check_collisions()
                self.check_game_over()
                self.check_level_complete()

                self.paddle.draw(screen)
                self.ball.draw(screen)
                self.brick_manager.draw(screen)
                self.display_ui()
            else:
                screen.fill((255, 255, 255))
                msg_surf = text_font1.render(f"{self.end_message}   {self.score}", False, "Black")
                msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

                replay_surf = text_font2.render("press <SPACE> to play again", False, "Black")
                replay_rect = replay_surf.get_rect(center=(SCREEN_WIDTH // 2, 500))

                screen.blit(msg_surf, msg_rect)
                screen.blit(replay_surf, replay_rect)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

# ---------- Run the Game ----------
if __name__ == "__main__":
    game = Game()
    game.run()
