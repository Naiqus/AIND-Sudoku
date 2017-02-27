assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """


    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    if values is False:
        return False ## Failed earlier
    for key, value in values.items():
        if len(value) != 2: # focus on value with length of two
            pass
        else:
            for unit in unitlist:
                if key in unit:
                    found_twin = False
                    # get a dict of units which contains the key, itself not included
                    boxes = {tmp_key: values[tmp_key] for tmp_key in unit if tmp_key != key}

                    for box, val in boxes.items():
                        if len(val) == 2 and val == value: # found twin
                            found_twin = True
                            twin = box

                    if found_twin:
                        del boxes[twin]  #remove the twin before remove the values
                        for box, val in boxes.items():
                            assign_value(values,box,values[box].replace(value[0],"").replace(value[1],""))
                    else:
                        pass
                else:
                    pass
    return values


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [r+c for r in A for c in B]


# from Utils
rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#solving the diagonal sudoku: add two diagonal units in the unitlist
diagonal_units = [ [rows[idx] + cols[idx] for idx in range(0, len(cols))],
                   [rows[idx] + cols[len(cols) - 1 - idx] for idx in range(0, len(cols))] ]
unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def grid_values(grid):
    raw_dict = {}
    for idx in range(0, len(grid)):
        raw_dict[boxes[idx]] = grid[idx] if grid[idx] != '.' else '123456789'
    return raw_dict


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    if values is False:
        return False ## Failed earlier
        print("False is returned")
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    for key, val in values.items():
        if len(val) == 1:
            for peer in peers[key]:
                assign_value(values,peer,values[peer].translate({ord(val): ''}))
            no_single_value_box = False
    return values


def only_choice(values):
    for key, value in values.items():
        if len(value) == 1:
            pass
        else:
            for unit in unitlist:
                if key in unit:
                    # construct the list of boxes and values in the unit, the box itself is excluded
                    boxes = {tmp_key: values[tmp_key] for tmp_key in unit if tmp_key != key}

                    for digit in value:
                        is_only_choice = True
                        for box, val in boxes.items():
                            if digit in val: is_only_choice = False
                        if is_only_choice == True: #It is the only choice
                            assign_value(values,key,digit)
    return values


def reduce_puzzle(values):
    if values is False:
        return False ## Failed earlier
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)

        values = naked_twins(values)

        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    values = reduce_puzzle(values)
    if values == False:
        return False

    solved = True
    for key, val in values:
        if len(val) > 1:
            solved = False
    if solved:
        return values
    else:
        min_box = "A1";
        min_size = 10
        for key, val in values:
            if len(val) < min_size and len(val) > 1:
                min_box = key
                min_size = len(val)

        for digit in values[min_box]:
            temp_values = values.copy()
            temp_values[min_box] = digit
            search(temp_values)



def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)

    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
