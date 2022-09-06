import sys

import pygame
from pygame.locals import *
import math
import random

FPS = 20.0
WIDTH, HEIGHT = 1920, 1080
SIZE = 10
PAUSE = True
STEP = False
alives = set()
x_start, y_start = 0, 0
        
def get_neighbours(cell):
    neighbours = [
        (cell[0] - 1, cell[1] - 1),
        (cell[0] - 1, cell[1]),
        (cell[0], cell[1] - 1),
        (cell[0] + 1, cell[1]),
        (cell[0], cell[1] + 1),
        (cell[0] + 1, cell[1] + 1),
        (cell[0] - 1, cell[1] + 1),
        (cell[0] + 1, cell[1] - 1),
    ]
    return neighbours

def count_near_alives(cell):
    global alives
    
    neighbours = get_neighbours(cell)
    alives_count = 0
    for n in neighbours:
        if n in alives:
            alives_count += 1
    return alives_count

def update_alives():
    global alives
    new_alives = set()
    for cell in alives:
        #Check if should stay, else dies
        cell_alive_neighbours = count_near_alives(cell) 
        if cell_alive_neighbours == 2 or cell_alive_neighbours == 3:
            new_alives.add(cell)
        
        #Spawn a new one
        neighbours = get_neighbours(cell)
        for n in neighbours:
            n_alive_neighbours = count_near_alives(n)
            if n not in alives and n_alive_neighbours == 3:
                new_alives.add(n)
    alives = new_alives            
        
def generate_random(filling_percentage = 30):
    global alives
    max_x = math.floor(WIDTH / SIZE)
    max_y = math.floor(HEIGHT / SIZE)
    
    for y in range(max_y):
        for x in range(max_x):
            if random.random() < (filling_percentage / 100):
                alives.add((x, y))


def update(dt):
    global alives
    global PAUSE
    global STEP
    global FPS
    global SIZE
    
    if not PAUSE:
        update_alives()
    if STEP:
        STEP = False
        update_alives()
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() 
            sys.exit()
        
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                return
            elif event.key == K_SPACE:
                
                PAUSE = not PAUSE
                print( "P" if PAUSE else "Unp", "aused", sep="")
            elif event.key == K_UP:
                FPS += 1
                print("FPS = ", FPS)
            elif event.key == K_DOWN and FPS >= 1:
                FPS -= 1
                print("FPS = ", FPS)
            elif event.key == K_r:
                
                alives.clear()
                generate_random(25)
                print("Reset")
            elif event.key == K_s:
                STEP = True
                print("Step")
        elif event.type == pygame.MOUSEWHEEL:
            x, y = pygame.mouse.get_pos()
            
            if event.y > 0:
                if SIZE > 1:
                    SIZE -= 1
            else:
                SIZE += 1
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
                
            x = math.floor(pos[0] / SIZE)
            y = math.floor(pos[1] / SIZE)
            if event.button == 3 and (x, y) in alives:
                alives.remove((x, y))
            else:
                alives.add((x, y))
        
def draw(screen):
    global alives
    screen.fill((0, 0, 0))
    
    max_x = math.floor(WIDTH / SIZE)
    max_y = math.floor(HEIGHT / SIZE)
    
    for y in range(max_y):
        screen.fill((30, 30, 30), (0, y * SIZE, WIDTH, 1))
    for x in range(max_x):
        screen.fill((30, 30, 30), (x * SIZE, 0, 1, HEIGHT))

    for cell in alives:
        x = cell[0]
        y = cell[1]
        # color = (math.floor(abs(x) / max_x * 255), math.floor(abs(y) / max_y * 255), math.floor(abs(y + x)  / (max_y + max_x) * 255))
        color = (math.floor(abs(x) / max_x * 255), math.floor(abs(y) / max_y * 255), 0)
        if x > 0 and x <= max_x and y > 0 and y <= max_y:
            screen.fill(color, (cell[0] * SIZE, cell[1] * SIZE, SIZE, SIZE))
    
    pygame.display.flip()
 
def run():
    pygame.init()
    fpsClock = pygame.time.Clock()
    global FPS

    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags = pygame.NOFRAME, display = 2)
    # generate_random(25)
    
    
    while True:
        dt = 1/FPS
        update(dt)
        draw(screen)
        
        dt = fpsClock.tick(FPS)

run()