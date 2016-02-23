"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import grid
import queue
import zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
        
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie
            
            
    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
        
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        visited = grid.Grid(self.get_grid_height(), self.get_grid_width())
        distance_field = [[(self.get_grid_height() * self.get_grid_width()) 
                           for dummy_col in range(self.get_grid_width())] 
                          for dummy_row in range(self.get_grid_height())]
        
        boundary = queue.Queue()
        
        if entity_type == HUMAN:
            for human in self.humans():
                boundary.enqueue(human)
        else:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
        
        for entity in boundary:
            visited.set_full(entity[0], entity[1])
            distance_field[entity[0]][entity[1]] = 0 
        
        # Breadth First Search:
        while boundary:
            curr_cell = boundary.dequeue() # tuple of the form (row, col)
            neighbors = self.four_neighbors(curr_cell[0], curr_cell[1])
            for nbr in neighbors:
                if visited.is_empty(nbr[0], nbr[1]) and self.is_empty(nbr[0], nbr[1]):
                    visited.set_full(nbr[0], nbr[1])
                    boundary.enqueue(nbr)
                    curr_dist = distance_field[nbr[0]][nbr[1]]
                    distance_field[nbr[0]][nbr[1]] = min(curr_dist, \
                        distance_field[curr_cell[0]][curr_cell[1]] + 1)
        return distance_field
         
                
                    
                                            
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_human_list = []
        for human in self.humans():
            curr_row = human[0]
            curr_col = human[1]
            nbrs = self.eight_neighbors(curr_row, curr_col)
            curr_best_dist = zombie_distance_field[curr_row][curr_col]
            best_so_far = human
            for nbr in nbrs:
                if self.is_empty(nbr[0], nbr[1]):
                    if zombie_distance_field[nbr[0]][nbr[1]] > curr_best_dist:
                        curr_best_dist = zombie_distance_field[nbr[0]][nbr[1]]
                        best_so_far = nbr
                    
            # Move that human's position:
            new_human_list.append(best_so_far)
        
        # Update all positions:
        self._human_list = new_human_list
        
                 
            
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_zombie_list = []
        for zombie in self.zombies():
            curr_row = zombie[0]
            curr_col = zombie[1]
            nbrs = self.four_neighbors(curr_row, curr_col)
            curr_best_dist = human_distance_field[curr_row][curr_col]
            best_so_far = zombie
            for nbr in nbrs:
                if self.is_empty(nbr[0], nbr[1]):
                    if human_distance_field[nbr[0]][nbr[1]] < curr_best_dist:
                        curr_best_dist = human_distance_field[nbr[0]][nbr[1]]
                        best_so_far = nbr
            
            # Now move the zombie accordingly:
            new_zombie_list.append(best_so_far)
        
        # Update all positions:
        self._zombie_list = new_zombie_list

        
        
def run_tests():
    obj1 = Apocalypse(20, 30, [(4, 15), (5, 15), (6, 15), 
                              (7, 15), (8, 15), (9, 15), 
                              (10, 15), (11, 15), (12, 15), 
                              (13, 15), (14, 15), (15, 15), 
                              (15, 14), (15, 13), (15, 12), 
                              (15, 11), (15, 10)], [], [(18, 14), 
                              (18, 20), (14, 24), (7, 24), (2, 22)])
    
    assert obj1.compute_distance_field(HUMAN) == [[ 24,  23,  22,  21,  20,  19,  18,  17,  16,  15,  14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   3,   4,   5,   6,   7,   8,   9],
    [ 23,  22,  21,  20,  19,  18,  17,  16,  15,  14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   2,   3,   4,   5,   6,   7,   8],
    [ 22,  21,  20,  19,  18,  17,  16,  15,  14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   0,   1,   2,   3,   4,   5,   6,   7],
    [ 23,  22,  21,  20,  19,  18,  17,  16,  15,  14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   2,   3,   4,   5,   6,   7,   8],
    [ 24,  23,  22,  21,  20,  19,  18,  17,  16,  15,  14,  13,  12,  11,  10, 600,   8,   7,   6,   5,   4,   3,   2,   3,   3,   4,   5,   6,   7,   8],
    [ 25,  24,  23,  22,  21,  20,  19,  18,  17,  16,  15,  14,  13,  12,  11, 600,   9,   8,   7,   6,   5,   4,   3,   3,   2,   3,   4,   5,   6,   7],
    [ 26,  25,  24,  23,  22,  21,  20,  19,  18,  17,  16,  15,  14,  13,  12, 600,   9,   8,   7,   6,   5,   4,   3,   2,   1,   2,   3,   4,   5,   6],
    [ 25,  24,  23,  22,  21,  20,  19,  18,  17,  16,  17,  16,  15,  14,  13, 600,   8,   7,   6,   5,   4,   3,   2,   1,   0,   1,   2,   3,   4,   5],
    [ 24,  23,  22,  21,  20,  19,  18,  17,  16,  15,  16,  17,  16,  15,  14, 600,   9,   8,   7,   6,   5,   4,   3,   2,   1,   2,   3,   4,   5,   6],
    [ 23,  22,  21,  20,  19,  18,  17,  16,  15,  14,  15,  16,  17,  16,  15, 600,  10,   9,   8,   7,   6,   5,   4,   3,   2,   3,   4,   5,   6,   7],
    [ 22,  21,  20,  19,  18,  17,  16,  15,  14,  13,  14,  15,  16,  17,  16, 600,  10,  10,   9,   8,   7,   6,   5,   4,   3,   4,   5,   6,   7,   8],
    [ 21,  20,  19,  18,  17,  16,  15,  14,  13,  12,  13,  14,  15,  16,  17, 600,   9,  10,   9,   8,   7,   6,   5,   4,   3,   4,   5,   6,   7,   8],
    [ 20,  19,  18,  17,  16,  15,  14,  13,  12,  11,  12,  13,  14,  15,  16, 600,   8,   9,   8,   7,   6,   5,   4,   3,   2,   3,   4,   5,   6,   7],
    [ 19,  18,  17,  16,  15,  14,  13,  12,  11,  10,  11,  12,  13,  14,  15, 600,   7,   8,   7,   6,   5,   4,   3,   2,   1,   2,   3,   4,   5,   6],
    [ 18,  17,  16,  15,  14,  13,  12,  11,  10,   9,  10,  11,  12,  13,  14, 600,   6,   7,   6,   5,   4,   3,   2,   1,   0,   1,   2,   3,   4,   5],
    [ 17,  16,  15,  14,  13,  12,  11,  10,   9,   8, 600, 600, 600, 600, 600, 600,   5,   6,   5,   4,   3,   4,   3,   2,   1,   2,   3,   4,   5,   6],
    [ 16,  15,  14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   3,   4,   5,   4,   3,   2,   3,   4,   3,   2,   3,   4,   5,   6,   7],
    [ 15,  14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   2,   3,   4,   3,   2,   1,   2,   3,   4,   3,   4,   5,   6,   7,   8],
    [ 14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   0,   1,   2,   3,   2,   1,   0,   1,   2,   3,   4,   5,   6,   7,   8,   9],
    [ 15,  14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   2,   3,   4,   3,   2,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10]]
        
    obj2 = Apocalypse(20, 30, [(4, 15), (5, 15), (6, 15), 
                               (7, 15), (8, 15), (9, 15), 
                               (10, 15), (11, 15), (12, 15), 
                               (13, 15), (14, 15), (15, 15), 
                               (15, 14), (15, 13), (15, 12), 
                               (15, 11), (15, 10)], [(12, 12), 
                               (7, 12)], [])
    assert obj2.compute_distance_field(ZOMBIE) == [[ 19,  18,  17,  16,  15,  14,  13,  12,  11,  10,   9,   8,   7,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24],
    [ 18,  17,  16,  15,  14,  13,  12,  11,  10,   9,   8,   7,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23],
    [ 17,  16,  15,  14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22],
    [ 16,  15,  14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21],
    [ 15,  14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   4,   5, 600,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22],
    [ 14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   3,   4, 600,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23],
    [ 13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   2,   3, 600,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24],
    [ 12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   0,   1,   2, 600,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25],
    [ 13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   2,   3, 600,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26],
    [ 14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   3,   4, 600,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27],
    [ 14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   3,   4, 600,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28],
    [ 13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   2,   3, 600,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29],
    [ 12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   0,   1,   2, 600,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30],
    [ 13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   1,   2,   3, 600,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30],
    [ 14,  13,  12,  11,  10,   9,   8,   7,   6,   5,   4,   3,   2,   3,   4, 600,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29],
    [ 15,  14,  13,  12,  11,  10,   9,   8,   7,   6, 600, 600, 600, 600, 600, 600,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28],
    [ 16,  15,  14,  13,  12,  11,  10,   9,   8,   7,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27],
    [ 17,  16,  15,  14,  13,  12,  11,  10,   9,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28],
    [ 18,  17,  16,  15,  14,  13,  12,  11,  10,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29],
    [ 19,  18,  17,  16,  15,  14,  13,  12,  11,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30]]   

    print "Tests pass!!!"


run_tests()       
        
# Start up gui for simulation:
zombie_gui.run_gui(Apocalypse(30, 40))