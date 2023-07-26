import cv2
import time
from keras.models import load_model
import numpy as np
import random

class RockPaperScissors:
    '''
    This class is used to play the rock-paper-scissors game with the use of the camera.

    Attributes:
        rounds (int): number of rounds in the game, defaults to 3
        rounds_played (int): the number of rounds already played in the game, defaults to 0
        choices (list): a list of hand choices returned from the get_choice_list function
        cap (tuple): the image collected from the camera using the cv2 module as a NumPy array
        model: the model created from keras_model.h5 file using the keras module
    '''
    def __init__(self, rounds:int=3):
        '''
        See help(RockPaperScissors) for accurate signature
        '''
        self.rounds = rounds
        self.rounds_played = 0
        self.choices = self.get_choice_list()
        self.cap = cv2.VideoCapture(0)
        self.model = load_model('keras_model.h5')

    def get_choice_list(self):
        '''
        This method is used to extract a list of hand choices from labels.txt.

        Returns:
            class_names (list): a list of names of classes contained in labels.txt (Rock, Paper, Scissors and Nothing)
        '''
        with open("labels.txt", "r") as f:
            class_names = f.read().splitlines()
            f.close()
            return class_names
      
    def countdown(self):
        '''
        This method displays a countdown from 5 to 1 to the camera and announces the round number.
        
        With the use of the time module the start and total elapse time is calculated. This dictates
        which number is shown in the displayed frame. The effect is a fluent countdown with the camera
        view still displaying in real time. The round number is shown after 5 seconds have passed.

        Returns:
            None
        '''

        #start counting time
        start = time.time()

        #font set up
        font = cv2.FONT_HERSHEY_COMPLEX
        org = (50, 100)
        thickness = 1
        fontScale = 2
        fontColor = (0, 0, 0)
        lineType = cv2.LINE_AA

        while True:
            #capture frame from camera
            ret, frame = self.cap.read()

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
                print(f"Round {self.rounds_played + 1}!")
                org = (50, 100)
                cv2.putText(frame,f"Round {self.rounds_played + 1}!", org, font, fontScale, fontColor, thickness, lineType)
                cv2.imshow("frame",frame)
                cv2.waitKey(500)
                break  

    # gets random choice for computer
    def get_computer_choice(self):
        '''
        This method generates a choice of hand for the computer.

        The computer choice is a random selection from the choices list excluding the last
        item: Nothing.

        Returns:
            random item from choice_list (str): a random choice of hand from choice_list
        '''
        choice_list = self.choices[:3]
        return random.choice(choice_list)

    def get_prediction(self):
        '''
        This method uses the loaded model to predict which hand is shown to the camera
        by the player. 

        The predicted class is accepted if the probability calculated by the model exceeds 80%.

        Returns:
            class_name (str)
        '''
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        while True: 
            ret, frame = self.cap.read()
            resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
            image_np = np.array(resized_frame)
            normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
            data[0] = normalized_image
            prediction = self.model(data)
            cv2.imshow('frame', frame)
            index = np.argmax(prediction)
            # Press q to close the window
            if cv2.waitKey(1) & 0xFF == ord('q') or index !=3 and prediction[0][index] > 0.8 :
                class_name = self.choices[index]
                break
        return class_name, frame

    # compares computer_choice and user_choice and prints the outcome, both arguments are required
    def get_winner(self, computer_choice, user_choice_prediction):
        '''
        This method uses game rules to check who is the winner of the round.
        
        Args:
            computer_choice (str): choice of hand for the computer
            user_choice_prediction (str): choice of hand for the player

        Returns:
            winner (str): the winner of the round
        '''
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

    def play(self):
        '''
        This method is used to initiate gameplay.

        The game is run in the following sequence:
            1. Countdown from 5 to 1.
            2. Get the predicted choice of hand for the player.
            3. Generate a random choice of hand for the computer.
            4. Check who is the winner.
            5. Display the result to the camera image.
        This sequence is repeated until either the player or computer get 3 wins or
        the maximum defined number of rounds is reached.
        Finally, the end game result is displayed to the camera image.
        
        Returns:
            None
        '''
        user_wins = 0
        computer_wins = 0

        while user_wins < 3 and computer_wins < 3 and self.rounds_played < self.rounds:
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
            fontColor = (0, 0, 0)
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
                cv2.putText(last_frame_recorded,"You win!", org, font, fontScale, fontColor, thickness, lineType)
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
            ret, frame = self.cap.read()
            cv2.putText(frame,"You lost the game! Press any key to exit.", org, font, fontScale, fontColor, thickness, lineType)
            cv2.imshow("frame",frame)
            cv2.waitKey(0)

        elif user_wins == 3:
            print("You won 3 games!")
            ret, frame = self.cap.read()
            cv2.putText(frame,"You won the game! Press any key to exit.", org, font, fontScale, fontColor, thickness, lineType)
            cv2.imshow("frame",frame)
            cv2.waitKey(0)

        elif self.rounds_played == self.rounds:
            print(f"You have reached {self.rounds} rounds wihout a winner!")
            print(f"You won {user_wins} games. \nComputer won {computer_wins} games.")
            ret, frame = self.cap.read()
            cv2.putText(frame,f"No winner in {self.rounds} rounds !", org, font, fontScale, fontColor, thickness, lineType)
            cv2.putText(frame,"Press any key to exit.", (50, 150), font, fontScale, fontColor, thickness, lineType)
            cv2.imshow("frame",frame)
            cv2.waitKey(0)

if __name__ == "__main__":
    five_round_rps = RockPaperScissors(5)
    five_round_rps.play()
