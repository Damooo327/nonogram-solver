from nonogram import nonogramEncoding
import numpy as np
import math

#################
# Master Function
#################

class nonogram_solver(nonogramEncoding):
    def __init__(self, dimensions, rows, cols):
        super().__init__(dimensions, rows, cols)
        self.rowStatus = []
        self.colStatus = []

    def nonogramSolve(self):

        ##########################################
        # Do a simple solve for all columns/rows 
        # which can be simple solved             
        ##########################################

        # Check which rows and cols can be solved normally
        self.rowStatus = np.array([self.checkSolvableRowCol(self.rows[i], self.dimensions[1], rowIndex=i) for i in range(len(self.rows))],dtype=str)


        # Solve rows which are SOLVABLE/SIMPLE SOLVABLE
        for index, row in enumerate(self.rowStatus):
            if row == "SIMPLE_SOLVE" or row == "SOLVABLE_EMPTY":
                #print(self.rows[index], index)
                self.fillSolvableRowCol(self.rows[index], np.index_exp[index,::])

        self.colStatus = np.array([self.checkSolvableRowCol(self.cols[j], self.dimensions[0], colIndex=j) for j in range(len(self.cols))],dtype=str)

        print(self.colStatus)
        
        # At this point, solve the ones which are solvable empty
        
        for index, col in enumerate(self.colStatus):
            if col == "SOLVABLE_EMPTY":
                #print(self.rows[index], index)
                self.fillSolvableRowCol(self.cols[index], np.index_exp[::, index])
        


        #################################################
        # Now run the solve Partially filled 
        # function torecursviely solve the entire puzzle
        #################################################

        # Now fill in all the partially filled ones

        '''

        sectionsToSolve = [] # an array of format [(number, indexSlice, solveType, specialCondition)], 
        # to denote how many more indexSlices are left to solvem, where solveType refers to the row/col solve type and specialCondition refers to whether that row/col is completely solved for the time being

        for index, col in enumerate(self.colStatus):
            if col == "SOLVABLE_PARTIAL_FILLED":
                print(self.cols[index], index)
                indexSlice = np.index_exp[:,index]
                sectionsToSolve.append((self.cols[index],indexSlice))

        #self.solvePartiallyFilled(sectionsToSolve)
        '''
        
        
        
    
    def solvePartiallyFilled(self, solveArray):
        """
        numbers: the list of numbers in format [x,x,x...]
        solveArray: an array of format [(number, indexSlice, solveType, specialCondition)] 

        This func assumes that row/col is UN/SOLVABLE_PARTIALLY_FILLED
        """


        # ----------------------------------------------
        # First identify what kinda of solve is required
        # ----------------------------------------------

        # NUMBERS == 1, meaning that that row/col only has 1 number
        # There exists a run of Os which satisfy 1 of the numbers in numbers
        # You can simply just remove some spaces with Xs as they won't be utilised
        # Nothing can be done, leave it alone

        specialCondition = solveArray[-1][3]
        indexSlice = solveArray[-1][1]
        numbers = solveArray[-1][0]
        solveType = solveArray[-1][2]
            
        
        if specialCondition == "UNREACHABLE_SPACES":
            args = {'arraySlice':self.grid[indexSlice], 'numbers':numbers}
            return self.removeUnreachableSpaces(**args)
        

        elif len(numbers) == 1:
            # numbers only contain 1 value
            if solveType == "SOLVABLE_PARTIAL_FILLED":
                self.fillSolvableRowCol(numbers, indexSlice=indexSlice)

                # Now remove the unreachabale spaces
                spaces = self.solvePartiallyFilled(numbers, indexSlice=indexSlice, solveType=solveType, specialCondition="UNREACHABLE_SPACES")
                self.grid[indexSlice] = spaces

                #At this point nothing more can be done to that row/column. Check to see if it is solved

            

            elif solveType == "UNSOLVABLE_PARTIAL_FILLED":
                print("enter code here")

        
    
        

            

        


        
        






    #################
    # Basic functions
    #################

    """
    def solveAndUpdateTypes(self, axis, conditions):

        if axis == "rows":
            self.rowStatus = np.array([self.checkSolvableRowCol(self.rows[i], self.dimensions[1], rowIndex=i) for i in range(len(self.rows))],dtype=str)
        elif axis == "cols":
            self.colStatus = np.array([self.checkSolvableRowCol(self.cols[j], self.dimensions[0], colIndex=j) for j in range(len(self.cols))],dtype=str)
        
        
        if len(conditions) != 0:
            if axis == "rows":
                for index, row in enumerate(self.rowStatus):
                    if row in conditions:
                        self.fillSolvableRowCol(self.rows[index], row=index)
            else:
                for index, col in enumerate(self.colStatus):
                    if col in conditions:
                        print(self.rows[index], index)
                        self.fillSolvableRowCol(self.cols[index], col=index)
    """


        


    # Fill a row/col which is SOLVABLE/SIMPLE SOLVE by doing a SIDE to SIDE fill and subtract
    def fillSolvableRowCol(self, numbers, indexSlice):
        """
        numbers: the array of numbers in format [x,x,x..] to represent list of runs to fill with
        indexSlice: the indexSlice of the self.grid. Formatted to either refer to a specific column or row. in the format np.index_exp
        rows= a val > -1 if filling a row, where the val represents the row to fill
        cols= a val > -1 if filling a col, where the val represents the col to fill
        """

    
        fillArea = np.zeros(len(self.grid[indexSlice]))

        spaceTaken = len(numbers)+sum(numbers)-1
        spaceLeft = len(fillArea) - spaceTaken

        fillStart = -1
        fillEnd = -1

        for number in numbers:
            if fillStart == -1:
                fillStart = 0
                fillEnd = number

                fillStart += spaceLeft
            else:
                fillStart = fillEnd+1
                fillEnd += number+1

                fillStart += spaceLeft

            fillArea[fillStart:fillEnd] = 1
        

        #Now put that array in the grid and update row/col status

        arrayAtIndex = np.copy(self.grid[indexSlice])
        self.grid[indexSlice] = np.logical_or(arrayAtIndex, fillArea)

        
        if isinstance(indexSlice[0], int):
            if spaceLeft == 0:
                self.rowStatus[indexSlice[0]] = "SOLVED_NOT_FILLED"
            else:
                self.rowStatus[indexSlice[0]] = "PARIAL_SOLVED_NOT_EMPTY"
        elif isinstance(indexSlice[1], int):
            if spaceLeft == 0:
                self.colStatus[indexSlice[1]] = "SOLVED_NOT_FILLED"
            else:
                self.colStatus[indexSlice[1]] = "PARIAL_SOLVED_NOT_EMPTY"
        
            



    # Check if a row/col can be filled and its return its solving type
    def checkSolvableRowCol(self, numbers, length, rowIndex=-1, colIndex=-1):
        """
        numbers: array of numbers for that row/col
        length: length of the row/col
        rowIndex: the row to look at in self.grid
        colIndex: the col to look at in self.grid
        """
        spaceTaken = 0
        for i in numbers:
            spaceTaken += 1 + i

        spaceTaken -= 1

        if rowIndex != -1:
            if 1 in self.grid[rowIndex]:
                isPartiallyFilled = True
            else:
                isPartiallyFilled = False
        elif colIndex != -1:
            if 1 in self.grid[:, colIndex]:
                isPartiallyFilled = True
            else:
                isPartiallyFilled = False


        #print(spaceTaken, length, numbers, rowIndex, colIndex)

        if spaceTaken == length:
            return "SIMPLE_SOLVE"
        elif spaceTaken > math.floor(length/2):
            # Potentiall solvable, check to see if the space remaining can be covered with a 
            # number if subracted from the left side
            if max(numbers) > (length-spaceTaken):
                if isPartiallyFilled:
                    return "SOLVABLE_PARTIAL_FILLED"
                else:
                    return "SOLVABLE_EMPTY"
            else:
                if isPartiallyFilled:
                    return "UNSOLVABLE_PARTIAL_FILLED"
                else:
                    return "UNSOLVE_EMPTY"
        elif len(numbers) == 1:
            return "UNSOLVE_EMPTY"
        else:
            # If it is unsolvable, but it is partially filled already
            if isPartiallyFilled:
                return "UNSOLVABLE_PARTIAL_FILLED"
            else:
                return "UNSOLVE_EMPTY"
        
    


    # Cover a row with Xs
    def coverWithXs(self, nonogram):
        nonogram[np.where(nonogram=='')] = "X"

    # Do a check to see if a row/col is done
def checkCompleteness(array, numbers):
    """
    self, indexSlice, numbers
    indexSlice: index slice in format np.index_exp denoting a particular row/col
    numbers: numbers in format [x,x,x,...] for that particular index row/col
    """

    index = 0
    #arrayAtIndex = self.grid[indexSlice]
    #filledSpaces = np.where(arrayAtIndex[index] == 1)
    filledSpaces = np.where(array == 1)[0]

    numberRun = 1   
    numberIndex = 0
    print(array, numbers, filledSpaces)

    for num in range(len(filledSpaces)-2,0,-1):
        if filledSpaces[num]+1 == filledSpaces[num+1] and numberRun == 0:
            numberRun += 1
        else:
            if numberRun == numbers[numberIndex]:
                if numberIndex+1 > len(filledSpaces):
                    return True
                else:
                    numberIndex += 1
                    numberRun = 0
            else:
                return False
            


    def removeUnreachableSpaces(self, arraySlice, numbers):

        """
        arraySlice: reference to the array
        numbers: list of numbers in format [x,x,x...]
        """

        #print(array, numbers)

        newArray = np.full(len(arraySlice), 2, dtype=int)
        oneIndices = []

        for i in range(1,len(arraySlice)):
            if (arraySlice[i] == 1 and arraySlice[i-1] == 0) or (arraySlice[i] == 0 and arraySlice[i-1] == 1):
                oneIndices.append(i)
        
        
        for j in range(len(numbers)):
            space = numbers[j] - (oneIndices[(j*2) +1] - oneIndices[(j*2)])
            oneIndices[(j*2)] -= space
            oneIndices[(j*2) +1] += space

            newArray[oneIndices[j*2]:oneIndices[(j*2) +1]] = 0
        
        
        copyOfArray = np.copy(arraySlice)

        print(copyOfArray, newArray)
        return newArray+copyOfArray
        


            

        

        

        





# Example code
cols = [[4,2],[6,1,1],[3,3,3],[2,3,1,1,1],[8,1],[6,3],[4,5],[4,5],[10],[9],[8,2],[6,3],[1,1,4,3],[2,3],[3,2]]


rows = [[3],
        [2],
        [3,3,1,1],
        [5,5],
        [3,9],
        [2,10],
        [2,10],
        [7,5],
        [2,2,5],
        [3,5],
        [1,5],
        [1,1,4,2,2],
        [3,3,5],
        [1,1,1,3],
        [2,1]]


exampleNonogram = nonogramEncoding((15,15), rows, cols)
hello = nonogram_solver((15,15), rows, cols)
hello.nonogramSolve()
hello.fillSolvableRowCol([7,3],8)
hello.printGrid()
#print(hello.grid)

#print(checkSolvableRowCol([7,5,1],15))

#hello.removeUreachableSpaces([0,0,0,0,1,1,1,1,0,0,0,0,1,0,0], [6,3])

#print(np.logical_or([1,0,1,1,1,1,1], [0,1,1,1,1,1,1]))


array = np.full((5,3), 10)
"""
#print(array)

pointer = array[1]

#print(pointer)
pointer[2] = 2

print(array)

condition = np.index_exp[::,2]
condition2 = np.index_exp[1,::]

print(array[condition])

print(condition)
print(condition2)

"""
"""
array = [1,2,3,4,5]

def daman(h):
    print(h)
    h.append(1029)

def daman2(h):
    h.append(501)

#daman(array)
daman2(array)
print(array)
"""

array2 = np.arange(15).reshape(5,3)

f = np.where(array[1] == 10)

print(f[0])

array = np.array([0,0,1,1,1,0,0,1,1,1,1,0,0,1,0])
numbers = [3,4,1]

print(checkCompleteness(array, numbers))


