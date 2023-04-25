import solver
import display

grid = solver.inputSudoku('000000000000003085001020000000507000004000100090000000500000073002010000000040009')
sol = solver.solveConstraintPropagation(grid=grid)

print('Puzzle:')
solver.printGrid(grid)
print('Solution:')
solver.printGrid(sol)
display.dispAll(grid, sol)





