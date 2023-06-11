import cv2
import time
from keras.models import load_model
import numpy as np

model = load_model('keras_model.h5')
cap = cv2.VideoCapture(0)
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
class_names = open("labels.txt", "r").readlines()

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

countdown()
user_hand = get_prediction()
print(f"You chose {user_hand}")
