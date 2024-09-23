#!/usr/bin/env python3

# AMAZING PROGRAM
# CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY

# Refactoring of the "Amazing" BASIC game from the 1978 book BASIC Computer Games by Creative Computing into Python 3 - this version is refactored to accept CLI arguments so that the output can be passed to stdout and printed if required

# usage: Amazing Maze Generator [-help] width height
# Example - py .\amazing.py 10 20 prints a maze with 10 columns and 20 rows

# Original author is Jack Hauber of Windsor, Connecticut

import random
import argparse
import helpers

def check_positive(value):
    # Credit to https://stackoverflow.com/a/64980375    
    """
    Validates if the provided value is a positive integer greater than 1.
    If the value is less than or equal to 1, or if the input cannot be converted to an integer, an exception is raised.
    Args:
        value (str or int): The input value to be validated.
    Returns:
        int: The valid positive integer greater than 1.
    Raises:
        argparse.ArgumentTypeError: If the integer is less than or equal to 1.
        Exception: If the input cannot be converted to an integer.
    """
    try:
        value = int(value)
        if value <= 1:
            raise argparse.ArgumentTypeError("{} is not a positive integer greater than 1".format(value))
    except ValueError:
        raise Exception("{} is not an integer".format(value))
    return value

parser = argparse.ArgumentParser(
    prog='Amazing Maze Generator',
    description='Generates a random maze to stdout from a provided width and height',
    epilog='Generates a random maze to stdout',
)
parser.add_argument('width',help="Enter the width of the maze as a positive integer greater than 1", type=check_positive)

parser.add_argument('height',help="Enter the height of the maze as a positive integer greater than 1", type=check_positive)

# Credit to https://stackoverflow.com/a/12818237 - unknown arguments are ignored so that output can be passed to other commands

args = parser.parse_known_args()
width = getattr(args[0],"width")
height = getattr(args[0],"height")

# Initialise new terminal - terminal width can be greater than the default of 80 given stdout can be used - 3 characters are used for each column in the maze, followed by a single character after the last column
terminal = helpers.Terminal((width+1)*(3)) 

# W variable in original source code - intiialised at line 110
maze_cell_state = helpers.create_2d_array(width,height)

# V variable in original source code - intiialised at line 110
maze_walls = helpers.create_2d_array(width,height)

# q variable in original source code - initialised at line 160 as 0 - variable determines whether we are backtracking
backtrack = False 

# x variable in original source code - initialised at line 160 - variable chooses a random starting column for the maze
random_col = (int(random.random()*(width))+1)

col = random_col
row = 1

# Variable to store path taken
maze_path = []

# c variable in original source code - initialised at line 195
counter = 0

def print_first_row():
    '''
    Prints the first row of the maze with a random entrance.
    Args:
        None
    Returns:
        None
    '''
    for i in range(0,((width*3)),3):
        if i == (random_col-1)*3:
            # Print the maze entrance at a random col
            terminal.add_character(0,i,".")
            terminal.add_character(0,i+1," ")
            terminal.add_character(0,i+2," ")
        else:
            # Print the maze walls
            terminal.add_character(0,i,".")
            terminal.add_character(0,i+1,"-")
            terminal.add_character(0,i+2,"-")
    terminal.add_character(0,width*3,".")

def print_exit():
    '''
    Prints a random exit in the last row of the maze.
    Args:
        None
    Returns:
        None
    '''
    random_col = (int(random.random()*(width)))
    terminal.add_character((height*2),(random_col*3),":")
    terminal.add_character((height*2),(random_col*3)+1," ")
    terminal.add_character((height*2),(random_col*3)+2," ")

def check_direction(row=int,col=int):
    '''
    Determines the possible directions the maze can move from the specified cell.
    Function checks all four possible movement directions from the specified position in the maze and returns a list of valid directions where the next move can be made. A direction is considered valid if it leads to a cell that has not yet been visited.
    Args:
        row : int
        The current row position in the maze (1-indexed).
        col : int
        The current column position in the maze (1-indexed).
    Returns:
    --------
    list[str] or bool
        - A list of valid directions ('UP', 'DOWN', 'LEFT', 'RIGHT') where movement is possible.
        - If no valid directions are found, returns False.
    '''
    possible_directions=[]

    # Check if we can move up
    if row > 1 and maze_cell_state[row-2][col-1]!=1:
        possible_directions.append("UP")

    # Check if we can move down
    if row < height and maze_cell_state[row][col-1]!=1:
        possible_directions.append("DOWN")

    # Check if we can move left
    if col > 1 and maze_cell_state[row-1][col-2]!=1:
        possible_directions.append("LEFT")

    # Check if we can move right
    if col < width and maze_cell_state[row-1][col]!=1:
        possible_directions.append("RIGHT")

    if len(possible_directions)>0:
        return(possible_directions)
    else: return False

def move_in_direction(direction=str):
    '''
    Knocks down walls in the maze in a specified direction by updating the maze wall state.
    Function updates the current position (`row`, `col`) in the maze and cell visited state based on the provided direction and updates the maze's wall configuration state. If we are backtracking, position is updated without altering the maze wall or cell visited state. 
    Args:
        direction : str
        The direction to move in the maze.
    Global Variables:
    counter : int
        Tracks the number of cells visited during maze generation.
    row : int
        The current row position in the maze (1-indexed).
    col : int
        The current column position in the maze (1-indexed).
    backtrack : bool
        A flag indicating whether we are currently backtracking.
    maze_walls : list
        A 2D list representing the maze wall state.
    maze_cell_state : list
        A 2D list representing the state of each cell in the maze.
    Returns:
        None
    '''

    global counter
    global row
    global col
    global backtrack
    global maze_walls
    global maze_cell_state

    # Movement when backtracking is false:
    if direction == "UP" and backtrack==False:
        if (maze_walls[row-1][col-1] == ""):
            maze_walls[row-1][col-1] = "UP"
        # If the cell has already been visited, we change the maze wall state in the adjacent cell
        elif (maze_walls[row-1][col-1] != ""):
            maze_walls[row-2][col-1] = "DOWN"
        row -= 1
        maze_cell_state[row-1][col-1] = 1
        counter += 1
        maze_path.append("UP")
    elif direction == "DOWN" and backtrack==False:
        if (maze_walls[row-1][col-1] == ""):
            maze_walls[row-1][col-1] = "DOWN"
        elif (maze_walls[row-1][col-1] != ""):
            maze_walls[row-0][col-1] = "UP"
        row += 1
        maze_cell_state[row-1][col-1] = 1
        counter += 1
        maze_path.append("DOWN")
    elif direction == "LEFT" and backtrack==False:
        if (maze_walls[row-1][col-1] == ""):
            maze_walls[row-1][col-1] = "LEFT"
        elif (maze_walls[row-1][col-1] != ""):
            maze_walls[row-1][col-2] = "RIGHT"
        col -= 1
        maze_cell_state[row-1][col-1] = 1
        counter += 1
        maze_path.append("LEFT")
    elif direction == "RIGHT" and backtrack==False:
        if (maze_walls[row-1][col-1] == ""):
            maze_walls[row-1][col-1] = "RIGHT"
        elif (maze_walls[row-1][col-1] != ""):
            maze_walls[row-1][col-0] = "LEFT"
        col += 1
        maze_cell_state[row-1][col-1] = 1
        counter += 1
        maze_path.append("RIGHT")

    # Movement when backtracking is true:
    # Direction is UP - however we need to move DOWN
    elif direction == "UP" and backtrack==True:
        row += 1
    # Direction is DOWN - however we need to move UP
    elif direction == "DOWN" and backtrack==True:
        row -= 1
    # Direction is LEFT - however we need to move RIGHT
    elif direction == "LEFT" and backtrack==True:
        col += 1
    # Direction is RIGHT - however we need to move LEFT
    elif direction == "RIGHT" and backtrack==True:
        col -= 1

def generate_maze():
    '''
    Generates a maze using a depth-first search (DFS) algorithm with backtracking.
    If no options remain for backtracking, the function selects a new random starting position within the maze until all cells have been visited.
    Global Variables:
    counter : int
        Tracks the number of cells visited during maze generation.
    row : int
        The current row position in the maze (1-indexed).
    col : int
        The current column position in the maze (1-indexed).
    backtrack : bool
        A flag indicating whether we are currently backtracking.
    maze_path : list
        A list of the path taken in the maze.
    Returns:
        None
    '''
    global counter
    global row
    global col
    global backtrack
    global maze_path

    # Mark entrance cell as visited
    maze_cell_state[row-1][col-1] = 1
    counter += 1

    while counter < (width*height):
        if backtrack == False:
            directions = []
            if check_direction(row,col):
                directions = check_direction(row,col)
                direction = random.choice(directions)
                move_in_direction(direction)
            else:
                backtrack = True 

        if backtrack == True:
            backtrack_directions=[]
            # backtrack is true - no available directions to move but the maze isn't finished yet
            if maze_path==[]:
                # Select another random starting position if the maze isn't finished and no options remain for backtracking
                random_col = (int(random.random()*(width)))
                random_row = (int(random.random()*(height)))
                col = random_col
                row = random_row
                backtrack = False
                continue
            backtrack_direction = maze_path.pop()
            move_in_direction(backtrack_direction)
            if check_direction(row,col):
                backtrack_directions=check_direction(row,col)
                direction = random.choice(backtrack_directions)
                backtrack = False
                move_in_direction(direction)
            
def draw_maze():
    '''
    Draws the full maze and then knocks down walls depending on the maze wall state.
    Args:
        None
    Returns:
        None
    '''
    for row in range(1,(height*2),2):
        for col in range(0,(width*3),3):

            # Draw all walls in maze
            terminal.add_character(row,col,"|")
            terminal.add_character(row,col+1," ")
            terminal.add_character(row,col+2," ")
            if col==(width-1)*3:
                terminal.add_character(row,col+3,"|")

            # Draw all floors in maze
            terminal.add_character(row+1,col,":")
            terminal.add_character(row+1,col+1,"-")
            terminal.add_character(row+1,col+2,"-")
            if col==(width-1)*3:
                terminal.add_character(row+1,col+3,":")
            if col==(width-1)*3 and row==((height*2)-1):
                terminal.add_character(row+1,col+3,".")
    
    # Loop through maze and knock down walls depending on state of entry in maze_walls array
    for row in range(len(maze_walls)):
        for col in range(len(maze_walls[row])):
            if maze_walls[row][col]=="UP":
                # Knock down floor of cell above
                terminal.add_character(((row*2)),(col*3)+1," ")
                terminal.add_character(((row*2)),(col*3)+2," ")
            if maze_walls[row][col]=="DOWN":
                # Knock down floor of cell below
                terminal.add_character(((row*2)+2),(col*3)+1," ")
                terminal.add_character(((row*2)+2),(col*3)+2," ")
            if maze_walls[row][col]=="RIGHT":
                # Knock down wall of cell to the right
                terminal.add_character(((row*2)+1),(col*3)+3," ")
            if maze_walls[row][col]=="LEFT":
                # Knock down wall of cell to the left
                terminal.add_character(((row*2)+1),(col*3)," ")

print_first_row()
generate_maze()
draw_maze()
print_exit()    

terminal.display()