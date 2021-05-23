import pycosat

# To create the variable boolean number for a given cell and number
# Since boolean, not numerical, we need to create a variable for each
# cell and its 9 possible values.
# I understood this with: https://nickp.svbtle.com/sudoku-satsolver
def determine_var(i, j, k):
    return i*81 + j*9 + k+1

# Confused how this works.
# Also learnt from https://nickp.svbtle.com/sudoku-satsolver.
def inverse_var(v):
    v, k = divmod(v-1, 9)
    v, j = divmod(v, 9)
    v, i = divmod(v, 9)
    return i, j, k

## Makes sure that a cell can only have one number true at a time
def make_sure_only_one(variables):
    clauses = [variables]
    for i in range(len(variables)):
        for j in range(i+1, len(variables)):
            first = variables[i]
            second = variables[j]
            clauses.append([-first, -second])
    return clauses

if __name__ == '__main__':
    puzzle = [list(input()) for _ in range(9)]

    clauses = []

    for i in range(9):
        for s in range(9):
            clauses += make_sure_only_one([determine_var(i, j, s) for j in range(9)])
            clauses += make_sure_only_one([determine_var(j, i, s) for j in range(9)])
            clauses += make_sure_only_one([determine_var(i, s, j) for j in range(9)])

    # Sub-matrix constraints
    for k in range(9):
        for box_column in range(3):
            for box_row in range(3):
                box_clause = [determine_var(box_row * 3 + i, box_column * 3 + j, k) for i in range(3) for j in range(3)]
                clauses += make_sure_only_one(box_clause)


    # Now we add the actual sudoku as clauses, saving each value as an independent boolean that must be true.
    # E.g if (0, 0) is 8, then we add determine_var(0, 0, 8) to clauses.
    for row in range(9):
        for cell in range(9):
            if puzzle[row][cell] != '*':
                clauses += [[determine_var(row, cell, int(puzzle[row][cell]) - 1)]]

    solution = pycosat.solve(clauses)
    if isinstance(solution, str):
        print(-1)
    else:
        # Convert the variables back to their i, j and k values
        solution_variables = [inverse_var(variable) for variable in solution if variable > 0]
        # Order solution tuples in terms of their i an j values (aka h[0] and h[1]
        for i, cell in enumerate(sorted(solution_variables, key=lambda h: h[0] * 81 + h[1] * 9)):
            print(cell[2] + 1, end="")
            ## Every 9th value, print a new line
            if (i + 1) % 9 == 0: print()
