import pygame
from sys import exit
import random

GAME_WIDTH = 360
GAME_HEIGHT = 640

BIRD_X = GAME_WIDTH/8
BIRD_Y = GAME_HEIGHT/2
BIRD_WIDTH = 30
BIRD_HEIGHT = 21

GRAVITY = 0.7
BIRD_VELOCITY_Y = -10
FLOOR_Y = GAME_HEIGHT

pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512

velocity_x = -2

class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False

background_image = pygame.image.load("images/background.jpg")
bird_image = pygame.image.load("images/bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH,BIRD_HEIGHT))
top_pipe_image = pygame.image.load("images/toppipe.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width,pipe_height))
bottom_pipe_image = pygame.image.load("images/bottompipe.png")
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (pipe_width,pipe_height))

pipes = []

def create_pipes():
    random_pipe_y = pipe_y - pipe_height/6 - random.random()*(pipe_height/2)
    opening_space = GAME_HEIGHT/4
    
    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + pipe_height + opening_space
    pipes.append(bottom_pipe)

def move_pipe():
     
    for pipe in pipes:
        pipe.x += velocity_x

    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(0)

create_pipes_timer = pygame.USEREVENT + 0

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Flappy bird")
pygame.display.set_icon(bird_image)
clock = pygame.time.Clock()

pygame.time.set_timer(create_pipes_timer, 1500)

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self,BIRD_X,BIRD_Y,BIRD_WIDTH,BIRD_HEIGHT)
        self.image = bird_image
        self.velocity_y = 0

bird = Bird(bird_image)

def move():
    bird.velocity_y += GRAVITY
    bird.y += bird.velocity_y
    bird.y = max(bird.y ,0)

    if bird.y + BIRD_HEIGHT > FLOOR_Y:
        bird.y = FLOOR_Y - BIRD_HEIGHT

def draw():
    window.blit(background_image, (0,0))
    window.blit(bird_image, bird)
    
    for pipe in pipes:
        window.blit(pipe.img, pipe)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == create_pipes_timer:
            create_pipes()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bird.velocity_y = BIRD_VELOCITY_Y

    move_pipe()
    move()
    draw()
    pygame.display.update()
    clock.tick(60)