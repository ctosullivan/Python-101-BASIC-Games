#!/usr/bin/env python3

import random
from helpers import clear_console, centred_text

# Refactoring of the "Acey Ducey" BASIC game from the 1978 book BASIC Computer
# Games by Creative Computing into Python 3
# Original author is Bill Palmby of Prairie View, Illinois

def random_card() -> int:
    '''Generates a random playing card, represented as an integer from 2 to 14
    Ace=14).
    Args:
        None
    Returns:
        A random integer in the range 2-14
    '''
    return random.randint(2,14)


def print_card(card: int) -> None:
    '''
    Prints the integer or text value of a playing card.
    Args:
        Card: An integer representing a playing card.
    Returns:
        None
    '''    
    if card == 11:
        print("JACK")
    elif card == 12:
        print("QUEEN")
    elif card == 13:
        print("KING")
    elif card == 14:
        print("ACE")
    else:
        print(card)

clear_console()
print(centred_text("ACEY DUCEY CARD GAME"))
print(centred_text("CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY"))
print("\n"*3,end="")
print("ACEY-DUCEY IS PLAYED IN THE FOLLOWING MANNER ")
print("THE DEALER (COMPUTER) DEALS TWO CARDS FACE UP")
print("YOU HAVE AN OPTION TO BET OR NOT BET DEPENDING")
print("ON WHETHER OR NOT YOU FEEL THE CARD WILL HAVE")
print("A VALUE BETWEEN THE FIRST TWO.")
print("IF YOU DO NOT WANT TO BET, INPUT A 0")

def main() -> None:
    '''Main game loop
    '''
    current_money: int = 100
    game_over: bool = False

    while not game_over:
        bet: bool = False
        first_card: int = random_card()
        second_card: int = random_card()

        print(f"YOU NOW HAVE {current_money} DOLLARS")
        print() 
        print("HERE ARE YOUR NEXT TWO CARDS: ")

        # reshuffle if the first card is greater or equal to the second card
        while first_card>=second_card:
            first_card = random_card()
            second_card = random_card()

        print_card(first_card)
        print_card(second_card)
        print("\n"*2,end="")

        while not bet:
            bet_input = int(input("WHAT IS YOUR BET\n"))
            if bet_input > current_money:
                print("SORRY, MY FRIEND, BUT YOU BET TOO MUCH.") 
                print(f"YOU ONLY HAVE {current_money} DOLLARS LEFT TO BET.")  
                continue              
            elif bet_input == 0:
                print("CHICKEN!!")
                print()
                break
            elif bet_input > 0:
                bet = True

        if not bet:
            continue

        third_card: int = random_card()
        print_card(third_card)
        if third_card > first_card and third_card < second_card:
            print("YOU WIN!!!")
            print() 
            current_money += bet_input
        else:
            print("SORRY, YOU LOSE")
            current_money -= bet_input
            if current_money <= 0:
                print("\n"*2,end="")
                print("SORRY, FRIEND, BUT YOU BLEW YOUR WAD.")
                print("\n"*2,end="")
                while not game_over:
                    try_again = input("TRY AGAIN (YES OR NO)\n")
                    print("\n"*2,end="")
                    if try_again.upper()=="YES":
                        current_money=100
                        break
                    elif try_again.upper()=="NO":
                        print("O.K., HOPE YOU HAD FUN!")
                        game_over=True  
                    else:
                         continue 

if __name__ == "__main__":
    main()