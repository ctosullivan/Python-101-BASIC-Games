#!/usr/bin/env python3

import sys
from typing import List, NamedTuple
from collections import namedtuple

from helpers import centred_text, clear_console, print_tabbed_text

# Animal
# Originally developed by Arthur Luehrmann at Dartmouth College.
# Subsequently shortened & modified by Nathan Teichholtz at DEC
# and Steve North at Creative Computing

Node = namedtuple("Node", "question, true, false")

def display_intro() -> None:
    """Displays the introduction text.
    """
    clear_console()
    print(centred_text("ANIMAL"))
    print(centred_text("CREATIVE COMPUTING  MORRISTOWN, NEW JERSEY"))
    print("\n" * 3, end = "")
    print("PLAY 'GUESS THE ANIMAL'")
    print()
    print("THINK OF AN ANIMAL AND THE COMPUTER WILL TRY TO GUESS IT.")
    print()


def get_user_input(input_question: str, input_list: List[str]) -> str:
    """Function gets input from the user using the input_question argument 
    as a prompt and returns the matching string from the input list 
    provided. The function will attempt to match at least one letter in
    the input with the item in the input list - i.e. "Y" will return "YES",
    "YE" will return "YES" etc. If no matching string is found, the user input 
    string is returned.
    Args:
        input_question: str- string to be used as a prompt for the input 
        question
        input_list: List[str]- list of possible options
    Returns:
        selected_option: str- string representing the option selected or
        string entered if no match found
    """
    input_list = [ item.upper() for item in input_list ]
    while True:
        input_text = input(f"{input_question}?\n").upper()
        if input_text in input_list:
            return input_text
        for option in input_list:
            for i in range(len(option)):
                if input_text.startswith(option[0:i+1]):
                    return option
        # no match found in the input list - return the user input
        if input_text:
            return input_text
        
def print_animal_list(node: Node) -> None:
    """Traverses the animal tree and prints the curent list of animals 
    the computer knows.
    Args:
        node: Node - Node representing current tree of known animals
    Returns:
        None
    """
    animal_set = set()

    def traverse(node):
        if isinstance(node, Node):
            traverse(node.true)
            traverse(node.false)
        else:
            # Leaf node reached
            animal_set.add(node)

    traverse(node)
    print("ANIMALS I ALREADY KNOW ARE:")
    animal_list = list(animal_set)
    print_tabbed_text(animal_list)


def thinking_of_animal_question(node: Node) -> bool:
    """ Asks if the user is thinking of an animal and handles the 
    response.
    Args:
        node: Node- current tree of known animals so that 
        print_animal_list can be called 
    Returns: 
        True-  if the user has answered affirmatively
        False- if the user has answered negatively
    """
    while True:
        thinking_of_animal = get_user_input(
            "ARE YOU THINKING OF AN ANIMAL", 
            ["YES", "NO", "LIST", "", " "],
            )
        match thinking_of_animal:
            case "LIST":
                print_animal_list(node)
            case "YES":
                return True
            case "NO" | "" | " ":
                return False

def guess_animal(node: Node) -> tuple[bool, List[str]] | None:
    """
    Traverses the animal tree starting at the parent node & guesses animals 
    until a leaf is reached. Returns whether the last guess was correct and 
    the path to insert a new node if needed.
    Args:
        node: Node - the root node of the animal tree
    Returns:
        tuple[bool, list[str]]: A tuple containing:
            - A boolean indicating if the last guess was correct
            - A list representing the path to insert a new node if the guess 
            was incorrect
    """
    current_node = node
    path = []

    while isinstance(current_node, Node):
        animal_guess = get_user_input(
            current_node.question,
            ["YES", "NO", "LIST", "", " "],
            )
        match animal_guess:
            case "LIST":
                print_animal_list(node)
            case "YES":
                path.append("true")
                current_node = current_node.true
            case "NO":
                path.append("false")
                current_node = current_node.false
            case "" | " ":
                print("GAME OVER")
                sys.exit()    
    
    # Current_node is now a leaf
    animal_guess = get_user_input(
        f"IS IT A {current_node}",
        ["YES", "NO", "LIST", "", " "],
        )
    match animal_guess:
        case "LIST":
            print_animal_list(node)
        case "YES":
            return True, path
        case "NO":
            return False, path
        case "" | " ":
            print("GAME OVER")
            sys.exit()
    return None


def add_new_animal(node: Node, path: list[str]) -> Node:
    """
    Add a new animal and its differentiating question to the tree.
    Args:
        node (Node): The root node of the tree
        path (list[str]): Path to the node that was guessed incorrectly
    Returns:
        Node: The updated tree with the new animal node inserted
    """
    def recursive_update(current_node: Node, path: list[str]) -> Node:
        if not path:  # Base case: replace the current node
            new_animal = get_user_input(
                "THE ANIMAL YOU WERE THINKING OF WAS A",
                [],
                )
            new_question = get_user_input(
                f"PLEASE TYPE IN A QUESTION TO DISTINGUISH A {new_animal} "
                f"FROM A {current_node}",
                [],
            )
            new_answer = get_user_input(
                f"FOR A {new_animal} THE ANSWER WOULD BE", 
                ["YES", "NO"],
            )
            # Create the new node
            if new_answer == "YES":
                return Node(new_question, new_animal, current_node)
            else:
                return Node(new_question, current_node, new_animal)

        # Recursive case: traverse the tree
        step = path[0]
        if step == "true":
            return Node(
                current_node.question,
                recursive_update(current_node.true, path[1:]),
                current_node.false
            )
        else:
            return Node(
                current_node.question,
                current_node.true,
                recursive_update(current_node.false, path[1:])
            )
    # Start the recursive update and return the updated tree
    return recursive_update(node, path)

def main():
    """Main game loop
    """
    animal_tree = Node("DOES IT SWIM", "FISH", "BIRD")

    display_intro()

    while True:
        match thinking_of_animal_question(animal_tree):
            case True:
                guess_correct, path = guess_animal(animal_tree)
                if guess_correct:
                    print("WHY NOT TRY ANOTHER ANIMAL?")
                    continue
                if not guess_correct:
                    animal_tree = add_new_animal(animal_tree, path)
                    continue
            case False:
                print("GAME OVER")
                break

        
if __name__ == "__main__":
    main()