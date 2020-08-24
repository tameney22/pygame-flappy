"""
Author: Yoseph Tamene
A simple Flappy Bird-like game.
"""

import pygame
import random
import sys

pygame.init()

WIDTH = 500
HEIGHT = 700

GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
BKG_COLOR = (0,0,0)
YELLOW = (255,255,0)

UP = False
VERTICAL = 20
player_size = 50
player_pos = [30 , HEIGHT / 2]

enemy_size = 50
GAP = 3 * enemy_size
enemy_pos = [WIDTH, random.randint(0, HEIGHT - GAP), random.randint(0, HEIGHT - GAP) + GAP]
enemy_list = []
SPEED = 10

score = 0
screen =  pygame.display.set_mode((WIDTH, HEIGHT))

game_over = False

clock = pygame.time.Clock()

FONT = pygame.font.SysFont("monospace", 35)

def GAME_OVER(score):
    screen.fill(BKG_COLOR)
    pygame.display.update()
    text = "GAME OVER!"
    text1 ="Your Score: " + str(score)
    label = FONT.render(text, 1, YELLOW)
    
    screen.blit(label, ((WIDTH / 2) - ((len(text) * 20) / 2), HEIGHT / 2))
    
    
    label1 = FONT.render(text1, 1, YELLOW)
    screen.blit(label1, ((WIDTH / 2) - ((len(text) * 25) / 2), HEIGHT / (5/2)))
    pygame.display.update()
    
def set_level(score, SPEED):
    if score < 20:
        SPEED = 5
    elif score < 40:
        SPEED = 8
    elif score < 60:
        SPEED = 10
    else:
        SPEED = 15
    return SPEED

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) == 0:
        x_pos = WIDTH
        y_pos = random.randint(0, HEIGHT - GAP)

        y_pos2 = y_pos + GAP

        enemy_list.append([x_pos, y_pos, y_pos2])
        

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, GREEN, (enemy_pos[0], 0, enemy_size, enemy_pos[1]))

        pygame.draw.rect(screen, GREEN, (enemy_pos[0], enemy_pos[2], enemy_size, HEIGHT - enemy_pos[2]))


def update_enemy_positions(enemy_list, score):
    for i, enemy_pos in enumerate(enemy_list):
        #Updates Enemy Position
        if enemy_pos[0] + enemy_size >= 0 and enemy_pos[0] <= WIDTH:
            enemy_pos[0] -= SPEED
        else:
            enemy_list.pop(i)
            score += 1
    return score

def update_player_position(player_pos, UP, VERTICAL):
    if (UP and VERTICAL >= 0):
        player_pos[1] -= VERTICAL
        VERTICAL -= 3
    elif (UP and VERTICAL < 0):
        UP = False
        VERTICAL = 20
    elif (not UP):
        player_pos[1] += 5
    
    return [VERTICAL, UP]


def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]
    e_y2 = enemy_pos[2]

    if (e_x == p_x + player_size) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y <= e_y or p_y >= e_y2):
            return True
        
    return False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_pos[0] -= player_size
            elif event.key == pygame.K_RIGHT:
                player_pos[0] += player_size
            elif event.key == pygame.K_UP:
                UP = True
            elif event.key == pygame.K_DOWN:
                player_pos[1] += player_size

    screen.fill(BKG_COLOR)
    
    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)
    [VERTICAL, UP] = update_player_position(player_pos, UP, VERTICAL)
    text = "Score: " + str(score)
    label = FONT.render(text, 1, YELLOW)
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))

    SPEED = set_level(score, SPEED)
                        
    if collision_check(enemy_list, player_pos):
        game_over = True
        GAME_OVER(score)
        break
    draw_enemies(enemy_list)

    
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
    pygame.display.update()
    
    
    clock.tick(30)


    


