"""
Merge function for 2048 game.
"""

def slide_list(line):
    """
    Slides all of the non-zero tiles slid over to the 
    beginning of the list with 
    the appropriate number of zeroes at 
    the end of the list
    """
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
    Function that merges a single row or column in 2048.
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
    

def run_tests():
    assert merge([2, 0, 2, 2]) == [4, 2, 0, 0]
    assert merge([2, 0, 2, 4]) == [4, 4, 0, 0]
    assert merge([0, 0, 2, 2]) == [4, 0, 0, 0]
    assert merge([2, 2, 0, 0]) == [4, 0, 0, 0]
    assert merge([2, 2, 2, 2, 2]) == [4, 4, 2, 0, 0]
    assert merge([8, 16, 16, 8]) == [8, 32, 8, 0]
    
    print "All tests pass!!!"
    
run_tests()
 
    
