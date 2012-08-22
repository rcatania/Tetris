import math
import pygame
import math
from globals_and_constants import *
from game_controls import get_permissions, set_permissions, draw_screen

def add(vector1,vector2):
    return [vector1[0]+vector2[0],vector1[1]+vector2[1]]
def times(scalar, vector):
    return [vector[0]*scalar,vector[1]*scalar]

#Note, never name a variable the same as a class, or you will have a cryptic attribute error

class Block():
    def __init__(self, colour, position):
        self.colour = colour
        self.position = position
        self.boundaries = []
        self.midpoint = [position[0] + BLOCK_SIZE/2, position[1] + BLOCK_SIZE/2]

    def set_boundaries(self):  
        self.boundaries = []
        
        prev = self.position
        for n in range(0,5):  #Use sine and cos to set boundaries given starting position and no of sides of regular shape. Based on unit circle
            angle = 2*math.pi/4 * n
            addition = (math.cos(angle)*BLOCK_SIZE,math.sin(angle)*BLOCK_SIZE)
            new = [0,0]
            new[0] = prev[0] + addition[0]
            new[1] = prev[1] + addition[1]
            self.boundaries.append(Boundary(tuple(prev),tuple(new)))
            prev = new
   
    def draw(self):
        global black,white,BLOCK_SIZE,red
        new_colour = []
        for n in self.colour:
            if n > 45:
                new_colour.append(n-45)
            else:
                new_colour.append(n)
        new_colour = tuple(new_colour)
        pygame.draw.rect(screen,new_colour,(self.position[0],self.position[1],BLOCK_SIZE,BLOCK_SIZE),0)
        pygame.draw.rect(screen,self.colour,(self.position[0]+BLOCK_SIZE/6,self.position[1]+BLOCK_SIZE/6, BLOCK_SIZE * 2/3,BLOCK_SIZE * 2/3))
        
        #pygame.draw.circle(screen,pygame.Color("pink"),self.midpoint,2)  #For debuggin purposes
        #for boundary in self.boundaries:
        #    pygame.draw.line(screen,pygame.Color("black"),boundary.startpos,boundary.endpos)
    def move(self,offset):
        self.position = list(self.position)
        self.position = add(self.position,offset)
        self.midpoint = add(self.midpoint,offset)

    def __str__(self):
        print self.position

        
class Boundary(): #Note: since motion is discrete, these only check that the object touches the boundary
    def __init__(self,startpos, endpos):
        if round(startpos[1],1) == round(endpos[1],1): #y-value is constant
            self.vertical = False   #Note that vertical is valued as false is crucial to the check_boundary function.  False corresponds to the 0th place of the coord. while
        elif round(startpos[0],1) == round(endpos[0],1):  #...True corresponds to the 1st place of the coord.
            self.vertical = True
        else:
            
            raise ValueError        #Note the round() function had to be used because of floating roint number inaccuricies where for example 30 is not equal to 30.00000004

        
        self.startpos = list(startpos)
        self.endpos = list(endpos)
        self.length = math.sqrt((startpos[0]-endpos[0])**2 + (startpos[1] - endpos[1])**2) 
 
            
    def check_boundary(self,other_boundary):
        if self.vertical != other_boundary.vertical:
            return False
        if other_boundary.length > self.length:  #To ensure that self's is always greater (or equal) to the other boundary
            return other_boundary.check_boundary(self)
        vertical = other_boundary.vertical  #Check oomment in __init__ method

        if self.startpos[not vertical] == other_boundary.startpos[not vertical]:   #Since the (not vertical) coord is constant
            edge1 = self.startpos[vertical]
            edge2 = self.endpos[vertical]
        
            assert edge1 != edge2
        
            if (edge1 >edge2):  #To make sure the next if statement works correctly.This is needed because the set_boundary() method is based on the unit circle
                #=> it moves anticlockwise => boundaries are in opposite directions
                #In other parts of the program, boundaries must be facing from left to right or upwards                
                edge1, edge2 = edge2, edge1
            edge1,edge2 = round(edge1,0),round(edge2,0)

            if ( (edge1 < round(other_boundary.startpos[vertical],0) < edge2) or ( edge1 < round(other_boundary.endpos[vertical],0) < edge2) ):
          #Note: everything is rounded due to problems with floating point numbers
                    return True
            elif ((edge1 == round(other_boundary.startpos[vertical],0)) and (edge2 == round(other_boundary.endpos[vertical],0))) or((edge1 == other_boundary.endpos[vertical]) and (edge2 == other_boundary.startpos[vertical])):  
            #The OR is implemented for reasons mentioned above.
                return True                    
            
        return False
    def direction(self,block):
        permission_left,permission_right,permission_down = tuple(get_permissions())
        if self.vertical:
            if self.startpos[0] < block.midpoint[0]:
                permission_left = False
            else:
                permission_right = False
        elif self.startpos[1] > block.midpoint[1]:             
                permission_down = False
        set_permissions(permission_left,permission_right,permission_down)

    def update(self, difference):     
        self.startpos[0] += difference[0]
        self.startpos[1] += difference[1]
        self.endpos[0] += difference[0]
        self.endpos[1]  += difference[1]
        
    def equal(self,boundary2):  # is equal.  Not to be confused with __eq__.  Not used anywhere in code but may be used later on
        def compare(positions_tuple):
            pos1,pos2 = positions_tuple[0], positions_tuple[1]
            if (round(pos1[0],1) == round(pos2[0],1) )and ( round(pos1[1],1) == round(pos2[1],1)):
                return True
            
        tuples = [(self.startpos, boundary2.startpos),(self.endpos, boundary2.endpos), (self.startpos, boundary2.endpos), (self.endpos, boundary2.startpos)]
        if (compare(tuples[0]) and compare(tuples[1])) or  (compare(tuples[2]) and compare(tuples[3])):  #All the posibilities for the two boundaries to be equal
            return True
        else:
            return False
 


class Grid():
    def __init__(self):
        self.level_list = []  #Level refers to height, as in storey
        for n in range(0,15): 
            self.level_list.append(0)
    def update(self):
        block_list = get_lists()[1]
        self.level_list = []
        max_level = 0
        for n in range(0,15): 
            self.level_list.append(0)
        for blokk in block_list:
            level = int(15-(blokk.midpoint[1] - 15)/30) #Midpoint is used as the position attribute of a block would pose problems when rotated. 
            #15 is subtracted from blokk.midpoint as it is half of the BLOCK_SIZE -  This makes the highest blokk touch the upper edge of the screen
            #This is divided by 30, the BLOCK_SIZE.  There is "15 -" since this is the number of levels there are
            self.level_list[level-1] += 1
            if level > max_level:
                max_level = level
        return max_level
    def check_levels_full(self):
        global screen
        boundary_list, blocks = tuple(get_lists())
        full_levels = []
        full_levels.sort()  #So that the lower levels are deleted first
        
        for n  in range(0,15):
            if self.level_list[n] >= 10:
                full_levels.append(n)
        if not(full_levels):
            return None

        delete_level_animation(full_levels)       
        def move_levels(full_level_list):
            level = full_level_list[0]
            blokk_count = 0
            while blokk_count < 10:
                for blokk in blocks:
                    if int(blokk.midpoint[1]) == (29*15)-30*(level):#Use of algebra from the definition of level above
                        boundaries_found = 0
                        while boundaries_found <= 4:  #For some reason the program manages to find 5 boundaries for each block, despite it having 4 sides
                            for boundary1 in blokk.boundaries:                        
                                if boundary1 in boundary_list:
                                    del boundary_list[boundary_list.index(boundary1)]
                                    boundaries_found += 1
                                    break
                        del blocks[blocks.index(blokk)]
                        blokk_count += 1
                        print blokk_count
                        break

        
            for blokk in blocks:
                if int(blokk.midpoint[1]) < (29*15)-30*(level):              
                    blokk.move((0,30))
                    for boundary in blokk.boundaries:
                        boundary.update((0,BLOCK_SIZE))
            if len(full_level_list) > 1:
                full_level_list = full_level_list[1:]
                for lvl in enumerate(full_level_list):
                    full_level_list[lvl[0]] -= 1      #Since blocks are brought down a level
                return move_levels(full_level_list)
            
        move_levels(full_levels)
        
        draw_screen(screen)
        pygame.display.flip()
        set_lists(boundary_list,blocks)
            
def delete_level_animation(levels):
    s = pygame.Surface((300,30))
    for n in range(0,60):
        s.set_alpha(n)
        s.fill(pygame.Color("white"))
        for level in levels:           
            screen.blit(s,(25,420-(level*30)))
        pygame.display.flip()
        pygame.time.wait(25)
        

