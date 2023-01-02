import solver

grid = solver.inputSudoku('306508400520000000087000031003010080900863005050090600130000250000000074005206300')
sol = solver.solveBacktracking(grid=grid)

print('Puzzle:')
solver.printGrid(grid)
print('Solution:')
solver.printGrid(sol)



