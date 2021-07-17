import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos+288, 400))


def create_pipe():
    pipe_height = random.randint(100, 275)
    new_pipe = pipe_surface.get_rect(midtop=(300, pipe_height))
    return new_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface,pipe)


pygame.init()
screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

gravity = 0.16
bird_movement = 0


bg_surface = pygame.image.load("./sprites/background-day.png").convert()
floor_surface = pygame.image.load("./sprites/base.png").convert()
floor_x_pos = 0

bird_surface = pygame.image.load("./sprites/bluebird-midflap.png").convert()
bird_rect = bird_surface.get_rect(center=(100, 206))

pipe_surface = pygame.image.load("./sprites/pipe-green.png").convert()
pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 5
        if event.type == SPAWNPIPE:
            pipe_list.append(create_pipe())

    screen.blit(bg_surface, (0, 0))

    bird_movement += gravity
    screen.blit(bird_surface, bird_rect)

    pipe_list = move_pipe(pipe_list)
    draw_pipes(pipe_list)

    floor_x_pos -= 1

    if floor_x_pos <= -288:
        floor_x_pos = 0
    bird_rect.centery += bird_movement
    draw_floor()
    pygame.display.update()
    clock.tick(120)
