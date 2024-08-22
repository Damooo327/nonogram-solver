#Solving a nonogram
"""
1. First, check which rows/columns values can be solved simply (all numbers + padding == width or height of the puzzle). You also determine the amount of space remaining by checking if the row/column has a X, and looking around those Xs.
2. Now, go through all the rows/columns, and find the one where the numbers + padding > lenght or width of the puzzle AND are empty.
3. Now of those rows/columns, do a simple filling from one direction. Now look at number of whitespace leftover, and subtract it from each string of Os from left to right
4. Now there are a couple of scenarios..
    a) SEGMENTING TWO STRING OF 0s.... First go through the rows with some elements, and check what happens if areas with 1 whitespace postioned with Os between them are connected. If the resulting string of Os is bigger than any of the numbers in the rows/ columns, 
    it means that they cannot be connected. Hence place a X there. Otherwise.... check if placing a O there still means that row/column can be solved and.....  
        
        a.a) and.... if so, check the lenght of that string of Os, and check for the amount of space remaining after that string of 0s. If the amount of space remaining means that the numbers preceding it can be done, then fill 
    
    b) SEGMENTING AREAS WITH Xs.... Now look for any rows/columns with Xs. Segment the spaces around it and count the number of spaces remaining in it,  and check what string of numbers can fit there and segment those as well. For each segment, if they are empty, perform step 1 and 2. Otherwise,  Check the number of Os after the X. Count all the remaining spots after the inital O. if the X is before the O, then count from bottom up, otherwise top bottom. 
    Count the number plus padding until the value > the number of spots left. If the thing which made it exceed it was padding, then EASILY SOLVE THE PORTION by using 1) and put X to end it. Otherwise extend the Os, until it fits the last number identified and add an X to the end of it.
    
    c) DEALING WITH SINGLE NUMBERS.... Look for rows/columns which only have 1 number AND have elements in it already. If there a more than 1 string of Os, then connect them. Afterwards, count from both sides of the string of Os, and remove any spaces with Xs which are not being utilized.
    If there is no space remaining in one side, add Os in the other direction until there is.
    
    d) COVER SPACES ANNWITH Xs IF THEY COT BE UTILIZED.... Look for rows/columns with atleast 1 X and look at the space around it. If the space left over around it is smaller than all of the numbers + padding in that direction, then cover it with Xs.
    e) PERFORM A COMPLETE CHECK.. Check if a row/column is done, if so fill remaining spaces with Xs.
"""
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


class nonogramEncoding:
    def __init__(self, dimensions, rows, cols):
        """
        dimensions: a tuple of (height, width) indicating nonogram size
        nonogram: a tuple of (row nums, col nums) containing 2 arrays containing the row and col of numbers
        """
        self.grid = np.zeros(dimensions, dtype=int)

        self.dimensions = dimensions
        self.rows = rows
        self.cols = cols
    
    def printGrid(self):

        rows, cols = self.dimensions[1], self.dimensions[0]
        square_size = 50  # Size of each square in pixels

        # Create an empty canvas (white background)
        canvas = np.ones((rows * square_size, cols * square_size, 3), dtype=np.uint8) * 255

        white = [255, 255, 255]  # white
        black = [0, 0, 0] # black
        red = [255, 0, 0] # red

        for i in range(rows):
            for j in range(cols):
                if self.grid[i][j] == 1:
                    canvas[i * square_size:(i + 1) * square_size, j * square_size:(j + 1) * square_size] = white
                elif self.grid[i][j] == 2:
                    canvas[i * square_size:(i + 1) * square_size, j * square_size:(j + 1) * square_size] = red
                else: 
                    canvas[i * square_size:(i + 1) * square_size, j * square_size:(j + 1) * square_size] = black

        plt.imshow(canvas)
        plt.axis('off')
        plt.show()
        
    
    def getWidth(self):
        return dimensions[1]
    
    def getHeight(self):
        return dimensions[0]


##hello = nonogramEncoding((40,20),10)
#hello.printGrid()

#print("hello world")