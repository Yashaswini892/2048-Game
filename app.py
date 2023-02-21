from flask import Flask, request, render_template
from random import choice
from copy import deepcopy

app = Flask(__name__)

# Pass string ( which is used to encode the state of the game and pass it to the url) to convert it to list of lists
def string_grid(grid_string):
    # Intialize an empty list to store lists
    matrix = []
    # Split rows in the string by * character for example: 0 0 0 2*0 0 2 0*0 0 0 0*0 0 0 0
    rows = grid_string.split('*')
    # Iterate each element in a row and split the columns by space character
    for i in rows:
        columns = i.split(' ')
        matrix.append([int(j) for j in columns])
    return matrix
    	
# Pass a grid to convert it to a 2D matrix
"""[[0,0,0,2],
    [0,0,2,0],
    [0,0,0,0],
    [0,0,0,0]]"""
def grid_string(grid):
    # Create a grid_matrix to store lists of rows in 2D
    grid_matrix = []
    for row in grid:
        # Appending each list of grid as string into 2D
        grid_matrix .append(' '.join([str(i) for i in row]))
    return '*'.join(grid_matrix)

# Defining a function to provide random choice of inputs in grid after the moves of grid from player
def next_step(grid):
    default = False
    while not default:
        # In 4x4 2D matrix assigning random choice of 2,4 in the grid where the grid is empty
        r = choice([0,1,2,3])
        c = choice([0,1,2,3])
        if grid[r][c] == 0:
            default = True
            grid[r][c] = choice([2,4])
    return grid


def pass_grid(g, score, game_over = False, suggested_move = None, autoplay = False):
    # Update grid based on the moves of player
    up_grid = [["" if r == 0 else r for r in row] for row in g]
    return render_template('index.html', row1col1 = up_grid[0][0], row1col2 = up_grid[0][1], row1col3 = up_grid[0][2], row1col4 = up_grid[0][3], 
                                       row2col1 = up_grid[1][0], row2col2 = up_grid[1][1], row2col3 = up_grid[1][2], row2col4 = up_grid[1][3], 
                                       row3col1 = up_grid[2][0], row3col2 = up_grid[2][1], row3col3 = up_grid[2][2], row3col4 = up_grid[2][3], 
                                       row4col1 = up_grid[3][0], row4col2 = up_grid[3][1], row4col3 = up_grid[3][2], row4col4 = up_grid[3][3], grid_encoding = grid_string(g), score = score, game_over = game_over, suggested_move = suggested_move, autoplay = autoplay)


# A function to specify the shifting of grid based on player input
def grid_shifts(g, player_input, player_score):
    score = player_score
    new_grid = [[0 for c in [0,1,2,3]] for r in [0,1,2,3]]
    if player_input == 'up':
        for c in [0,1,2,3]:
            grid_matrix = []
            new_grid_matrix = []
            # Finds a non empty element in a grid and appends element in grid matrix
            for r in [0,1,2,3]:
                if g[r][c] != 0:
                    grid_matrix.append(g[r][c])
            nxt_default = False
            # Considering next default as false for the element next to non empty element of grid 
            for i in range(len(grid_matrix)):
                if nxt_default:
                    nxt_default = False
                else:
                    # Next default is True when the next element is equal to current non empty element of grid
                    # Both elements are summed and appended to new_grid_matrix
                    if i < len(grid_matrix)-1 and grid_matrix[i] == grid_matrix[i+1]:
                        new_grid_matrix.append(grid_matrix[i]*2)
                        score += grid_matrix[i]*2
                        nxt_default = True
                    # But when the next element is not equal to current non empty element of grid
                    # Then the element is just appended to new_grid_matrix
                    else:
                        new_grid_matrix.append(grid_matrix[i])
            # Now appending new_grid_matrix 1st row[all row values are added] to new_grid
            for r in range(len(new_grid_matrix)):
                new_grid[r][c] = new_grid_matrix[r]

    if player_input == 'down':
        for c in [0,1,2,3]:
            grid_matrix = []
            new_grid_matrix = []
            # Finds a non empty element in a grid and appends element in grid matrix
            for r in [3,2,1,0]:
                if g[r][c] != 0:
                    grid_matrix.append(g[r][c])
            nxt_default = False
            # Considering next default as false for the element next to non empty element of grid 
            for i in range(len(grid_matrix)):
                if nxt_default:
                    nxt_default = False
                else:
                    # Next default is True when the next element is equal to current non empty element of grid
                    # Both elements are summed and appended to new_grid_matrix
                    if i < len(grid_matrix)-1 and grid_matrix[i] == grid_matrix[i+1]:
                        new_grid_matrix.append(grid_matrix[i]*2)
                        score += grid_matrix[i]*2
                        nxt_default = True
                    # But when the next element is not equal to current non empty element of grid
                    # Then the element is just appended to new_grid_matrix
                    else:
                        new_grid_matrix.append(grid_matrix[i])
            if len(new_grid_matrix) > 0:
                # Now appending new_grid_matrix last row[all row values are added] to new_grid
               for r in range(3,3-len(new_grid_matrix),-1):
                    new_grid[r][c] = new_grid_matrix[3-r]

    if player_input == 'left':
        for r in [0,1,2,3]:
            grid_matrix = []
            new_grid_matrix = []
            for c in [0,1,2,3]:
                if g[r][c] != 0:
                    grid_matrix.append(g[r][c])
            nxt_default = False
            for i in range(len(grid_matrix)):
                if nxt_default:
                    nxt_default = False
                else:
                    if i < len(grid_matrix)-1 and grid_matrix[i] == grid_matrix[i+1]:
                        new_grid_matrix.append(grid_matrix[i]*2)
                        score += grid_matrix[i]*2
                        nxt_default = True
                    else:
                        new_grid_matrix.append(grid_matrix[i])

            # Now appending new_grid_matrix 1st column[all column values are added] to new_grid
            for c in range(len(new_grid_matrix)):
                new_grid[r][c] = new_grid_matrix[c]
    if player_input == 'right':
        for r in [0,1,2,3]:
            grid_matrix = []
            new_grid_matrix = []
            for c in [3,2,1,0]:
                if g[r][c] != 0:
                    grid_matrix.append(g[r][c])
            nxt_default = False
            for i in range(len(grid_matrix)):
                if nxt_default:
                    nxt_default = False
                else:
                    if i < len(grid_matrix)-1 and grid_matrix[i] == grid_matrix[i+1]:
                        new_grid_matrix.append(grid_matrix[i]*2)
                        score += grid_matrix[i]*2
                        nxt_default = True
                    else:
                        new_grid_matrix.append(grid_matrix[i])
            if len(new_grid_matrix) > 0:

                # Now appending new_grid_matrix last column[all column values are added] to new_grid
               for c in range(3,3-len(new_grid_matrix),-1):
                    new_grid[r][c] = new_grid_matrix[3-c]
    return new_grid, score

# To check whether the game is completed or not, we do this by checking whether all the elements in the grid is zero or not   
def game_over(grid):
    game_over = True

    # To check the count of non zero elements in the grid
    counter = 0
    for r in [0,1,2,3]:
        for c in [0,1,2,3]:
            counter += 1 if grid[r][c] != 0 else 0
            if r < 3 and grid[r][c] == grid[r+1][c]:
                game_over = False
                break
            if c < 3 and grid[r][c] == grid[r][c+1]:
                game_over = False
                break
    if counter == 16 and game_over:
        return True
    return False
    
# To count the number of zero 
def count_empty(grid):
    counter = 0
    for row in grid:
        for each_col in row:
            counter += 1 if each_col == 0 else 0
    return counter

# To suggest a move by thinking 10 moves ahead of that 
def suggest_move(original, num_simulations, depth):
    """ play some scenarios and determine which one has the best expected outcome """
    directions = ['up','down','right','left']
    total_score = {d:0 for d in directions}
    total_deaths = {d:0 for d in directions}
    min_number_moves_to_kill = {d:1000 for d in directions}
    for direction in directions:
        griddd = deepcopy(original)
        score = 0
        gridd, score = grid_shifts(griddd, direction, score)
        gridd = deepcopy(gridd)

        # check whether the next predicted move string and current string are equal or not and start prediction
        if grid_string(gridd) != grid_string(original):
            for i in range(num_simulations):
                grid = deepcopy(gridd)
                grid = next_step(grid)
                d = 1
                deathcount = depth
                while(d <= depth):
                    dir = choice(['up','down','right','left'])
                    prev_encoding = grid_string(grid)
                    grid, score = grid_shifts(grid, dir, score)
                    if grid_string(grid) != prev_encoding:
                        grid = next_step(grid)
                        d += 1
                    else:
                        break
                    if game_over(grid):
                        total_deaths[direction] += 1
                        deathcount = d
                        break
                min_number_moves_to_kill[direction]
                total_score[direction] += score
                min_number_moves_to_kill[direction] = min(min_number_moves_to_kill[direction], deathcount)
    for key in total_deaths:
        if total_deaths[key] == 0:
            total_deaths[key] = -1
    for key in min_number_moves_to_kill:
        if min_number_moves_to_kill[key] == 1000:
            min_number_moves_to_kill[key] = 0
    
    return max(total_score, key=total_score.get)

@app.route('/')
# Start the game
def index():
    start_grid = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    start_grid = next_step(start_grid)
    start_grid = next_step(start_grid)
    return pass_grid(start_grid, 0)
    
@app.route('/move/<string:direction>/<string:last_encoding>/<int:score>/')

# Move the elements if game is not over else directly return the grid
def move(direction, last_encoding, score):
    grid = string_grid(last_encoding)

    grid, score = grid_shifts(grid, direction, score)
    if last_encoding != grid_string(grid):
        grid = next_step(grid)
    suggested_move = suggest_move(grid, 200, 10)
    if game_over(grid):
        return pass_grid(grid, score, True, suggested_move)
    return pass_grid(grid, score, False, suggested_move)
    
@app.route('/autoplay/<string:direction>/<string:last_encoding>/<int:score>/')

# Move automatically when clicked on Automove
def automove(direction, last_encoding, score):
    grid = string_grid(last_encoding)
    grid, score = grid_shifts(grid, direction, score)
    if last_encoding != grid_string(grid):
        grid = next_step(grid)
    suggested_move = suggest_move(grid, 200, 10)
    if game_over(grid):
        return pass_grid(grid, score, True, suggested_move)
    return pass_grid(grid, score, False, suggested_move, autoplay = True)
    
if __name__ == "__main__":
    app.run(debug=False, port = 5000, host = "0.0.0.0")