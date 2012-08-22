import pygame

white = pygame.Color("white")
black = pygame.Color("black")
red = pygame.Color("red")

BLOCK_SIZE = 30  #Constants.  May give the user the option to adjust some of these.  Note these have common factors
EDGES = 25

screen_size = (BLOCK_SIZE*10 + 2*EDGES, BLOCK_SIZE*15 + EDGES)

pygame.init()
screen = pygame.display.set_mode((screen_size[0]+85,screen_size[1]), pygame.DOUBLEBUF, 32)  #Expansion of screen.  Cannot change screen size

boundary_list = []  #Global variables, needed everywhere
blocks = []

def set_lists(boundary_list1,blocks1):
    global boundary_list, blocks
    boundary_list = boundary_list1
    blocks = blocks1
    
def get_lists():
    return [boundary_list,blocks]
