import random

choice_list =["Rock", "Paper", "Scissors"]

# gets random choice for computer
def get_computer_choice():
    return random.choice(choice_list)

# asks user for choice
def get_user_choice():
    while True:
        choice = input("Choose from: rock, paper, scissors:\n")
        if choice.capitalize() in choice_list:
            break
        else:
            print("Incorrect input, try again.")
            continue
    return choice.capitalize()

get_computer_choice()
get_user_choice()