"""
Clone of 2048 game.
"""

import poc_2048_gui
import random
import simpletest


# Directions for merging 
#(constants - should not be changed):
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4


# Offsets for computing tile indices 
# in each direction (constants - should not be changed):
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


# Helper function for merge:
def slide_list(line):
    '''
    Slides all of the non-zero tiles over to the 
    beginning of the list with 
    the appropriate number of zeroes at 
    the end of the list
    '''
    slided = []
    for num in line:
        if num != 0:
            slided.append(num)
    if len(slided) != len(line):
        for dummy_i in range(len(line) - len(slided)):
            slided.append(0)
    return slided


def merge(line):
    """
    Function that merges a single 
    row or column in 2048.
    """
    result = []
    slided = slide_list(line)
    index  = 0
    while index <= len(slided) - 1:
        if index == len(slided) - 1:
            result.append(slided[index])
            index += 1
        elif slided[index] != slided[index + 1]:
            if index == len(slided) - 2:
                result.append(slided[index])
                result.append(slided[index + 1])
            else:
                result.append(slided[index])
            index += 1
        else:
            result += (([slided[index] * 2]) + [0])
            index += 2
    if len(result) > len(slided):
        return slide_list(result[:-1])
    else:
        return slide_list(result)
    

    

class TwentyFortyEight:
    """
    Class to run the game logic.
    """
    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self.create_initials_cache()
        self.create_ranges_cache()
        
    
    def create_initials_cache(self, testing=False):
        '''
        Create a dictionary to quickly access the correct
        directional offsets.
        '''
        self._initials = {}
        self._initials[UP] = [(0, dummy_i) 
                          for dummy_i in range(self._grid_width)]
        self._initials[DOWN] = [(self._grid_height - 1, dummy_i) 
                            for dummy_i in range(self._grid_width)]
        self._initials[LEFT] = [(dummy_i, 0)
                            for dummy_i in range(self._grid_height)]
        self._initials[RIGHT] = [(dummy_i, self._grid_width - 1)
                             for dummy_i in range(self._grid_height)]
        if testing:
            return self._initials
        
    
    def create_ranges_cache(self, testing=False):
        '''
        Cache loop ranges for generating offsets in move function.
        '''
        self._loop_ranges = {UP: self._grid_height,
                       DOWN: self._grid_height,
                       LEFT: self._grid_width,
                       RIGHT: self._grid_width
                      }
        if testing:
            return self._loop_ranges
    
    
    def reset(self):
        """
        Reset the game so the grid is 
        empty except for two initial tiles.
        """
        # Create a rectangular grid using nested list comprehension 
        # Inner comprehension creates a single row
        self._grid = [[0 for dummy_col in range(self._grid_width)] 
                                 for dummy_row in range(self._grid_height)]
        
        for dummy_i in range(2):
            self.new_tile()
        
    
    def __str__(self):
        """
        Returns a string representation 
        of the grid for debugging.
        """
        return str(self._grid)

    
    def get_grid_height(self):
        """
        Returns the height of the board.
        """
        return self._grid_height

    
    def get_grid_width(self):
        """
        Returns the width of the board.
        """
        return self._grid_width

    
    def gen_offset_list(self, coord, offset, loop_range):
        '''
        Gets the list of correct offsettted values
        for a co-ordinate given an offset based
        on direction.
        '''
        offset_list = []
        this_coord = coord
        for dummy_in in range(loop_range):
            offset_list.append(this_coord)
            this_coord = tuple(map(lambda x, y: x + y, this_coord, offset))
        return offset_list
    
    
    def move(self, direction):
        """
        Moves all tiles in the given 
        direction and add a new tile 
        if any tiles moved.
        """
        before_move = str(self._grid)
        offset = OFFSETS[direction]
        init_coords = self._initials[direction]
      
        for init_coord in init_coords:
            offset_coords = self.gen_offset_list(init_coord, offset, self._loop_ranges[direction])
            temp_vals = [self._grid[offset_coord[0]][offset_coord[1]]
                        for offset_coord in offset_coords]
            merged_vals = merge(temp_vals)
            
            for index in range(len(merged_vals)):
                self._grid[offset_coords[index][0]][offset_coords[index][1]] = merged_vals[index]
            
        after_move = str(self._grid)
        if before_move != after_move:
            self.new_tile()
        
    
    def find_empty_coords(self):
        """
        Searches for and returns a random empty element.
        """
        try:
            for dummy_i in range((self._grid_height * self._grid_width)):
                random_row = random.choice(range(self._grid_height))
                random_col = random.choice(range(self._grid_width))
                random_sq = self._grid[random_row][random_col]
                if random_sq == 0:
                    return [random_row] + [random_col]
        except IndexError:
            return None
        
    
    def new_tile(self):
        """
        Creates a new tile in a randomly 
        selected empty square. The tile 
        will be 2 90% of the time 
        and 4 10% of the time.
        """
        random_empty_coords = self.find_empty_coords()
        if random_empty_coords:
            random_row = random_empty_coords[0]
            random_col = random_empty_coords[1]
        
            # Set value of random tile
            # Value is chosen from a list with the
            # didtribution specified above
            value_dist = ([2] * 90) + ([4] * 10) 
            self.set_tile(random_row, random_col, random.choice(value_dist))
        else:
            return "Game is over!!!"
        
    
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col 
        to have the given value.
        """
        self._grid[row][col] = value

    
    def get_tile(self, row, col):
        """
        Return the value of the tile 
        at position row, col.
        """
        return self._grid[row][col]


def run_test_suite():
    """
    Some informal tests
    """
    # Create a TestSuite object:
    suite = simpletest.TestSuite()
    
    # Testing slide_list and merge functions:
    suite.run_test(merge([2, 0, 2, 2]), [4, 2, 0, 0], "Test #1:")
    suite.run_test(merge([2, 0, 2, 4]), [4, 4, 0, 0], "Test #2:")
    suite.run_test(merge([0, 0, 2, 2]), [4, 0, 0, 0], "Test #3:")
    suite.run_test(merge([2, 2, 0, 0]), [4, 0, 0, 0], "Test #4:")
    suite.run_test(merge([2, 2, 2, 2, 2]) , [4, 4, 2, 0, 0], "Test #5:")
    suite.run_test(merge([8, 16, 16, 8]), [8, 32, 8, 0], "Test #6:")
    
    test_obj_one = TwentyFortyEight(4, 4)
    
    # Testing create_initials_cache and create_loop_ranges_cache methods:
    suite.run_test(test_obj_one.create_initials_cache(testing=True)[UP], 
                   [(0, 0), (0, 1), (0, 2), (0, 3)], "Test #7:")
    suite.run_test(test_obj_one.create_initials_cache(testing=True)[DOWN], 
                   [(3, 0), (3, 1), (3, 2), (3, 3)] , "Test #8:")
    suite.run_test(test_obj_one.create_initials_cache(testing=True)[RIGHT], 
                   [(0, 3), (1, 3), (2, 3), (3, 3)] , "Test #9:")
    suite.run_test(test_obj_one.create_initials_cache(testing=True)[LEFT], 
                   [(0, 0), (1, 0), (2, 0), (3, 0)], "Test #10:")
    suite.run_test(test_obj_one.create_ranges_cache(testing=True)[UP], 
                   4, "Test #11:")
    suite.run_test(test_obj_one.create_ranges_cache(testing=True)[DOWN], 
                   4, "Test #12:")
    suite.run_test(test_obj_one.create_ranges_cache(testing=True)[RIGHT], 
                   4, "Test #13:")
    suite.run_test(test_obj_one.create_ranges_cache(testing=True)[LEFT], 
                   4, "Test #14:")
        
    # Testing reset and new_tile methods:
    test_obj_one.reset()
    print test_obj_one.__str__()
        

    # Testing get_grid_height and get_grid_width:
    suite.run_test(test_obj_one.get_grid_height(), 
                   4, "Test #15:")
    suite.run_test(test_obj_one.get_grid_width(), 
                   4, "Test #16:")
    
    test_obj_two = TwentyFortyEight(5, 4)
    suite.run_test(test_obj_two.get_grid_height(), 
                   5, "Test #16:")
    suite.run_test(test_obj_two.get_grid_width(), 
                   4, "Test #17:")
    
    # Testing get_tile and set_tile methods:
    # (set to values that couldn't arise otherwise)
    test_obj_two.set_tile(4, 3, 10)
    suite.run_test(test_obj_two.get_tile(4, 3), 
                   10, "Test #18:")
    test_obj_two.set_tile(3, 3, 11)
    suite.run_test(test_obj_two.get_tile(3, 3), 
                   11, "Test #18:")

    # Collect and report results:
    suite.report_results()


# Run test suite:
run_test_suite()


# Run 2048 game:
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))