import pygame
import math
from utilities import Block, Boundary, Grid
from tetronimoes import *
import game_controls
from globals_and_constants import *
import random


floor = Boundary((EDGES,screen_size[1]-EDGES),(screen_size[0]-EDGES,screen_size[1]-EDGES)) #Note: unlike the others above, which are constants, this is a global variable
boundary_list.append(Boundary( (EDGES,screen_size[1]-EDGES),(EDGES,0) ))
boundary_list.append(Boundary((screen_size[0]-EDGES,screen_size[1]-EDGES),(screen_size[0]-EDGES,0)))
boundary_list.append(floor)

game_controls.draw_screen(screen)
pygame.display.flip()            

#Setting main boundaries at the edge of the screen
startpos = [85,-5]
tetrominoes = ["O","I","J","L","T","S","Z"]
grid = Grid()
while True: #Randomly chooses a tetrominoe and then passes it to the main method of the game_controls 
    blocks = get_lists()[1]
    index = random.randint(0,6)  
    letter = tetrominoes[index]
    string = [letter,"(",str(startpos),")"]
    string = ''.join(string)
    argument = eval(string)    
    game_controls.main(argument)  #Check that blocks and boundary_list are passed correctly around the program
    max_level = grid.update()
    grid.check_levels_full()
    if max_level >= 14:  #ensures it stops when blocks reach the top
        break

