import cv2
import sys
import json
import time
import numpy as np
from keras.models import model_from_json
import CNN_MODEL as cnn    

emotion_labels = ['angry', 'fear', 'happy', 'sad', 'surprise', 'neutral']
cascPath = sys.argv[1]

faceCascade = cv2.CascadeClassifier(cascPath)

##load the model 
sess = cnn.Initialize() 

def predict_emotion(face_image_gray): # a single cropped face
    resized_img = cv2.resize(face_image_gray, (48,48), interpolation = cv2.INTER_AREA)
    # cv2.imwrite(str(index)+'.png', resized_img)
   ## image = resized_img.reshape(1, 1, 48, 48)
    list_of_list = cnn.Predict(resized_img,sess)
    angry, fear, happy, sad, surprise, neutral, unknown = [prob for lst in list_of_list for prob in lst]
    return [angry, fear, happy, sad, surprise, neutral, unknown]

video_capture = cv2.VideoCapture(0)
while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY,1)


    faces = faceCascade.detectMultiScale(
        img_gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags= cv2.CASCADE_SCALE_IMAGE
    )

    emotions = []
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        face_image_gray = img_gray[y:y+h, x:x+w]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        angry, fear, happy, sad, surprise, neutral, unknown = predict_emotion(face_image_gray)
        list1 = ["angry","fear","happy","sad","surprise","neutral", "unknown"]
        list2 = [angry,fear,happy,sad,surprise,neutral, unknown]
        print (list1[list2.index(max(list2))])


    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):      ## character q means exit
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
