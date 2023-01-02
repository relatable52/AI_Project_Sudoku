import time
import solver
import csv

def collectBacktracking(dataset):
    rows = list()
    fieldnames = ['No.', 'Puzzle', 'Solution', 'Solve time in seconds']
    filename = '..\\collected_data\\backtracking_' + dataset[:-4] + '.csv'
    num = 0

    with open('..\\dataset\\' + dataset, 'r') as data:
        row = data.readline()
        while len(row) > 1:
            grid = solver.inputSudoku(puzzle_string=row)
            start = time.perf_counter()
            sol = solver.solveBacktracking(grid=grid)
            sol_time = time.perf_counter() - start
            sol_string = solver.grid2string(grid=sol)
            num += 1
            tem = [num, row.rstrip() + '\'', sol_string + '\'', sol_time]
            rows.append(tem)
            row = data.readline()

    with open(filename, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(rows)

def collectConstraintPropagation(dataset):
    rows = list()
    fieldnames = ['No.', 'Puzzle', 'Solution', 'Solve time in seconds']
    filename = '..\\collected_data\\constraintpropagation_' + dataset[:-4] + '.csv'
    num = 0

    with open('..\\dataset\\' + dataset, 'r') as data:
        row = data.readline()
        while len(row) > 1:
            grid = solver.inputSudoku(puzzle_string=row)
            start = time.perf_counter()
            sol = solver.solveConstraintPropagation(grid=grid)
            sol_time = time.perf_counter() - start
            sol_string = solver.grid2string(grid=sol)
            num += 1
            tem = [num, row.rstrip() + '\'', sol_string + '\'', sol_time]
            rows.append(tem)
            row = data.readline()

    with open(filename, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(rows)

def collectSimulatedAnnealing(dataset, temp=0.5, alpha=0.99999):
    rows = list()
    fieldnames = ['No.', 'Puzzle', 'Solution', 'Solve time in seconds']
    filename = '..\\collected_data\\simulatedannealing_' + dataset[:-4] + '.csv'
    num = 0

    with open('..\\dataset\\' + dataset, 'r') as data:
        row = data.readline()
        while len(row) > 1:
            grid = solver.inputSudoku(puzzle_string=row)
            start = time.perf_counter()
            sol = solver.solveSimulatedAnnealing(grid=grid, temp=temp, alpha=alpha)
            sol_time = time.perf_counter() - start
            sol_string = solver.grid2string(grid=sol)
            num += 1
            tem = [num, row.rstrip() + '\'', sol_string + '\'', sol_time]
            rows.append(tem)
            row = data.readline()

    with open(filename, 'w+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        writer.writerows(rows)


    


