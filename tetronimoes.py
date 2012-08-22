from utilities import Block, Boundary, add, times
import math
import pygame
from globals_and_constants import *
from game_controls import set_rotation

class tetrominoes():  #these methods mirror the block methods
    # Note: spelling
    def draw(self):
        for block in self.list_of_blocks:
            block.draw()
    def set_boundaries(self):
        boundaries = []
        for blockk in self.list_of_blocks:
            blockk.set_boundaries()
            boundaries += blockk.boundaries
            
        return boundaries
    def move(self,offset):
        for blk in self.list_of_blocks:
            blk.move(offset)
    def rotate(self,angle):   #Remove angles and trigonometric identities to make tetronimoes more smooth
        set_rotation(True)
         #To tell the program that the tetronimoe has been rotated and so it should update the boundaries
        origin = self.main_block.position
        origin = times(-1,origin)  #to be able to subtract later on
        for blockk in self.list_of_blocks:
            pos = (add(blockk.position,origin))
            pos[0], pos[1] = pos[0]*math.cos(angle) - pos[1]*math.sin(angle), pos[1]*math.cos(angle) + pos[0]*math.sin(angle)
            pos[0], pos[1] = round(pos[0],0) , round(pos[1],0)
            pos = add(pos,times(-1,origin))  #Add the origin again

            origin2 = times(-1,self.main_block.midpoint)
            midpoint = (add(blockk.midpoint,origin2))
            midpoint[0],midpoint[1] = midpoint[0]*math.cos(angle) - midpoint[1]*math.sin(angle), midpoint[1]*math.cos(angle) + midpoint[0]*math.sin(angle)
            midpoint[0], midpoint[1] = round(midpoint[0],0), round(midpoint[1],0)
            midpoint = add(midpoint, times(-1,origin2))
            
            blockk.position = pos
            blockk.midpoint = midpoint

        minmax_move = 0   #THe remaining part of this method makes sure that no part of the tetrominoe gets outside the boundaries when rotated
        minmax_vert = 0
        down = 0
        move = 0
        for blokk in self.list_of_blocks:
            if blokk.midpoint[0] < EDGES:
                print "left"
                move = abs(EDGES-blokk.midpoint[0]+BLOCK_SIZE/2)
                if move > minmax_move:
                    minmax_move = move
            elif ((EDGES+BLOCK_SIZE*10) < blokk.midpoint[0]):
                print "right"
                move = (blokk.midpoint[0])-(BLOCK_SIZE*9.5+EDGES) 
                move *=  -1

                if move < minmax_move:
                    minmax_move = move
            if (blokk.midpoint[1] > BLOCK_SIZE*15):
                move = (blokk.midpoint[1] - BLOCK_SIZE*15)
                move *= -1
                if move < down:
                    down = move
        if minmax_move != 0:
            print minmax_move
            for blokk in self.list_of_blocks:
                blokk.move((minmax_move,down))
class O(tetrominoes):
    def __init__(self,pos):
        self.colour = pygame.Color("yellow")
        
        self.main_block = Block(self.colour,pos)  #Not worth it to set up a parent constructor
        
        self.blk1 = Block(self.colour, (self.main_block.position[0]+BLOCK_SIZE, self.main_block.position[1]))
        self.blk2 = Block(self.colour, (self.main_block.position[0], self.main_block.position[1]+BLOCK_SIZE))
        self.blk3 = Block(self.colour, (self.main_block.position[0]+BLOCK_SIZE, self.main_block.position[1]+BLOCK_SIZE))
        self.list_of_blocks = [self.main_block,self.blk1,self.blk2,self.blk3]

    def rotate(self,angle):
        pass  #Since it has rotational symmetry, it makes no sense to rotate 
    
    def __str__():
        return "O"

class I(tetrominoes):
    def __init__(self,pos):
        self.colour = pygame.Color(0,255,255,0)

        self.main_block = Block(self.colour,pos)
        
        self.blk1 = Block(self.colour, (self.main_block.position[0]+BLOCK_SIZE*1, self.main_block.position[1]))
        self.blk2 = Block(self.colour, (self.main_block.position[0]+BLOCK_SIZE*2, self.main_block.position[1]))
        self.blk3 = Block(self.colour, (self.main_block.position[0]+BLOCK_SIZE*3, self.main_block.position[1]))
        self.list_of_blocks = [self.main_block,self.blk1,self.blk2,self.blk3]

    def __str__():
        return "I"
    
class J(tetrominoes):
    def __init__(self,pos):
        self.colour = pygame.Color("blue")

        self.main_block = Block(self.colour,pos)
        self.list_of_blocks = [self.main_block]
        
        self.blk1 = Block(self.colour, (self.main_block.position[0], self.main_block.position[1]+BLOCK_SIZE))
        self.blk2 = Block(self.colour, (self.main_block.position[0]-BLOCK_SIZE, self.main_block.position[1]))
        self.blk3 = Block(self.colour, (self.main_block.position[0]-BLOCK_SIZE*2, self.main_block.position[1]))
        self.list_of_blocks = [self.main_block,self.blk1,self.blk2,self.blk3]
       
    def __str__():
        return "J"

class L(tetrominoes):
    def __init__(self,pos):
        self.colour = pygame.Color(255, 229, 180,0)

        self.main_block = Block(self.colour,pos)
  
        self.blk1 = Block(self.colour, (self.main_block.position[0], self.main_block.position[1]+BLOCK_SIZE))
        self.blk2 = Block(self.colour, (self.main_block.position[0]+BLOCK_SIZE, self.main_block.position[1]))
        self.blk3 = Block(self.colour, (self.main_block.position[0]+BLOCK_SIZE*2, self.main_block.position[1]))
        self.list_of_blocks = [self.main_block,self.blk1,self.blk2,self.blk3]

    def __str__():
        return "L"


class T(tetrominoes):
    def __init__(self,pos):
        self.colour = pygame.Color("purple")
        
        self.main_block = Block(self.colour,pos)
             
        self.blk1 = Block(self.colour, (self.main_block.position[0], self.main_block.position[1]+BLOCK_SIZE))
        self.blk2 = Block(self.colour, (self.main_block.position[0]-BLOCK_SIZE, self.main_block.position[1]))
        self.blk3 = Block(self.colour, (self.main_block.position[0], self.main_block.position[1]-BLOCK_SIZE))
        self.list_of_blocks = [self.main_block,self.blk1,self.blk2,self.blk3]
        
    def __str__():
        return "T"

class S(tetrominoes):
    def __init__(self,pos):
        self.colour = pygame.Color("green")
        
        self.main_block = Block(self.colour,pos)
             
        self.blk1 = Block(self.colour, (self.main_block.position[0]-BLOCK_SIZE, self.main_block.position[1]))
        self.blk2 = Block(self.colour, (self.main_block.position[0], self.main_block.position[1]+BLOCK_SIZE))
        self.blk3 = Block(self.colour, (self.main_block.position[0]+BLOCK_SIZE, self.main_block.position[1]+BLOCK_SIZE))
        self.list_of_blocks = [self.main_block,self.blk1,self.blk2,self.blk3]
        
    def __str__():
        return "S"
    
class Z(tetrominoes):
    def __init__(self,pos):
        self.colour = pygame.Color("red")
        
        self.main_block = Block(self.colour,pos)
             
        self.blk1 = Block(self.colour, (self.main_block.position[0]+BLOCK_SIZE, self.main_block.position[1]))
        self.blk2 = Block(self.colour, (self.main_block.position[0], self.main_block.position[1]+BLOCK_SIZE))
        self.blk3 = Block(self.colour, (self.main_block.position[0]-BLOCK_SIZE, self.main_block.position[1]+BLOCK_SIZE))
        self.list_of_blocks = [self.main_block,self.blk1,self.blk2,self.blk3]
        
    def __str__():
        return "Z"
        
