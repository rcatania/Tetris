import utilities
from globals_and_constants import *
import pygame
import math

def draw_screen(screen):
    blocks = get_lists()
    blocks = blocks[1]
    global black
    screen.fill(pygame.Color(125,125,125)) #192,192 192 (silver) isn't bad although friends have preferred this colour
    pygame.draw.rect(screen,white,((EDGES,0,screen_size[0]-EDGES*2,screen_size[1]-EDGES)),0)
    for block in blocks:
        block.draw()
        
paused = False
bool_faster = False
waiting_time = 125
bool_debug = False

permission_left = True
permission_right = True
permission_down = True
count_no_movement = 0
difference = [0,0]
rotation = False


def left(tetronimoe):
    global premission_left
    if permission_left:
        count_no_movement = 0
        tetronimoe.move((-30,0))
        add_diff((-30,0))
        
def right(tetronimoe):
    global permission_right,count_no_movement
    if permission_right:
        count_no_movement = 0
        tetronimoe.move((30,0))
        add_diff((30,0))
        
def reset_permissions():
    global permission_left, permission_right,permission_down
    permission_left = True
    permission_right = True
    permission_down = True
    
def add_diff(diff):
    global difference
    difference[0] += diff[0]
    difference[1] += diff[1]
    
def pause():    #Note: These functions have to be set because they are called through eval.  Cannot assign through eval
    global paused
    paused = not paused #If the game is not paused, it will be paused.  If it is paused it will be unpaused.  This is set as a function so it can be passed through eval

def faster():
    global bool_faster
    bool_faster = True    

def debug():
    global bool_debug
    bool_debug = not bool_debug

def main(tetronimoe):     #Oversees the part of the game where the block falls down
    global rotation,count_no_movement,difference,permission_down,paused,bool_faster
    boundary_list, blocks = tuple(get_lists())
    debug = False
    boundaries = tetronimoe.set_boundaries()
    n = 0
    while True:
        draw_screen(screen)

        dictionary = {pygame.K_LESS:"tetronimoe.rotate(math.pi/-2)",pygame.K_GREATER:"tetronimoe.rotate(math.pi/2)",pygame.K_COMMA:"tetronimoe.rotate(math.pi/-2)",pygame.K_PERIOD:"tetronimoe.rotate(math.pi/2)",pygame.K_LEFT:"left(tetronimoe)",pygame.K_RIGHT: "right(tetronimoe)",pygame.K_p:"pause()",pygame.K_DOWN:"faster()",pygame.K_ESCAPE:"return True",pygame.K_d:"debug()"}  #A dictionary of functions
        for event in pygame.event.get():
            if event.type == 3:
                if event.key in dictionary:
                    eval(dictionary[event.key])
                    break

        if rotation:
            boundaries = tetronimoe.set_boundaries()
            rotation = False  #resetting the rotation flag
            
        tetronimoe.draw()
        pygame.display.flip()
        
        if (n % 2 == 0):
            if permission_down and not(paused):
                tetronimoe.move((0,5))
                add_diff((0,5))
            elif paused:
                pass  #To prevent the else statement from being executed, otherwise program would stop instead of pause
            else:
                count_no_movement += 1

        if not paused:
            reset_permissions()
            
        for block_boundary in boundaries:
            block_boundary.update(difference)
            for bboundary in boundary_list:    
                if bboundary.check_boundary(block_boundary):
                    bboundary.direction(tetronimoe.main_block)  #this method also sets the permissions
                        
        difference = [0,0]
          
        
        
        if count_no_movement >= 3:              
            bool_faster = False
            boundary_list += tetronimoe.set_boundaries()
            blocks += tetronimoe.list_of_blocks
            reset_permissions()
            count_no_movement = 0
            return tetronimoe.list_of_blocks
        if bool_faster:
            pygame.time.wait(5)
        else:
            pygame.time.wait(waiting_time)

        set_lists(boundary_list,blocks)
        pygame.display.flip()
        n += 1

    
def get_permissions():
    global permission_left,permission_right,permission_down
    return [permission_left,permission_right,permission_down]

def set_permissions(left,right,down):
    global permission_left,permission_right,permission_down
    permission_left,permission_right,permission_down = left,right,down
    
def get_rotation():
    global rotation
    return rotation
def set_rotation(new_value):
    global rotation
    rotation = new_value
    

