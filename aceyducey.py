#!/usr/bin/env python3

# Refactoring of the "Acey Ducey" BASIC game from the 1978 book BASIC Computer Games by Creative Computing into Python 3
# Original author is Bill Palmby of Prairie View, Illinois

import random
import sys
import helpers

def random_card():
    '''
    Generates a random playing card, represented as an integer from 2 to 14 (Ace=14).
    Args:
        None
    Returns:
        None
    '''
    return random.randint(2,14)

def print_card(card):
    '''
    Prints the integer or text value of a playing card.
    Args:
        None
    Returns:
        None
    '''
    if card<11:
        print(card)
    elif card==11:
        print("JACK")
    elif card==12:
        print("QUEEN")
    elif card==13:
        print("KING")
    elif card==14:
        print("ACE")

helpers.clear_console()
print(" "*15+str("ACEY DUCEY CARD GAME"))
print(" "*5+str("CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY"))
sys.stdout.write("\n" * 3) 
print("ACEY-DUCEY IS PLAYED IN THE FOLLOWING MANNER ")
print("THE DEALER (COMPUTER) DEALS TWO CARDS FACE UP")
print("YOU HAVE AN OPTION TO BET OR NOT BET DEPENDING")
print("ON WHETHER OR NOT YOU FEEL THE CARD WILL HAVE")
print("A VALUE BETWEEN THE FIRST TWO.")
print("IF YOU DO NOT WANT TO BET, INPUT A 0")

money = 100
game_over = False

while game_over==False:
    try_again = False
    bet=False
    first_card = random_card();
    second_card = random_card();
    print(f'YOU NOW HAVE {money} DOLLARS')
    sys.stdout.write("\n") 
    print("HERE ARE YOUR NEXT TWO CARDS: ")

    # reshuffle if the first card is greater or equal to the second card
    while first_card>=second_card:
        first_card = random_card();
        second_card = random_card();

    print_card(first_card)
    print_card(second_card)
    sys.stdout.write("\n"*2) 

    while bet==False:
        bet = input("WHAT IS YOUR BET\n")
        if int(bet)>money:
            sys.stdout.write("SORRY, MY FRIEND, BUT YOU BET TOO MUCH.\n") 
            print(f'YOU ONLY HAVE {money} DOLLARS LEFT TO BET.')
            bet=False
    if int(bet)==0:
        sys.stdout.write('CHICKEN!!\n')
        continue
    elif int(bet)<=money:
        third_card = random_card()
        print_card(third_card)
        if third_card > first_card and third_card < second_card:
            sys.stdout.write('YOU WIN!!!\n')
            money += int(bet)
            continue
        else:
            sys.stdout.write('SORRY, YOU LOSE\n')
            money -= int(bet)
            if money <= 0:
                sys.stdout.write('\n'*2)
                sys.stdout.write('SORRY, FRIEND, BUT YOU BLEW YOUR WAD.\n')
                sys.stdout.write('\n'*2)
                while try_again==False:
                    try_again = input('TRY AGAIN (YES OR NO)\n')
                    sys.stdout.write('\n'*2)
                    if try_again.upper()=="YES":
                        money=100
                        continue
                    else:
                        sys.stdout.write('O.K., HOPE YOU HAD FUN!')
                        game_over=True
                        break

    