import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 400))
    screen.blit(floor_surface, (floor_x_pos+288, 400))


def create_pipe():
    pipe_height = random.randint(150, 275)
    void_width = random.randint(80, 150)
    top_height = pipe_height-void_width
    bottom_pipe = pipe_surface.get_rect(midtop=(300, pipe_height))
    top_pipe = pipe_surface.get_rect(midbottom=(300, top_height))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 470:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collisions(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 400:
        return False
    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*5, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 30))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        play_again = pygame.font.Font('04B_19.ttf', 20)
        score_surface = game_font.render(f'Score:{int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 200))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High-score:{int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(144, 230))
        play_again_surface = play_again.render(f'Press Space to play again!', True, (255, 255, 255))
        play_again_rect = high_score_surface.get_rect(center=(110, 265))
        screen.blit(high_score_surface, high_score_rect)
        screen.blit(play_again_surface, play_again_rect)


def update_score(final_score, final_high_score):
    if final_score > final_high_score:
        final_high_score = final_score
    return final_high_score


pygame.init()
screen = pygame.display.set_mode((288, 512))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

gravity = 0.16
bird_movement = 0

bg_surface = pygame.image.load("./sprites/background-day.png").convert()
floor_surface = pygame.image.load("./sprites/base.png").convert()
floor_x_pos = 0


bird_downflap = pygame.image.load("./sprites/bluebird-downflap.png").convert_alpha()
bird_midflap = pygame.image.load("./sprites/bluebird-midflap.png").convert_alpha()
bird_upflap = pygame.image.load("./sprites/bluebird-upflap.png").convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
pygame.display.set_icon(bird_midflap )
bird_rect = bird_surface.get_rect(center=(100, 206))
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load("./sprites/pipe-green.png").convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 800)
game_font = pygame.font.Font('04B_19.ttf', 30)

active_game = check_collisions(pipe_list)
score = 0
high_score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 5
            if event.key == pygame.K_SPACE and not active_game:
                active_game = True
                pipe_list.clear()
                bird_rect.center = (100, 206)
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
    bird_surface, bird_rect = bird_animation()
    screen.blit(bg_surface, (0, 0))
    if active_game:

        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)

        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_display('main_game')
        active_game = check_collisions(pipe_list)
        floor_x_pos -= 1
    else:
        high_score = update_score(score, high_score)
        score_display('game_over')

    if floor_x_pos <= -288:
        floor_x_pos = 0
    bird_rect.centery += bird_movement
    draw_floor()
    pygame.display.update()
    clock.tick(120)
