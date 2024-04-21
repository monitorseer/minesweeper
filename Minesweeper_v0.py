## MOST RECENT
# BARELY WORKS
# Minesweeper Game
# Libraries that would be used in the code
import random
import copy

# Init
grid = []
labels_column = []
labels_column_count = 100 # Amount of labels present in labels_column list, is 1/2 letters
labels_row = []
labels_row_count = 100 # Amount of labels present in labels_row list, is a num
ms_lose = False
ms_continue = True
mine_possible_locations = []
empty_spaces = 0
# Functions

# This grid function makes the grid looks much readable and cleaner to the user
def ms_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end=' ')
        print()


# Validates the guess by player
def guess_validate(guess): # Take note, format for user's guess is "(letter) (number)"
    guess_col_row = guess.split(" ") # Extracts the guess column and row correspondingly
    guess_col = guess_col_row[0]
    guess_possible_col = labels_row[0:columns] # Takes the row labels accordingly
    guess_row = guess_col_row[1]
    try: # Checks whether guess_row is an integer
        guess_row = int(guess_col_row[1])
    except ValueError:
        return False
    guess_possibile_row = labels_column[0:rows] # Takes the column labels accordingly

    guess_spaceless = guess.replace(" ", "") # Removes the spaces from player's guess
    if guess_spaceless.isalnum() == False: # If spaces are included, it will return False
        return False
    elif guess_col not in guess_possible_col or guess_row not in guess_possibile_row: # If guess is out of range, return False
        return False
    else:
        return True


# Process of converting user input to coordinates for the grid
def conversion(guess):
    conv_index_second_char = 0 # In the case of no second char, it would not return an error for below
    conv_col_row = guess.split(" ") # Separates column and row

    conv_col_char = conv_col_row[0]
    conv_first_char = conv_col_char[0]
    conv_index_first_char = labels_column.index(conv_first_char) # Finds the index of first letter in labels_column list

    if len(conv_col_char) == 2: # Following code will be extracted if length of letters is 2
        conv_second_char = conv_col_char[-1] # Extracts second char from the char column
        conv_index_second_char = labels_column.index(conv_second_char) # Finds the index of second letter in labels_column list
    conv_col = (conv_index_first_char + conv_index_second_char * 26) # Calculates the column to extract

    conv_row = int(conv_col_row[1])

    tile = [conv_row+1, conv_col+1]
    return tile


# Process of finding the tile status
def tile_char(tile, grid):
    # Init
    possible_adj_tiles = []
    adj_tile_values = []
    tile_row = tile[0]
    tile_col = tile[1]
    mine_count = 0
    # Tile orders: Above left mid right, left mid right, below left mid right
    adjacent_tiles = [[tile_row-1, tile_col-1], [tile_row-1, tile_col], [tile_row-1, tile_col+1], [tile_row, tile_col-1], [tile_row, tile_col+1], [tile_row+1, tile_col-1], [tile_row+1, tile_col], [tile_row+1, tile_col+1]]

    # If tile is a mine
    if admin_grid[tile_row][tile_col] == "X":
        return "X"

    # If tile is on the side
    if tile_row == 1 or tile_row == columns or tile_col == 1 or tile_col == rows:
        for adj_tile in adjacent_tiles:
            adj_tile_row = adj_tile[0]
            adj_tile_col = adj_tile[1]

            # Checks whether adjacent tile is within grid range and stores it
            if adj_tile_row >= 1 and adj_tile_row <= columns and adj_tile_col >= 1 and adj_tile_col <= rows:
                possible_adj_tiles.append(adj_tile)

        # Finds the values from the adjacent tiles of a selected tile
        for pos_adj_tile in possible_adj_tiles:
            pos_adj_tile_row = pos_adj_tile[0]
            pos_adj_tile_col = pos_adj_tile[1]
            # print(f"p_adjtilecol: {p_adjtile_row}")
            # print(f"p_adjtilerow: {p_adjtile_col}")
            # print(ms_grid(admin_grid))
            # print(admin_grid[p_adjtile_row][p_adjtile_col])
            adj_tile_values.append(grid[pos_adj_tile_row][pos_adj_tile_col])
        mine_count += (adj_tile_values).count("X") # Counts amount of mines to find status of tile

    # If tile is not on the side
    else:
        for adj_tile in adjacent_tiles:
            adj_tile_row = adj_tile[0]
            adj_tile_col = adj_tile[1]
            adj_tile_values.append(grid[adj_tile_row][adj_tile_col])
        mine_count += (adj_tile_values).count("X") # Counts amount of mines to find status of tile

    return mine_count


# Process to find how many tiles should be opened after every action (buggy, temporarily excluded)
# def tile_open(tile):
#     adjtile_values_tileopen = []
#     safe_tile_list = []
#     tile_row = tile[0]
#     tile_col = tile[1]
#     adjacent_tiles = [[tile_row-1, tile_col-1], [tile_row-1, tile_col], [tile_row-1, tile_col+1], [tile_row, tile_col-1], [tile_row, tile_col+1], [tile_row+1, tile_col-1], [tile_row+1, tile_col], [tile_row+1, tile_col+1]]
#     for adj_tile in adjacent_tiles:
#         adj_tile_row = adj_tile[0]
#         adj_tile_col = adj_tile[1]
#         adjtile_values_tileopen.append(admin_grid[adj_tile_row+1][adj_tile_col+1])
#         print(adjtile_values_tileopen)
#         mine_count_tileopen = (adjtile_values_tileopen).count("X")
#         if mine_count_tileopen == 0:
#             safe_tile_list.append(adj_tile)
#     return safe_tile_list


# Introduction
print("Hello! Welcome to Minesweeper!")
print("You may select a difficulty (easy, medium, hard) or create your own board! (custom)")

# Adds the labels to row and column label lists
for labels_letter in range(ord("A"), ord("Z")+1): # Creates row labels for every alphabet
    labels_column.append(chr(labels_letter))
    labels_column_count -= 1

for letter2 in range(ord("A"), ord("Z")+1): # Since there are only 26 alphabets, duplicates are needed for more row labels
    if labels_column_count < 1:
        break
    for letter3 in range(ord("A"), ord("Z")+1):
        labels_column_count -= 1
        labels_column.append(chr(letter2) + chr(letter3))
        if labels_column_count < 1:
            break

for row_num in range(labels_row_count):
    labels_row.append(row_num)

# Lets user choose whether they want to play fixed modes or have it their way
mode = input("Please enter the difficulty (easy, medium, hard) or (custom) to start!")

# Sets the grid according to mode
if mode == "easy":
    rows = 9
    columns = 9
    mines = 10
elif mode == "medium":
    rows = 16
    columns = 16
    mines = 40
elif mode == "hard":
    rows = 20
    columns = 24
    mines = 99
# elif mode == "custom":
#     row = int(input("How many rows do you want your grid to have?"))
#     column = int(input("How many rows do you want your grid to have?"))
#     mines = int(input("How many mines do you want to have on your board?"))
#     tiles = row * column # Total tiles in grid to check whether board can contain specified amount of mines

    # Validation for custom
    while mines >= tiles or (mines-1) == tiles:
        if mines >= tiles:
            print("Come on, how you can play minesweeper if there is no mineless spaces? Please re-enter.")
            row = int(input("How many rows do you want your grid to have?"))
            column = int(input("How many rows do you want your grid to have?"))
            mines = int(input("How many mines do you want to have on your board?"))
        elif (mines-1) == tiles:
            print("The first spot you select would win you the game, please re-enter.")
            row = int(input("How many rows do you want your grid to have?"))
            column = int(input("How many rows do you want your grid to have?"))
            mines = int(input("How many mines do you want to have on your board?"))

# Creates a grid that does not look very compact, this grid will be constantly modified, then passed into ms_grid
for grid_rows in range(rows+1):
    row = []
    for grid_columns in range(columns+1):
        row.append("-")
    grid.append(row)

# Adds row and column labels for the grid
grid[0][0] = "M" # Symbol for left corner in grid

# In the first column, the row labels(numbers) are applied.
for labels_first_col_index in range(1, len(grid)):
    grid[labels_first_col_index][0] = labels_row[labels_first_col_index-1]

# In the first row, the column labels(letters) are applied.
for labels_first_row_index in range(1, len(grid[0])):
    grid[0][labels_first_row_index] = labels_column[labels_first_row_index-1]

# Lets user know the format of entering input
print("Due to my coding limitations, you cannot click on the grid to reveal tiles.")
print("Instead, to reveal tiles, you would have to type in your answer in a certain format.")
print("The format is (letter of column) (num of row)")
print("So something like 'A 0' would be valid. Happy mine sweeping!")

# ! First guess !
guess = input("Please enter the first tile you want to reveal: ")
while guess_validate(guess): # Validates the guess
    print("Invalid guess! Please re-enter!")
    guess = input("Please enter the first tile you want to reveal: ")
guess_converted = conversion(guess) # Converts user's guess into position for indexing
admin_grid = copy.deepcopy(grid) # ! .copy only copies one list, not the list of lists !

# Distributes the mines only after the first input, so the first input wouldn't be an immediate loss
for mine_col in range(1, columns):
    for mine_row in range(1, rows):
        mine_possible_locations.append([mine_col, mine_row])
for mine in range(mines):
    mine_location = random.choice(mine_possible_locations)
    mine_possible_locations.remove(mine_location)
    admin_grid[mine_location[0]][mine_location[1]] = "X"

# Producing admin grid
for index_row, row in enumerate(admin_grid[:-1]):
    for index_tile, tile in enumerate(row[:-1]):
        admin_grid[index_row+1][index_tile+1] = tile_char([index_row+1, index_tile+1], admin_grid)

# Prints the grid after first guess
guess_converted = conversion(guess) # Converts user's guess into position for indexing
print(guess_converted)
guess_converted_row = guess_converted[0]
guess_converted_col = guess_converted[1]
print(guess_converted_row)
grid[guess_converted_row][guess_converted_col] = admin_grid[guess_converted_row][guess_converted_col]
print(ms_grid(grid))
print(ms_grid(admin_grid))

while ms_continue:
    ms_complete = True
    empty_spaces = 0
    guess = input("Please enter the next tile you want to reveal: ")
    # Validates input
    while guess_validate(guess): # Validates the guess
        print("Invalid guess! Please re-enter!")
        guess = input("Please enter the next tile you want to reveal: ")
    # Converts guess into indexes
    guess_converted = conversion(guess)
    guess_converted_row = guess_converted[0]
    guess_converted_col = guess_converted[1]
    grid[guess_converted_row][guess_converted_col] = admin_grid[guess_converted_row][guess_converted_col]
    tile_value = tile_char(guess_converted, admin_grid)
    print(f"tv: {tile_value}")
    if tile_value == 'X':
        print("a")
        ms_lose = True
        break
    for row in grid:
        for item in row:
            if item == '-':
                empty_spaces += 1
    print(f"empty: {empty_spaces}")
    print(f"mines: {mines}")
    if empty_spaces > mines:
        ms_complete = False
    # safe_tile_list = tile_open(guess_converted)
    # if safe_tile_list != []:
    #     for safe_tile in safe_tile_list:
    #         safe_tile_col = safe_tile[0]
    #         safe_tile_row = safe_tile[1]
    #         grid[safe_tile_col][safe_tile_row] = '0'
    if ms_complete == True:
        break
    print(ms_grid(grid))
    print(ms_grid(admin_grid))
if ms_lose == True:
    print("Oh no! You uncovered a mine! Game over!")
    print(f"You got until {ms_grid(grid)}")
    print(f"The full grid is {ms_grid(admin_grid)}")
elif ms_complete == True:
    print("Congrats! You won!")
