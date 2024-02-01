import pygame
import math
import mines_aux as aux

pygame.init()
clock  = pygame.time.Clock()
screen = pygame.display.set_mode((aux.screen_x, aux.screen_y))
pygame.display.set_caption("Minesweeper")
icon = pygame.image.load(f"{aux.direc}/mines img/icon.png")
pygame.display.set_icon(icon)

direc_font = f"{aux.direc}/mines img/CONSOLA.TTF"
ZERO = "0"
def zerocomp(points, num_of_z):
    if points > 0:
        return f" {ZERO*(num_of_z-int(math.log(points, 10))-1)}{points}"
    elif points == 0:
        return f" {ZERO*num_of_z}"
    else:
        return f"-{ZERO*(num_of_z-int(math.log(abs(points), 10))-1)}{abs(points)}"

font  = pygame.font.Font(direc_font, int(aux.screen_y*.12))
arrow = pygame.image.load(f"{aux.direc}/mines img/arrow.png")
arrow_left  = pygame.transform.scale(arrow, (aux.screen_y*.1, aux.screen_y*.16))
arrow_right = pygame.transform.rotate(arrow_left, 180)

bombs = []
finished = False
mouse = False
flag_c = 0
time = 0
indx = None
temp_indx = 0
pitagoras = lambda c1, c2: (c1**2 + c2**2)**0.5

tiles = []
while not finished and indx == None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
                
    mouse_save = mouse
    mouse = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
            
    screen.fill(tuple(20 for x in range(0,3)))
    img = font.render("Minesweeper", True, "white")
    screen.blit(img, img.get_rect(center = (aux.screen_x/2, aux.screen_y*.16)))
            
    screen.blit(arrow_left,  (aux.screen_x*.2, aux.screen_y*.65))
    screen.blit(arrow_right, (aux.screen_x*.8-aux.screen_y*.1, aux.screen_y*.65))
    pygame.draw.circle(screen, (255, 136, 36), (aux.screen_x/2, aux.screen_y*.45), aux.screen_y*.15)
    screen.blit(pygame.transform.scale(aux.mine, (aux.screen_y*.3, aux.screen_y*.3)), (aux.screen_x/2 - aux.screen_y*.15, aux.screen_y*.45 - aux.screen_y*.15))
    
    if mouse[0] and not mouse_save[0]:
        if ((aux.screen_x*.2) < mouse_pos[0] < (aux.screen_x*.2 + aux.screen_y*.1)) and ((aux.screen_y*.65) < mouse_pos[1] < (aux.screen_y*.81)):
            temp_indx-=1
        if ((aux.screen_x*.8-aux.screen_y*.1) < mouse_pos[0] < (aux.screen_x*.8)) and ((aux.screen_y*.65) < mouse_pos[1] < (aux.screen_y*.81)):
            temp_indx+=1
        if pitagoras(aux.screen_x/2-mouse_pos[0], aux.screen_y*.45-mouse_pos[1]) < aux.screen_y*.15:
            indx = temp_indx%len(aux.lengths)
            
    img = font.render(aux.lengths_srt[temp_indx%len(aux.lengths)], True, "white")
    screen.blit(img, img.get_rect(center = (aux.screen_x/2, (aux.screen_y*.65 + aux.screen_y*.81)//2)))
    
    pygame.display.update()
    clock.tick(60)

sq, gap, sprites = aux.sizes(indx)
get_tile = lambda mouse_pos: (((mouse_pos[0]-gap[0])*aux.lengths[indx][0])//(aux.lengths[indx][0]*sq), ((mouse_pos[1]-gap[1])*aux.lengths[indx][1])//(aux.lengths[indx][1]*sq)) 
font  = pygame.font.Font(direc_font, int(gap[1]/2))

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    time+=1
    time_s = int(time%60**2/60**1)
    if time_s < 10:
        time_s = "0"+ str(time_s)
    else:
        time_s = str(time_s)
        
    time_min = int(time%60**3/60**2)
    if time_min < 10:
        time_min = "0"+ str(time_min)
    else:
        time_min = str(time_min)
        
    time_h = int(time%60**4/60**3)
    if time_h < 10:
        time_h = "0"+ str(time_h)
    else:
        time_h = str(time_h)
            
    mouse_save = mouse
    mouse = pygame.mouse.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    
    if mouse[0] and not mouse_save[0]:
        if len(tiles)==0:
            tiles, bombs = aux.gen(get_tile(mouse_pos), indx)
            
        x,y = get_tile(mouse_pos)
        try:
            if not tiles[int(x)][int(y)].flag:
                tiles[int(x)][int(y)].open = True
                
                if tiles[int(x)][int(y)].bomb:
                    finished = True
        except:
            pass
        
    elif mouse[2] and not mouse_save[2]:
        if len(tiles)==0:
            tiles, bombs = aux.gen(get_tile(mouse_pos), indx)
            
        x,y = get_tile(mouse_pos)
        try:
            if not tiles[int(x)][int(y)].open:
                tiles[int(x)][int(y)].flag = not tiles[int(x)][int(y)].flag
                if tiles[int(x)][int(y)].flag:
                    flag_c +=1
                else:
                    flag_c -=1
        except:
            pass
            
    screen.fill(tuple(20 for x in range(0,3)))
    # celeste (16, 130, 180), naranja (255, 136, 36), verde (13, 150, 15), violeta (176, 12, 195)
    pygame.draw.rect(screen, (255, 136, 36), (gap[0], gap[1], aux.lengths[indx][0]*sq, aux.lengths[indx][1]*sq))
            
    if finished:
        img = font.render("boom!", True, "white")
        screen.blit(img, img.get_rect(midleft = (gap[0], gap[1]//2)))
    
    if len(bombs)!=0 and (aux.num_bombs[indx]-flag_c)==0:
        for x,y in bombs:
            if not tiles[x][y].flag:
                break
        else:
            for x in tiles:
                for y in x:
                    y.open = True
            img = font.render("boomn't!", True, "white")
            screen.blit(img, img.get_rect(midleft = (gap[0], gap[1]//2)))
            finished = True
            
    img = font.render("bombs " + zerocomp(aux.num_bombs[indx]-flag_c, 3), True, "white")
    screen.blit(img, img.get_rect(midright = (aux.screen_x - gap[0] , gap[1]//2))) 
    
    img = font.render(f"{time_h}:{time_min}:{time_s}", True, "white")
    screen.blit(img, img.get_rect(center = (aux.screen_x//2, gap[1]//2))) 
    
    for x in tiles:
        for y in x:
            if len(tiles)!=0 and y.num==0 and y.open:
                for z in aux.around_fix(y.pos, indx):
                    if not tiles[z[0]][z[1]].bomb:
                        tiles[z[0]][z[1]].open = True 
            y.draw(screen, finished, gap, sq, sprites)
    
    pygame.display.update()
    clock.tick(60)
    
while finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
