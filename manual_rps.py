import random

# gets random choice for computer
def get_computer_choice():
    choice_list =["Rock", "Paper", "Scissors"]
    return random.choice(choice_list)

# asks user for choice
def get_user_choice():
    while True:
        choice = input("Choose from: rock, paper, scissors:\n")
        if choice.capitalize() in ["Rock", "Paper", "Scissors"]:
            break
        else:
            print("Incorrect input, try again.")
            continue
    return choice.capitalize()

# compares computer_choice and user_choice and prints the outcome, both arguments are required
def get_winner(computer_choice, user_choice):
    if computer_choice != user_choice:
        if computer_choice == "Rock" and user_choice != "Paper":
            print("You lost.")
        elif computer_choice == "Paper" and user_choice != "Scissors":
            print("You lost.")
        elif computer_choice == "Scissors" and user_choice != "Rock":
            print("You lost.")
        else:
            print("You won!")
    else:
        print("It is a tie!")

# wraps all game functions into one that allows to play the game
def play():
    computer_choice = get_computer_choice()
    user_choice = get_user_choice()
    get_winner(computer_choice, user_choice)
        
play()