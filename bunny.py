#!/usr/bin/env python3

from typing import List

from helpers import Terminal, clear_console, centred_text

# Refactoring of the "Bunny" BASIC game from the 1978 book BASIC Computer 
# Games by Creative Computing into Python 3

def main():
    """Main program loop
    """

    ASCII_OFFSET = 64    # Letters begin at ASCII 65 with A
    BUNNY_STRING = [2,21,14,14,25] 
    # Letters making up BUNNY when ASCII offset is applied
    PATTERN_DATA = [ 
        # Data making up the bunny pattern
        # Integers less than 0 represent a newline, positive integers 
        # represent starting and stopping columns where text should be printed
        # 4096 represents the end of printing
        1, 2, -1, 0, 2, 45, 50, -1, 0, 5, 43, 52, -1, 0, 7, 41, 52, -1,
        1, 9, 37, 50, -1, 2, 11, 36, 50, -1, 3, 13, 34, 49, -1, 4, 14, 32, 48, 
        -1,
        5, 15, 31, 47, -1, 6, 16, 30, 45, -1, 7, 17, 29, 44, -1, 8, 19, 28, 
        43, -1,
        9, 20, 27, 41, -1, 10, 21, 26, 40, -1, 11, 22, 25, 38, -1, 12, 22, 24, 
        36, -1,
        13, 34, -1, 14, 33, -1, 15, 31, -1, 17, 29, -1, 18, 27, -1, 19, 26, 
        -1, 16, 28, -1,
        13, 30, -1, 11, 31, -1, 10, 32, -1, 8, 33, -1, 7, 34, -1, 6, 13, 16, 
        34, -1,
        5, 12, 16, 35, -1, 4, 12, 16, 35, -1, 3, 12, 15, 35, -1, 2, 35, -1, 1, 
        35, -1,
        2, 34, -1, 3, 34, -1, 4, 33, -1, 6, 33, -1, 10, 32, 34, 34, -1, 14, 
        17, 19, 25, 28, 31, 35, 35, -1,
        15, 19, 23, 30, 36, 36, -1, 14, 18, 21, 21, 24, 30, 37, 37, -1, 13, 
        18, 23, 29, 33, 38, -1,
        12, 29, 31, 33, -1, 11, 13, 17, 17, 19, 19, 22, 22, 24, 31, -1, 10, 
        11, 17, 18, 22, 22, 24, 24, 29, 29, -1,
        22, 23, 26, 29, -1, 27, 29, -1, 28, 29, -1, 4096
    ]

    terminal = Terminal()

    def draw_pattern(pattern: List[int]) -> None:
        '''
        Function to draw the bunny pattern.
        Args:
            pattern: list- a list of integers representing pattern data to be 
            converted to a string and added to the terminal display
        Returns:
            None
        '''
        start = 0
        row = 0
        while True: 
            if pattern[start] < 0: 
                print()
                start += 1
                row += 1
                continue
            elif pattern[start] > 240: 
                break
            else:
                stop = start + 1
                for col in range(pattern[start], pattern[stop] + 1):
                    bunny_letter = chr(
                        ASCII_OFFSET + BUNNY_STRING[int(col % 5)]
                        )
                    terminal.add_character(row, col, bunny_letter)
                start += 2
                continue

    draw_pattern(PATTERN_DATA)
    clear_console()
    print(centred_text("BUNNY"))
    print(centred_text("CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY"))
    print("\n" * 3, end="") 
    terminal.display()
    print("\n" * 6, end="")

if __name__ == "__main__":
    main()