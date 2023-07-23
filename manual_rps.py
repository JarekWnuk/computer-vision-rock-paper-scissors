import random

choice_list =["Rock", "Paper", "Scissors"]

def get_computer_choice():

    '''
    This function generates a choice of hand for the computer.

    The computer choice is a random selection from choice_list containing:
    Rock, Paper and Scissors.

    Returns:
        str: a random choice of hand from choice_list
    '''
    return random.choice(choice_list)

def get_user_choice():
    
    '''
    This function asks the user for a choice of hand.

    The "while True" loop will infinitely ask for user input until valid.
    The user input is validated against the options available in choice_list.
    Because the input can be valid even if the first letter is not capitalized,
    it is automatically capitalized when validating.

    Returns:
        str: a choice of hand obtained from the user
    '''

    while True:
        choice = input("Choose from: rock, paper, scissors:\n")
        if choice.capitalize() in choice_list:
            break
        else:
            print("Incorrect input, try again.")
            continue
    return choice.capitalize()

def get_winner(computer_choice, user_choice):

    '''
    This function announces the winner of the RPS game.

    The choice of hand for the computer and user are compared using game logic.
    The outcome is printed to the screen. The game ends after one round and a tie is
    one of the possible outcomes.
    
    Args:
        computer_choice (str): choice of hand for the computer
        user_choice (str): choice of hand for the user

    Returns:
        None
    '''

    if computer_choice != user_choice:
        if computer_choice == "Rock" and user_choice != "Paper"\
        or computer_choice == "Paper" and user_choice != "Scissors"\
        or computer_choice == "Paper" and user_choice != "Scissors"\
        or computer_choice == "Scissors" and user_choice != "Rock":
            print("You lost")
        else:
            print("You won!")
    else:
        print("It is a tie!")

def play():

    '''
    This function calls all the other game functions to initialize gameplay.

    The value returned from function "get_computer_choice()" is stored in variable "computer_choice".
    The value returned from function "get_user_choice()" is stored in variable "user_choice".
    Both variables are used as arguments in function "get_winner()", which prints the outcome to the screen.

    Returns:
        None
    '''
    computer_choice = get_computer_choice()
    user_choice = get_user_choice()
    get_winner(computer_choice, user_choice)

if __name__ == "__main__":        
    play()