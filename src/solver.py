import copy
import random
import math

### Backtracking ###
def solveBacktracking(grid):
    # Function to check if a value is correct for a cell
    def checkCell(num, col, row):
        bloc_top = row - row%3
        bloc_left = col - col%3

        for i in range(9):
            if grid[i][col] == num or grid[row][i] == num:
                return False

        for i in range(3):
            for j in range(3):
                if grid[bloc_top+i][bloc_left+j] == num:
                    return False

        return True
    # Recursive function to solve sudoku using backtracking
    def walk(n):
        nonlocal sol
        if n == 81:
            sol = copy.deepcopy(grid)
        else:
            row = n // 9
            col = n % 9 
            if grid[row][col] != 0:
                walk(n+1)
            else:
                for i in range(1, 10):
                    if checkCell(row=row, col=col, num=i):
                        grid[row][col] = i
                        walk(n+1)
                        grid[row][col] = 0
                        
    sol = list()
    walk(0)          
    return sol

### Simulated Annealing ###
def getBloc(index): # return the position of the top left corner of the block that a cell is in
        bloc_top = (index//3)*3
        bloc_left = (index%3)*3
        return bloc_top, bloc_left

def initializeSolution(grid): # return a random initial solution for the simulated annealing algorithm
    
    def fillBlock(grid, index): # fill in the empty cell in a block with number 1-9
        bloc_top, bloc_left = getBloc(index)
        not_fill = list(i for i in range(1, 10))
        random.shuffle(not_fill)

        for i in range(3):
            for j in range(3):
                if grid[bloc_top+i][bloc_left+j] != 0:
                    not_fill.remove(grid[bloc_top+i][bloc_left+j])

        for i in range(3):
            for j in range(3):
                if grid[bloc_top+i][bloc_left+j] == 0:
                   grid[bloc_top+i][bloc_left+j] = not_fill[-1]
                   not_fill.pop() 
        
    def initSol(grid): # fill in all the blocks
        for i in range(9):
            fillBlock(grid=grid, index=i)
    
    sol = copy.deepcopy(grid)
    initSol(sol)
    return sol

def randomNeighbor(cur, grid):
    temp = copy.deepcopy(cur)
    def getPair():
        def getNotfill(bloc_index):
            not_fill = []
            bloc_top, bloc_left = getBloc(bloc_index)
            for i in range(3):
                for j in range(3):
                    if grid[bloc_top+i][bloc_left+j] == 0:
                        not_fill.append([bloc_top+i, bloc_left+j])
            return not_fill

        bloc_index = random.randint(0,8)
        not_fill = getNotfill(bloc_index=bloc_index)
        while(len(not_fill)<2):
            bloc_index = (bloc_index+1)%9
            not_fill = getNotfill(bloc_index=bloc_index)

        p = random.sample(not_fill, 2)    
        p1 = p[0]
        p2 = p[1]
        return p1, p2

    p1, p2 = getPair()
    temp[p1[0]][p1[1]], temp[p2[0]][p2[1]] = temp[p2[0]][p2[1]], temp[p1[0]][p1[1]]

    return temp

def getPoint(grid):
    conflicts = 0
    
    for i in range(9):
        row = []
        col = []
        for j in range(9):
            col.append(grid[j][i])
            row.append(grid[i][j])
        conflicts += len(set(col)) - 9
        conflicts += len(set(row)) - 9
    
    return conflicts

def solveSimulatedAnnealing(grid, temp=0.5, alpha=0.99999):
    cur_sol = initializeSolution(grid=grid)
    t = temp
    a = alpha
    while True:
        point = getPoint(cur_sol) # Return current solution if solved
        if point == 0:
            return cur_sol
        else:
            t *= a

            if t < 0.1:
                t = temp

            next_sol = randomNeighbor(grid=grid, cur=cur_sol)
            delta = getPoint(next_sol) - point
    
            if delta >= 0:
                cur_sol = next_sol
            elif random.random() < math.exp(delta/t):
                cur_sol = next_sol

def solveSimulatedAnnealingPlot(grid, pointlist, temp=0.5, alpha=0.99999):
    cur_sol = initializeSolution(grid=grid)
    t = temp
    a = alpha
    while True:
        point = getPoint(cur_sol) # Return current solution if solved
        pointlist.append(point)
        if point == 0:
            return cur_sol
        else:
            t *= a

            if t < 0.1:
                t = temp

            next_sol = randomNeighbor(grid=grid, cur=cur_sol)
            delta = getPoint(next_sol) - point
    
            if delta >= 0:
                cur_sol = next_sol
            elif random.random() < math.exp(delta/t):
                cur_sol = next_sol         

#### Constraint propagation ### 
def initDomain(grid):
    domain = list()
    for i in range(9):
        temp = list()
        for j in range(9):
            if grid[i][j] != 0:
                temp.append([grid[i][j]])
            else:
                temp.append(list(i for i in range(1, 10)))
        domain.append(temp)

    return domain

def removeValue(domain, col, row):
    if len(domain[row][col]) == 1:
        num = domain[row][col][0]
        bloc_top = row - row%3
        bloc_left = col - col%3
        # remove num from col and row
        for i in range(9):
            if num in domain[i][col] and i != row:
                domain[i][col].remove(num)
            if num in domain[row][i] and i != col:
                domain[row][i].remove(num)
        # remove num from block
        for i in range(3):
            for j in range(3):
                if num in domain[bloc_top+i][bloc_left+j] and bloc_top+i != row and bloc_left+j != col:
                    domain[bloc_top+i][bloc_left+j].remove(num)

def uniqueRow(col, row, domain, num):
    for i in range(9):
        if (num in domain[row][i]) and i != col:
            return False
    return True

def uniqueCol(col, row, domain, num):
    for i in range(9):
        if (num in domain[i][col]) and i != row:
            return False

    return True

def uniqueBloc(col, row, domain, num):
    bloc_top = row - row%3
    bloc_left = col - col%3
    for i in range(3):
        for j in range(3):
            if num in domain[bloc_top+i][bloc_left+j] and (bloc_top+i != row or bloc_left+j != col):
                return False
    return True


def checkUnit(domain, col, row, num):
    res = (uniqueBloc(col=col, row=row, domain=domain, num=num) or uniqueCol(col=col, row=row, domain=domain, num=num)) or uniqueRow(col=col, row=row, domain=domain, num=num)
    return res
            

def placeValue(domain, col, row):
    if len(domain[row][col]) > 1:
        for num in domain[row][col]:
            if checkUnit(domain=domain, col=col, row=row, num=num):
                domain[row][col] = [num]
                break

def checkSolved(domain):
    for i in range(9):
        for j in range(9):
            if len(domain[i][j]) > 1:
                return False
    return True

def solveConstraintPropagation(grid):
    def countDomain(domain):
        count = 0
        for i in range(9):
            for j in range(9):
                count += len(domain[i][j])
        return count

    def checkCell(num, col, row):
        bloc_top = row - row%3
        bloc_left = col - col%3

        for i in range(9):
            if grid[i][col] == num or grid[row][i] == num:
                return False

        for i in range(3):
            for j in range(3):
                if grid[bloc_top+i][bloc_left+j] == num:
                    return False

        return True

    def walk(n):
        nonlocal sol
        if n == 81:
            sol = copy.deepcopy(grid)
        else:
            row = n // 9
            col = n % 9 
            if grid[row][col] != 0:
                walk(n+1)
            else:
                for i in domain[row][col]:
                    if checkCell(row=row, col=col, num=i):
                        grid[row][col] = i
                        walk(n+1)
                        grid[row][col] = 0

    domain = initDomain(grid=grid)
    sol = list()
    cur_count = countDomain(domain=domain)
    pre_count = 0

    while True:
        if cur_count == 81:
            break
        if cur_count == pre_count:
            break
        pre_count = cur_count
        for i in range(9):
            for j in range(9):
                placeValue(domain=domain, col=j, row=i)
                removeValue(domain=domain, col=j, row=i)
        
        cur_count = countDomain(domain=domain)
    
    walk(0)
    return sol

# Utilities function to input sudoku puzzle
def inputSudoku(puzzle_string):
    index = lambda i, j: i*9 + j
    grid = list(list(int(puzzle_string[index(i, j)]) for j in range(9)) for i in range(9))
    return grid

# Ultiliets function to transform a sudoku grid to a string
def grid2string(grid):
    string = ''.join(list(''.join(list(str(grid[i][j]) for j in range(9))) for i in range(9)))
    return string

# Utilities function to print sudoku board        
def printGrid(grid):
    for row in range(9):
        if row == 0:
            print('╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗')
        elif row%3 == 0:
            print('╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣')
        else:
            print('╟───┼───┼───╫───┼───┼───╫───┼───┼───╢')
        res = '║'
        for col in range(9):
            f = lambda x: ' ' if x==0 else str(x)
            res = res + ' ' + f(grid[row][col]) + ' '
            if col%3 == 2:
                res = res + '║'
            else:
                res = res + '│'
        print(res)
    print('╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝')






                



