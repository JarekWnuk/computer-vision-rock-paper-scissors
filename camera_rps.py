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
        self.rounds_played = 0

    # counts down from 5 to 1 with each number printed        
    def countdown(self):

        #start counting time
        start = time.time()

        print(f"Round {self.rounds_played + 1}!")

        #font set up
        font = cv2.FONT_HERSHEY_COMPLEX
        org = (50, 100)
        thickness = 1
        fontScale = 2
        fontColor = (0,0,0)
        lineType = cv2.LINE_AA

        while True:
            #capture frame from camera
            ret, frame = cap.read()

            #calculate total time elapsed
            total = time.time() - start

            if total > 0 and total < 1:
                cv2.putText(frame,"5", org, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(2)

            elif total > 1 and total < 2:
                cv2.putText(frame,"4", org, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(1)

            elif total > 2 and total < 3:
                cv2.putText(frame,"3", org, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(1)

            elif total > 3 and total < 4:
                cv2.putText(frame,"2", org, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(1)

            elif total > 4 and total < 5:
                cv2.putText(frame,"1", org, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(1)

            elif total > 5:
                org = (50, 100)
                cv2.putText(frame,f"Round {self.rounds_played + 1}!", org, font, fontScale, fontColor, thickness, lineType)
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

        while user_wins < 3 and computer_wins < 3 and self.rounds_played < 5:
            self.countdown()
            results = self.get_prediction()
            user_choice_prediction = results[0]
            computer_choice = self.get_computer_choice()
            winner = self.get_winner(computer_choice, user_choice_prediction)
            last_frame_recorded = results[1]

            #font set up
            font = cv2.FONT_HERSHEY_COMPLEX
            org = (50, 100)
            thickness = 1
            fontScale = 0.75
            fontColor = (0,0,0)
            lineType = cv2.LINE_AA

            if winner == "computer":

                cv2.putText(last_frame_recorded,"You lost!", org, font, fontScale, fontColor, thickness, lineType)
                cv2.putText(last_frame_recorded,f"{computer_choice} beats {user_choice_prediction}!", (50, 150), font, fontScale, fontColor, thickness, lineType)
                cv2.putText(last_frame_recorded,"Press any key to continue.", (50, 200), font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",last_frame_recorded)
                cv2.waitKey(0)
                computer_wins += 1
                self.rounds_played += 1
            elif winner == "user":
                
                cv2.putText(last_frame_recorded,"You win! Press any key to continue.", org, font, fontScale, fontColor, thickness, lineType)
                cv2.putText(last_frame_recorded,f"{user_choice_prediction} beats {computer_choice}!", (50, 150), font, fontScale, fontColor, thickness, lineType)
                cv2.putText(last_frame_recorded,"Press any key to continue.", (50, 200), font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",last_frame_recorded)
                cv2.waitKey(0)
                user_wins += 1
                self.rounds_played += 1
            else:

                cv2.putText(last_frame_recorded,"It is a tie!", org, font, fontScale, fontColor, thickness, lineType)
                cv2.putText(last_frame_recorded,f"Both hands show {user_choice_prediction}!", (50, 150), font, fontScale, fontColor, thickness, lineType)
                cv2.putText(last_frame_recorded,"Press any key to continue.", (50, 200), font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",last_frame_recorded)
                cv2.waitKey(0)
                self.rounds_played += 1


        if computer_wins == 3:
            print("You lost 3 games!")
            cv2.putText(results[1],"You lost the game! Press any key to exit.", org, font, fontScale, fontColor, thickness, lineType)
            cv2.imshow("frame",results[1])
            cv2.waitKey(0)

        elif user_wins == 3:
            print("You won 3 games!")
            cv2.putText(results[1],"You won the game! Press any key to exit.", org, font, fontScale, fontColor, thickness, lineType)
            cv2.imshow("frame",results[1])
            cv2.waitKey(0)

        elif self.rounds_played == self.rounds:
            print(f"You have reached {self.rounds} rounds wihout a winner!")
            print(f"You won {user_wins} games. \nComputer won {computer_wins} games.")
            cv2.putText(results[1],f"No winner in {self.rounds} rounds ! Press any key to exit.", org, font, fontScale, fontColor, thickness, lineType)
            cv2.imshow("frame",results[1])
            cv2.waitKey(0)

five_round_rps = RockPaperScissors(5)
five_round_rps.play()
