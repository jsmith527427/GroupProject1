import pygame
import sys

pygame.init()

#Initializing all constants
screen_width = 900
screen_height = 600
paddle_width = 100
paddle_height = 20
ball_size = 20
brick_width = 75
brick_height = 30
fps = 60

#Set the screen size and the caption
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Block Breaker")

#The background needs to be the same size and black
background = pygame.Surface((screen_width, screen_height))
background.fill((0, 0, 0))

#these are all the images and scaling the images so they dont cover the whole screen
paddle_image = pygame.image.load('paddle.png').convert_alpha()
paddle_image = pygame.transform.scale(paddle_image, (paddle_width, paddle_height))
ball_image = pygame.image.load('ball.png').convert_alpha()
ball_image = pygame.transform.scale(ball_image, (ball_size, ball_size))
brick_image = pygame.image.load('brick.png').convert_alpha()
brick_image = pygame.transform.scale(brick_image, (brick_width, brick_height))

#The two required sounds, bringing total called files to 5
bounce_sound = pygame.mixer.Sound('bounce.mp3')
break_sound = pygame.mixer.Sound('break.mp3')

#Defining the paddle for the game
class Paddle:
    #Initializing the starts
    def __init__(self):
        self.image = paddle_image
        self.rect = self.image.get_rect()
        self.rect.x = (screen_width - paddle_width) // 2 #center it
        self.rect.y = screen_height - paddle_height - 10 #put near bottom
        self.speed = 10 #speed

    #Defining how you move.
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: #move left
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:#move right
            self.rect.x += self.speed
        # if it touches either side, it is reset to a position within the screen.
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > screen_width - paddle_width:
            self.rect.x = screen_width - paddle_width

#Defining the bacll
class Ball:
    #Initialization
    def __init__(self):
        self.image = ball_image
        self.rect = self.image.get_rect()
        self.rect.x = (screen_width - ball_size) // 2 #center it
        self.rect.y = screen_height // 2 #center it again
        self.speed_x = 3 #horitontal speed
        self.speed_y = -5 #vertical speed

    #it will start in the middle and move in all 4 directions.
    def move(self):
        #update balls position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        #if it hites the walls it changes direction
        if self.rect.x <= 0 or self.rect.x >= screen_width - ball_size:
            self.speed_x = -self.speed_x
            bounce_sound.play()
        #if it hits the cieling it changes direction
        if self.rect.y <= 0:
            self.speed_y = -self.speed_y
            bounce_sound.play()

#simple brick inititation
class Brick:
    def __init__(self, x, y):
        self.image = brick_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#Making the objects
paddle = Paddle()
ball = Ball()
bricks = []

#Putting it all into a list for easier updating later
all_sprites = []
all_sprites.append(paddle)
all_sprites.append(ball)

#create the bricks and add to list
for row in range(5): #5 rows
    for col in range(10): #10 collumns
        brick = Brick(col * (brick_width +5) + 35, row * (brick_height + 5) + 35)
        all_sprites.append(brick)
        bricks.append(brick)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #quit game
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #alternate quit game using esc
                running = False

    #update all sprites (using sprites as terminology for interactable surface)
    for sprites in all_sprites:
        if hasattr(sprites, 'move'):
            sprites.move()

    #check for collision for ball and paddle
    if ball.rect.colliderect(paddle.rect):
        ball.speed_y = -ball.speed_y #bounce it off the paddle
        bounce_sound.play() #boioioioioing

    #check for collision for ball and bricks
    for brick in bricks:
        if ball.rect.colliderect(brick.rect):
            bricks.remove(brick) #remove the brick from the list
            all_sprites.remove(brick) #remove brick from sprite list
            ball.speed_y = -ball.speed_y #bounce brick off
            break_sound.play()
            break

    #if ball falls to bottom, lose
    if ball.rect.y > screen_height:
        running = False

    #draw everything (this is why i put it in a list, this is way easier than doing everyhting individually)
    screen.blit(background, (0, 0))
    for sprites in all_sprites:
        screen.blit(sprites.image, sprites.rect)

    #update the screen
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()