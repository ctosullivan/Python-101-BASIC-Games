import platform
import os
import sys

def clear_console():
    """
    Clears the console screen.

    This function detects the operating system and issues the appropriate command
    to clear the console. On Windows, it runs the 'cls' command, while on other 
    platforms (Linux, macOS), it runs the 'clear' command.
    Args:
        None
    Returns:
        None
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

class Terminal:
    """
    A class that replicates BASIC terminal functions.

    Attributes:
    -----------
    width : int
        The width of the terminal (default is 80 columns).
    screen : 2D list of str
        A 2D list representing the terminal display, where each element is a row containing characters.

    Methods:
    --------
    add_character(row: int, col: int, char: str):
        Adds a character at the specified row and column position on the screen. 
        Automatically expands the screen height if the specified row does not exist. 
        Prints a message if the column is out of bounds.

    display():
        Displays the current state of the terminal by printing all rows to the standard output.

    reset():
        Resets the terminal display to its initial state, clearing all characters and returning to a single empty row.
    """
    def __init__(self, width=80):
        ''' 
        Initializes a terminal with one row, containing 80 spaces by default.
        '''
        self.width=width
        self.screen = [[' ' for _ in range(self.width)]]

    def add_character(self, row=int, col=int, char=any):
        '''
        Adds a character to the specified row and column in the terminal display, if within bounds, while adding new rows to the terminal as required.
        '''
        while len(self.screen) <= row:
            self.screen.append([' ' for _ in range(self.width)])
        
        if 0 <= col < self.width:
            self.screen[row][col] = char
        else:
            print(f"Column {col} is out of bounds")

    def display(self):
        '''
        Displays the current state of the terminal by printing all rows to the standard output.
        '''
        for row in self.screen:
            sys.stdout.write("".join(row)+"\n")

    def reset(self):
        '''
        Resets the terminal display to its initial state, clearing all characters and returning to a single empty row.
        '''
        self.screen = [[' ' for _ in range(self.width)]]

def create_2d_array(rows=int, cols=int, fill_value=""):
    """
    Generates a 2D array with specified dimensions and an optional fill value.

    Args:
        rows (int): The number of rows in the 2D array.
        cols (int): The number of columns in the 2D array.
        fill_value (optional, any type): The value to fill each element of the array with. Defaults to "".

    Returns:
        list: A 2D list (array) with dimensions [rows][cols], filled with `fill_value`.

    Raises:
        ValueError: If `rows` or `cols` are non-positive integers.
    """
    if rows <= 0 or cols <= 0:
        raise ValueError("Number of rows and columns must be positive integers.")
    return [[fill_value for _ in range(rows)] for _ in range(cols)]