import cv2
import time
from keras.models import load_model
import numpy as np
import random

model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
class_names = open("labels.txt", "r").read().splitlines()

# counts down from 5 to 1 with each number printed
def countdown():
    start = time.time()
    print("Get ready!")
    print(5)
    time_to_print = [4, 3, 2, 1]
    while True:
        total = time.time() - start
        if total > 1 and total < 2 and 4 in time_to_print:
            print(4)
            time_to_print.pop(0)
        elif total > 2 and total < 3 and 3 in time_to_print:
            print(3)
            time_to_print.pop(0)
        elif total > 3 and total < 4 and 2 in time_to_print:
            print(2)
            time_to_print.pop(0)
        elif total > 4 and total < 5 and 1 in time_to_print:
            print(1)
            time_to_print.pop(0)
        elif total > 5:
            print("Show your hand!")
            break  

# gets random choice for computer
def get_computer_choice():
    choice_list =["Rock", "Paper", "Scissors"]
    return random.choice(choice_list)

def get_prediction():
    while True: 
        ret, frame = cap.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        data[0] = normalized_image
        prediction = model.predict(data)
        cv2.imshow('frame', frame)
        index = np.argmax(prediction)
        # Press q to close the window
        if cv2.waitKey(1) & 0xFF == ord('q') or index !=3 and prediction[0][index] > 0.8 :
            class_name = class_names[index]
            break
    return class_name

# compares computer_choice and user_choice and prints the outcome, both arguments are required
def get_winner(computer_choice, user_choice_prediction):
    winner = ""
    if computer_choice != user_choice_prediction:
        if computer_choice == "Rock" and user_choice_prediction != "Paper":
            print(f"You lost. Rock beats {user_choice_prediction}")
            winner = "computer"
            return winner
        elif computer_choice == "Paper" and user_choice_prediction != "Scissors":
            print(f"You lost. Paper beats {user_choice_prediction}")
            winner = "computer"
            return winner
        elif computer_choice == "Scissors" and user_choice_prediction != "Rock":
            print(f"You lost. Scissors beats {user_choice_prediction}")
            winner = "computer"
            return winner
        else:
            print(f"You won! {user_choice_prediction} beats {computer_choice}")
            winner = "user"
            return winner
    else:
            print(f"It is a tie! Both hands show {user_choice_prediction}")
            winner = "nobody"
            return winner

# wraps all game functions into one that allows to play the game
def play():
    user_wins = 0
    computer_wins = 0
    rounds_played = 0
    while user_wins < 3 and computer_wins < 3 and rounds_played < 5:
        countdown()
        user_choice_prediction = get_prediction()
        computer_choice = get_computer_choice()
        winner = get_winner(computer_choice, user_choice_prediction)
        if winner == "computer":
            computer_wins += 1
            rounds_played += 1
        elif winner == "user":
            user_wins += 1
            rounds_played += 1
        else:
            rounds_played += 1
    if computer_wins > user_wins:
        print("You lost 3 games!")
    elif user_wins > computer_wins:
        print("You won 3 games!")
    else:
        print("You have reached 5 rounds wihout a winner!")
play()
