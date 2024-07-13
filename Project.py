import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_SIZE = 20
BRICK_WIDTH = 75
BRICK_HEIGHT = 30
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Breaker")

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(BLACK)

paddle_image = pygame.image.load('paddle.png').convert_alpha()
paddle_image = pygame.transform.scale(paddle_image, (PADDLE_WIDTH, PADDLE_HEIGHT))

ball_image = pygame.image.load('ball.png').convert_alpha()
ball_image = pygame.transform.scale(ball_image, (BALL_SIZE, BALL_SIZE))

brick_image = pygame.image.load('brick.png').convert_alpha()
brick_image = pygame.transform.scale(brick_image, (BRICK_WIDTH, BRICK_HEIGHT))

bounce_sound = pygame.mixer.Sound('bounce.mp3')
break_sound = pygame.mixer.Sound('break.mp3')

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = paddle_image
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT - 10
        self.speed = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PADDLE_WIDTH:
            self.rect.x = SCREEN_WIDTH - PADDLE_WIDTH

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - BALL_SIZE) // 2
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed_x = random.choice([-5, 5])
        self.speed_y = -5

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x <= 0 or self.rect.x >= SCREEN_WIDTH - BALL_SIZE:
            self.speed_x = -self.speed_x
            bounce_sound.play()
        if self.rect.y <= 0:
            self.speed_y = -self.speed_y
            bounce_sound.play()

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = brick_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

paddle = Paddle()
ball = Ball()

all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()

all_sprites.add(paddle)
all_sprites.add(ball)

for row in range(5):
    for col in range(10):
        brick = Brick(col * (BRICK_WIDTH + 5) + 35, row * (BRICK_HEIGHT + 5) + 35)
        all_sprites.add(brick)
        bricks.add(brick)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    all_sprites.update()

    if pygame.sprite.collide_rect(ball, paddle):
        ball.speed_y = -ball.speed_y
        bounce_sound.play()

    brick_collisions = pygame.sprite.spritecollide(ball, bricks, True)
    if brick_collisions:
        ball.speed_y = -ball.speed_y
        break_sound.play()

    if ball.rect.y > SCREEN_HEIGHT:
        running = False  # Lose condition

    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()