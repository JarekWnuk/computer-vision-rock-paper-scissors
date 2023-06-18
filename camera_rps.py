import cv2
import time
from keras.models import load_model
import numpy as np
import random

model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
class_names = open("labels.txt", "r").read().splitlines()

class RockPaperScissors:

    def __init__(self, rounds):
        self.rounds = rounds

    # counts down from 5 to 1 with each number printed        
    def countdown(self):
        start = time.time()
        print("Get ready!")
        font = cv2.FONT_HERSHEY_COMPLEX
        bottomLeftCornerOfText = (50,300)
        fontScale = 6
        fontColor = (0,191,255)
        thickness = 10
        lineType = 5
        total = time.time() - start
        while True:
            ret, frame = cap.read()
            total = time.time() - start

            if total > 0 and total < 1:
                cv2.putText(frame,"5", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(1)

            elif total > 1 and total < 2:
                cv2.putText(frame,"4", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(1)

            elif total > 2 and total < 3:
                cv2.putText(frame,"3", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(1)

            elif total > 3 and total < 4:
                cv2.putText(frame,"2", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(1)

            elif total > 4 and total < 5:
                cv2.putText(frame,"1", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(1)

            elif total > 5:
                bottomLeftCornerOfText = (10,100)
                thickness = 8
                fontScale = 2
                cv2.putText(frame,"Show your hand!", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(500)
                break  

    # gets random choice for computer
    def get_computer_choice(self):
        choice_list =["Rock", "Paper", "Scissors"]
        return random.choice(choice_list)

    def get_prediction(self):
        while True: 

            ret, frame = cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
            data[0] = normalized_image
            prediction = model(data)
            cv2.imshow('frame', frame)
            index = np.argmax(prediction)
            # Press q to close the window
            if cv2.waitKey(1) & 0xFF == ord('q') or index !=3 and prediction[0][index] > 0.8 :
                class_name = class_names[index]
                break
        return class_name, frame

    # compares computer_choice and user_choice and prints the outcome, both arguments are required
    def get_winner(self, computer_choice, user_choice_prediction):
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
    def play(self):
        user_wins = 0
        computer_wins = 0
        rounds_played = 0
        while user_wins < 3 and computer_wins < 3 and rounds_played < 5:
            self.countdown()
            results = self.get_prediction()
            user_choice_prediction = results[0]
            last_frame_recorded = results[1]
            computer_choice = self.get_computer_choice()
            winner = self.get_winner(computer_choice, user_choice_prediction)

            font = cv2.FONT_HERSHEY_COMPLEX
            bottomLeftCornerOfText = (10,100)
            thickness = 8
            fontScale = 2
            fontColor = (0,191,255)
            thickness = 10
            lineType = 5

            if winner == "computer":

                cv2.putText(last_frame_recorded,f"You lost! Press any key to continue.", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",last_frame_recorded)
                cv2.waitKey(0)
                computer_wins += 1
                rounds_played += 1
            elif winner == "user":
                
                cv2.putText(last_frame_recorded,f"You win! Press any key to continue.", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",last_frame_recorded)
                cv2.waitKey(0)
                user_wins += 1
                rounds_played += 1
            else:

                cv2.putText(last_frame_recorded,f"It is a tie! Press any key to continue.", bottomLeftCornerOfText, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",last_frame_recorded)
                cv2.waitKey(0)
                rounds_played += 1
        if computer_wins == 3:
            print("You lost 3 games!")
        elif user_wins == 3:
            print("You won 3 games!")
        elif rounds_played == self.rounds:
            print(f"You have reached {self.rounds} rounds wihout a winner!")
            print(f"You won {user_wins} games. \nComputer won {computer_wins} games.")

five_round_rps = RockPaperScissors(5)
five_round_rps.play()
