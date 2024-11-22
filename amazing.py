#!/usr/bin/env python3

import random
import argparse
from typing import List, Any

from helpers import Terminal, create_2d_array

# AMAZING PROGRAM
# CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY

# Refactoring of the "Amazing" BASIC game from the 1978 book BASIC Computer 
# Games by Creative Computing into Python 3 - this version is refactored to 
# accept CLI arguments so that the output can be passed to stdout and printed
#  if required

# usage: Amazing Maze Generator [-help] width height
# Example (Windows) - py .\amazing.py 10 20 prints a maze with 10 columns and 
# 20 rows
# Example (Linux) - python .\amazing.py 10 20 prints a maze with 10 columns 
# and 20 rows

# Original author is Jack Hauber of Windsor, Connecticut

def main():
    """Main game loop
    """

    def check_positive(value: str|int) -> int:   
        """
        Validates if the provided value is a positive integer greater than 1.
        If the value is less than or equal to 1, or if the input cannot be 
        converted to an integer, an exception is raised.
        Args:
            value: str | int- The input value to be validated
        Returns:
            value: int- The valid positive integer greater than 1
        Raises:
            argparse.ArgumentTypeError: If the integer is less than or equal 
            to 1
            Exception: If the input cannot be converted to an integer
        Credit - https://stackoverflow.com/a/64980375 
        """
        try:
            value = int(value)
            if value <= 1:
                raise argparse.ArgumentTypeError(
                    "{} is not a positive integer greater than 1"
                    .format(value)
                    )
        except ValueError:
            raise Exception("{} is not an integer".format(value))
        return value

    parser = argparse.ArgumentParser(
        prog="Amazing Maze Generator",
        description="""
            Generates a random maze to stdout from a provided width and height
            """,
        epilog="Generates a random maze to stdout",
        )

    parser.add_argument(
                        "width",
                        nargs = 1,
                        help = """
                        Enter the width of the maze as a positive integer 
                        greater than 1
                        """,
                        type = check_positive,
                        )
    parser.add_argument(
                        "height",
                        nargs = 1,
                        help = """
                        Enter the height of the maze as a positive integer greater 
                        than 1
                        """, 
                        type = check_positive,
                        )
    
    args = parser.parse_args()
    maze_width = args.width[0]
    maze_height = args.height[0]

    Maze = List[List[Any]]

    # Initialise new terminal - terminal width can be greater than the default 
    # of 80 given stdout can be used - 3 characters are used for each column 
    # in the maze, followed by a single character after the last column
    terminal = Terminal((maze_width + 1) * (3)) 

    maze_cell_state: Maze = create_2d_array(maze_width, maze_height)
    maze_walls: Maze = create_2d_array(maze_width, maze_height)
    backtracking: bool = False 

    # Choose a random starting column for the maze entrance
    entrance_col: int = random.randint(1, maze_width)
    # Choose a random column for the maze exit
    exit_col: int = random.randint(1, maze_height)

    col: int = entrance_col
    row: int = 1
    maze_path: List[str] = []
    counter: int = 0

    def print_first_row(
            terminal, entrance_col: int, maze_width: int
            ) -> Terminal:
        '''
        Prints the first row of the maze with a random entrance.
        Args:
            terminal: terminal class representing data to be output in console
            entrance_col: int - randomly selected maze entrance column
            maze_width: int - maze width
        Returns:
            terminal: updated terminal class representing data to be output in
            console
        '''
        for i in range(0, (maze_width * 3), 3):
            if i == (entrance_col-1)*3:
                # Print the maze entrance
                terminal.add_character(0, i, ".")
                terminal.add_character(0, i + 1, " ")
                terminal.add_character(0, i + 2, " ")
            else:
                # Print the maze walls in first row
                terminal.add_character(0, i, ".")
                terminal.add_character(0, i + 1, "-")
                terminal.add_character(0, i + 2, "-")
        terminal.add_character(0, maze_width * 3, ".")
        return terminal

    def print_exit(terminal, maze_height: int, exit_col: int) -> Terminal:
        '''
        Prints a random exit in the last row of the maze.
        Args:
            terminal: terminal class representing data to be output in console
            maze_height: int - maze height
            exit_col: int - randomly selected maze exit column 
        Returns:
            terminal: updated terminal class representing data to be output in
            console
        '''
        terminal.add_character((maze_height * 2), ((exit_col - 1) * 3), ":")
        terminal.add_character(
            (maze_height * 2), ((exit_col - 1) * 3) + 1, " "
            )
        terminal.add_character(
            (maze_height * 2), ((exit_col - 1) * 3) + 2, " "
            )
        return terminal

    def check_direction(
            row: int, col: int, maze_cell_state: Maze
            ) -> List[str]:
        '''
        Determines the possible directions the maze can move from the 
        specified cell. Function checks all four possible movement directions from the 
        specified position in the maze and returns a list of valid directions 
        where the next move can be made. A direction is considered valid if it 
        leads to a cell that has not yet been visited.
        Args:
            row: int - The current row position in the maze (1-indexed)
            col: int - The current column position in the maze (1-indexed)
            maze_cell_state: List - Variable representing current maze cell 
            state
        Returns:
            possible_directions: list[str]- A list of valid directions 
            ('UP', 'DOWN', 'LEFT', 'RIGHT') where movement is possible
        '''
        possible_directions=[]

        # Check if we can move up
        if row > 1 and maze_cell_state[row - 2][col - 1] != 1:
            possible_directions.append("UP")

        # Check if we can move down
        if row < maze_height and maze_cell_state[row][col - 1] != 1:
            possible_directions.append("DOWN")

        # Check if we can move left
        if col > 1 and maze_cell_state[row - 1][col - 2] != 1:
            possible_directions.append("LEFT")

        # Check if we can move right
        if col < maze_width and maze_cell_state[row - 1][col] != 1:
            possible_directions.append("RIGHT")

        return(possible_directions)

    def move_in_direction(
            direction: str, counter: int, row: int, col: int, 
            backtracking: bool, maze_walls: Maze, maze_cell_state: Maze,maze_path: List[str]
            ):
        '''
        Knocks down walls in the maze in a specified direction by updating the 
        maze wall state. Function updates the current position (`row`, `col`) 
        in the maze and cell visited state based on the provided direction 
        and updates the maze's wall configuration state. If we are 
        backtracking, position is updated without altering the maze wall or
        cell visited state. 
        Args:
            direction: str- direction to move in the maze
            counter : int- tracks the number of cells visited during maze 
            generation
            row: int- current row position in the maze (1-indexed)
            col: int- current column position in the maze (1-indexed)
            backtracking: bool- flag indicating whether we are currently 
            backtracking
            maze_walls: list- 2D list representing the maze wall state
            maze_cell_state: list- 2D list representing the state of each cell 
            in the maze
            maze_path: list- list representing the maze path taken so far
        Returns:
            counter: int- tracks the number of cells visited during maze 
            generation
            row: int- current row position in the maze (1-indexed)
            col: int- current column position in the maze (1-indexed)
            maze_walls: list- 2D list representing the maze wall state
            maze_cell_state: list - 2D list representing the state of each 
            cell in the maze
            maze_path: list- list representing the maze path taken so far
        '''

        # Movement when backtracking is false:
        if direction == "UP" and not backtracking:
            if (maze_walls[row - 1][col - 1] == ""):
                maze_walls[row - 1][col - 1] = "UP"
            # If the cell has already been visited, we change the maze wall 
            # state in the adjacent cell
            elif (maze_walls[row - 1][col - 1] != ""):
                maze_walls[row - 2][col - 1] = "DOWN"
            row -= 1
            maze_cell_state[row - 1][col - 1] = 1
            counter += 1
            maze_path.append("UP")
        elif direction == "DOWN" and not backtracking:
            if (maze_walls[row - 1][col - 1] == ""):
                maze_walls[row - 1][col - 1] = "DOWN"
            elif (maze_walls[row - 1][col - 1] != ""):
                maze_walls[row - 0][col - 1] = "UP"
            row += 1
            maze_cell_state[row - 1][col - 1] = 1
            counter += 1
            maze_path.append("DOWN")
        elif direction == "LEFT" and not backtracking:
            if (maze_walls[row - 1][col - 1] == ""):
                maze_walls[row - 1][col - 1] = "LEFT"
            elif (maze_walls[row - 1][col - 1] != ""):
                maze_walls[row - 1][col - 2] = "RIGHT"
            col -= 1
            maze_cell_state[row - 1][col - 1] = 1
            counter += 1
            maze_path.append("LEFT")
        elif direction == "RIGHT" and not backtracking:
            if (maze_walls[row - 1][col - 1] == ""):
                maze_walls[row - 1][col - 1] = "RIGHT"
            elif (maze_walls[row - 1][col - 1] != ""):
                maze_walls[row - 1][col - 0] = "LEFT"
            col += 1
            maze_cell_state[row - 1][col - 1] = 1
            counter += 1
            maze_path.append("RIGHT")

        # Movement when backtracking is true:
        # Direction is UP - however we need to move DOWN
        elif direction == "UP" and backtracking:
            row += 1
        # Direction is DOWN - however we need to move UP
        elif direction == "DOWN" and backtracking:
            row -= 1
        # Direction is LEFT - however we need to move RIGHT
        elif direction == "LEFT" and backtracking:
            col += 1
        # Direction is RIGHT - however we need to move LEFT
        elif direction == "RIGHT" and backtracking:
            col -= 1
        return(row, col, counter, maze_cell_state, maze_path, maze_walls)

    def generate_maze(
            counter: int, row: int, col: int, backtracking: bool, 
            maze_walls: Maze, maze_cell_state: Maze, maze_path: List[str], 
            maze_width: int, maze_height: int
            ) -> Maze:
        '''
        Generates a maze using a depth-first search (DFS) algorithm with 
        backtracking. If no options remain for backtracking, the function 
        selects a new random starting position within the maze until all cells
        have been visited.
        Args:
            counter : int- tracks the number of cells visited during maze 
            generation
            row: int- current row position in the maze (1-indexed)
            col: int- current column position in the maze (1-indexed)
            backtracking: bool- flag indicating whether we are currently 
            backtracking
            maze_walls: list- 2D list representing the maze wall state
            maze_cell_state: list- 2D list representing the state of each 
            cell in 
            maze_path: list- list representing the maze path taken so far
            the maze
            maze_width: int - maze width
            maze_height: int - maze height
        Returns:
            maze_walls: list- 2D list representing the maze wall state
        '''

        # Mark entrance cell as visited
        maze_cell_state[row - 1][col - 1] = 1
        counter += 1

        while counter < (maze_width * maze_height):
            if not backtracking:
                directions: List[str] = []
                if check_direction(row, col, maze_cell_state):
                    directions = check_direction(row, col, maze_cell_state)
                    direction = random.choice(directions)
                    (row, col, counter, maze_cell_state, maze_path, 
                     maze_walls) = \
                        move_in_direction(
                        direction, counter, row, col, backtracking, 
                        maze_walls, maze_cell_state, maze_path
                        )
                else:
                    backtracking = True 

            if backtracking:
                backtrack_directions = []
                # backtracking is true - no available directions to move but 
                # the maze isn't finished yet
                if not maze_path:
                    # Select another random starting position if the maze 
                    # isn't finished and no options remain for backtracking
                    random_col = (int(random.random() * maze_width))
                    random_row = (int(random.random() * maze_height))
                    col = random_col
                    row = random_row
                    backtracking = False
                    continue
                backtrack_direction = maze_path.pop()
                (row, col, counter, maze_cell_state, maze_path, maze_walls) =\
                move_in_direction(
                        backtrack_direction, counter, row, col, backtracking, 
                        maze_walls, maze_cell_state, maze_path
                        )
                if check_direction(row,col,maze_cell_state):
                    backtrack_directions=check_direction(
                        row,col,maze_cell_state
                        )
                    direction = random.choice(backtrack_directions)
                    backtracking = False
                    (row, col, counter, maze_cell_state, maze_path, 
                    maze_walls) = \
                    move_in_direction(
                        direction, counter, row, col, backtracking, 
                        maze_walls, maze_cell_state, maze_path
                        )
        return maze_walls

    def draw_maze(
            terminal: Terminal, maze_height: int, maze_width: int, row: int,
            col: int, maze_walls: Maze
            ) -> Terminal:
        '''
        Args:
            terminal: terminal class representing data to be output in console
            maze_height: int - maze height        
            maze_width: int - maze width
            row: int- current row position in the maze (1-indexed)
            col: int- current column position in the maze (1-indexed)
            maze_walls: list- 2D list representing the maze wall state
        Returns:
            terminal: updated terminal class representing data to be output in
            console
        '''
        for row in range(1, (maze_height * 2), 2):
            for col in range(0, (maze_width * 3), 3):
                # Draw all walls in maze
                terminal.add_character(row,col, "|")
                terminal.add_character(row,col + 1, " ")
                terminal.add_character(row,col + 2, " ")
                if col == (maze_width - 1) * 3:
                    terminal.add_character(row, col + 3, "|")
                # Draw all floors in maze
                terminal.add_character(row + 1, col, ":")
                terminal.add_character(row + 1, col + 1, "-")
                terminal.add_character(row + 1 ,col + 2, "-")
                if col == (maze_width - 1) * 3:
                    terminal.add_character(row+1,col+3,":")
                if col == (maze_width - 1) * 3 \
                    and row == ((maze_height * 2) - 1):
                    terminal.add_character(row + 1,col + 3, ".")
        
        # Loop through maze and knock down walls depending on state of entry 
        # in maze_walls array
        for row in range(len(maze_walls)):
            for col in range(len(maze_walls[row])):
                if maze_walls[row][col] == "UP":
                    # Knock down floor of cell above
                    terminal.add_character(((row * 2)), (col * 3) + 1, " ")
                    terminal.add_character(((row * 2)), (col * 3) + 2, " ")
                if maze_walls[row][col] == "DOWN":
                    # Knock down floor of cell below
                    terminal.add_character(
                        ((row * 2) + 2), (col * 3) + 1, " "
                        )
                    terminal.add_character(
                        ((row * 2) + 2), (col * 3) + 2, " "
                        )
                if maze_walls[row][col] == "RIGHT":
                    # Knock down wall of cell to the right
                    terminal.add_character(
                        ((row * 2) + 1), (col * 3) + 3, " "
                        )
                if maze_walls[row][col]=="LEFT":
                    # Knock down wall of cell to the left
                    terminal.add_character(
                        ((row * 2) + 1), (col * 3), " "
                        )
        return terminal
    
    maze_walls = generate_maze(
        counter, row, col, backtracking, maze_walls, maze_cell_state, 
        maze_path, maze_width, maze_height
        )
        
    terminal = print_first_row(terminal, entrance_col, maze_width)
    terminal = draw_maze(
        terminal, maze_height, maze_width, row, col, maze_walls
        )
    terminal = print_exit(terminal, maze_height,exit_col)    

    terminal.display()

if __name__ == "__main__":
    main()