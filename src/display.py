import matplotlib.pyplot as plt
import numpy as np

def generateLinesCoords():
    x = list()
    y = list()
    xb = list()
    yb = list()
    # A helper function
    def helper(a, b, n):
        for i in range(0, 10, n):
            a.append(i)
            a.append(i)
            b.append(0)
            b.append(9)
            a.append(None)
            b.append(None)
    # Horizontal lines
    helper(a=x, b=y, n=1)
    helper(a=xb, b=yb, n=3)
    # Vertical lines
    helper(a=y, b=x, n=1)
    helper(a=yb, b=xb, n=3)

    return x, y, xb, yb

def configPlot(ax, title): # A function to draw sudoku board
    x, y, xb, yb = generateLinesCoords() # Coordinates to draw sudoku board
    ax.set_title(title , color='black', alpha=1) # Set plot's title
    ax.tick_params(top=False, bottom=False, right=False, left=False) # Turn off ticks
    # Remove axes
    ax.spines.top.set_visible(False)
    ax.spines.bottom.set_visible(False)
    ax.spines.right.set_visible(False)
    ax.spines.left.set_visible(False)
    # Set axes' range
    ax.set_ylim([-0.2, 9.2])
    ax.set_xlim([-0.2, 9.2])
    # Set row and col label
    plt.sca(ax)
    plt.yticks(np.arange(0.5, 9.5, 1), np.arange(1, 10, 1), color='black')
    plt.xticks(np.arange(0.5, 9.5, 1), 'ABCDEFGHI', color='black')
    # Plot sudoku board
    ax.plot(x, y, color='black')
    ax.plot(xb, yb, linewidth=3, color='black')

def fillCell(col, row, color, ax, sol): # Write number in a cell
    ax.text(
        col+0.5, (8-row)+0.5,
        sol[row][col],
        horizontalalignment='center',
        verticalalignment='center',
        color=color,
        fontsize=16
    )

def fillSolution(ax, grid, sol): # Fill sudoku puzzle
    for i in range(9):
        for j in range(9):
            if(grid[i][j] == 0):
                fillCell(col=j, row=i, color='orange', ax=ax, sol=sol)
            else:
                fillCell(col=j, row=i, color='blue', ax=ax, sol=sol)

def fillPuzzle(ax, grid):
    for i in range(9):
        for j in range(9):
            if(grid[i][j] != 0):
                fillCell(col=j, row=i, color='blue', ax=ax, sol=grid)

def solDisp(sol, grid):
    fig, ax = plt.subplots(figsize=(5, 5)) # Init plot object
    configPlot(ax=ax, title='Solution')
    fillSolution(ax=ax, grid=grid, sol=sol)
    plt.show()

def puzzleDisp(grid):
    fig, ax = plt.subplots(figsize=(5, 5))
    configPlot(ax=ax, title='Puzzle')
    fillPuzzle(ax=ax, grid=grid)
    plt.show()

def dispAll(grid, sol):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    configPlot(ax=ax1, title='Puzzle')
    configPlot(ax=ax2, title='Solution')
    fillPuzzle(ax=ax1, grid=grid)
    fillSolution(ax=ax2, grid=grid, sol=sol)
    plt.show()





    
