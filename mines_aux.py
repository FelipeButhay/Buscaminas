import pygame
import random
import os

screen_x, screen_y = 1920, 1080
while False:
    try:
        resolution = input("resolution (x,y format): ").split(",")
        screen_x = int(resolution[0])
        screen_y = int(resolution[1]) 
        break
    except:
        pass
    
import tkinter as tk
resolution_screen = tk.Tk()
screen_x = resolution_screen.winfo_screenwidth()
screen_y = resolution_screen.winfo_screenheight()
       
micro = (5, 3)
nano  = (10, 6)
small = (15, 9)
smid  = (20, 12)
mid   = (25, 15)
lmid  = (30, 18)
large = (35, 21)
xl    = (40, 24)
xxl   = (45, 27)
ultra = (50, 30)
#                0     1      2     3    4     5      6    7    8      9
lengths_srt = ("Micro", "Nano", "Small", "S-Mid", "Mid", "L-Mid", "Large",  "XL", "XXL", "Ultra")
lengths     = (micro, nano, small, smid, mid, lmid, large,  xl, xxl, ultra)
num_bombs   = (    3,   10,    20,   40,  60,   90,   120, 160, 200,   250)

around  = tuple((x-1,y-1) for y in range(0,3) for x in range(0,3) if (x,y)!=(1,1))
def around_fix(pos, indx):
    result = []
    for x,y in around:
        result.append((pos[0]+x, pos[1]+y))
    for x in result[:]:
        if not -1<x[0]:
            result.remove(x)
        elif not x[0]<lengths[indx][0]:
            result.remove(x)
        elif not -1<x[1]:
            result.remove(x)
        elif not x[1]<lengths[indx][1]:
            result.remove(x)
    return tuple(result)

direc = os.path.dirname(os.path.abspath(__file__)).replace('\'', '/')
flag  = pygame.image.load(f"{direc}/mines img/flag.png")
mine  = pygame.image.load(f"{direc}/mines img/mine.png")
minex = pygame.image.load(f"{direc}/mines img/mine_exploded.png")
one   = pygame.image.load(f"{direc}/mines img/one.png")
two   = pygame.image.load(f"{direc}/mines img/two.png")
three = pygame.image.load(f"{direc}/mines img/three.png")
four  = pygame.image.load(f"{direc}/mines img/four.png")
five  = pygame.image.load(f"{direc}/mines img/five.png")
six   = pygame.image.load(f"{direc}/mines img/six.png")
seven = pygame.image.load(f"{direc}/mines img/seven.png")
eight = pygame.image.load(f"{direc}/mines img/eight.png")
    
def gen(clicked, indx):
    clicked_ar = (clicked, *((x+clicked[0], y+clicked[1]) for x,y in around))
    bombs = []
    # crea las bombas
    while True:
        new_bomb = (random.randint(0, lengths[indx][0]-1), random.randint(0, lengths[indx][1]-1))
        if not new_bomb in bombs and not new_bomb in clicked_ar:
            bombs.append(new_bomb)
        if len(bombs) == num_bombs[indx]:
            bombs = tuple(bombs)
            break

    # crea el obj de cada casilla
    tiles = []
    for x in range(0,lengths[indx][0]):
        row = []
        for y in range(0,lengths[indx][1]):
            pos = (x,y)
            z = 0
            if pos in bombs:
                row.append(tile(True, pos, None))
            else:
                for n in around:
                    try:
                        if (pos[0]+n[0], pos[1]+n[1]) in bombs:
                            z += 1
                    except:
                        pass
                row.append(tile(False, pos, z))
        tiles.append(tuple(row))
    return tiles, bombs

def sizes(indx):
    sq = (screen_x*.8 + .99)//lengths[indx][0]
    x_gap = (screen_x-sq*lengths[indx][0])*0.5
    y_gap = (screen_y-sq*lengths[indx][1])*0.8
    gap = x_gap, y_gap
    
    sprites = [flag, one, two, three, four, five, six, seven, eight, mine, minex,]
    for x in sprites[:]:
        sprites.remove(x)
        sprites.append(pygame.transform.scale(x, (sq, sq)))
    
    return sq, gap, sprites
    
class tile:
    def __init__(self, bomb, position, num_of_bombs):
        self.pos = position
        self.flag = False
        self.bomb = bomb
        self.open = False
        self.num = num_of_bombs
        
    def draw(self, screen, finished, gap, sq, sprites):
        if self.flag:
            screen.blit(sprites[0], (gap[0]+sq*self.pos[0], gap[1]+sq*self.pos[1]))
        
        elif self.open and not self.bomb:
            if self.num == 0:
                pygame.draw.rect(screen, tuple(30 for x in range(0,3)), (gap[0]+sq*self.pos[0], gap[1]+sq*self.pos[1], sq, sq))
            else:
                screen.blit(sprites[self.num], (gap[0]+sq*self.pos[0], gap[1]+sq*self.pos[1]))
                
        elif self.open and self.bomb:
            screen.blit(sprites[10], (gap[0]+sq*self.pos[0], gap[1]+sq*self.pos[1]))
            
        elif finished and self.bomb:
            screen.blit(sprites[9], (gap[0]+sq*self.pos[0], gap[1]+sq*self.pos[1]))
            