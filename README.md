# Computer Vision RPS

# Milestone 1
Git Hub repository created for the Rock-Paper_Scissors game. The files created are:
- README.md
- RPS-Template.py #not yet explained/understood

# Milestone 2
Project will use the teachable machine deep learing model from Google. The model will collect data from the video camera and, when trained, detect the shown hand.
Class for each option (rock, paper, scissors or nothing) has been created and camera images collected. The number of images for each hand exceeds 100 and includes images of hands up close
and further away.
Model trained, files keras_model.h5 and labels.txt downloaded.

# Milestone 3
This part of the project has been aimed to install all the required dependencies and check that the model trained in the previous milestone works as expected.
The libraries installed include:
- opencv-python
- tensorflow # there are issues when running this on a older computers
- ipykernel

File RPS-Template.py is used to run the model with the use of the camera. Output is displayed in a NumPy array format, example:
[[0.8, 0.1, 0.05, 0.05]]
Each number from the array corresponds to a probability (between 0 and 1) that an input image shows: rock, paper, scissors or nothing respectively.

# Milestone 4
The game logic is created in manual_rps.py. This file does not make use of the pre-trained model, only manual input.
Functions created include:

get_computer_choice() - uses Python's random module to choose the computer's hand

get_user_choice() - asks the user to input their choice and validates it

get_winner() - takes two required arguments; computer choice and user choice, compares the hands and announces the winner (or a tie)

play() - this function encapsulates all the ones described above to simplify game initiation