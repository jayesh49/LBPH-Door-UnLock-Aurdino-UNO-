import cv2
import numpy as np
import pyfirmata
import time 


port="COM3"

board = pyfirmata.Arduino(port)

servo1 = board.get_pin('d:2:s')
servo1.write(0)


face_classifier = cv2.CascadeClassifier('haar.xml')
jayesh_model = cv2.face.LBPHFaceRecognizer_create()
jayesh_model.read('jayesh.yml')

def move_servo(angle):
    servo1.write(angle)

def face_detector(img, size=0.5):
    # Convert image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    if faces is ():
        return img, []
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
    return img, roi

# Open Webcam
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    image, face = face_detector(frame)
    try:
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        results = jayesh_model.predict(face)
        if results[1] < 500:
            confidence = int( 100 * (1 - (results[1])/400) )
            display_string = str(confidence) + '% Confident it is Jayesh'
        if confidence <= 88:
            cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2)   
        if confidence > 88:
            cv2.putText(image, "Opening Door: Welcome Jayesh", (100, 120), cv2.FONT_HERSHEY_COMPLEX, 1, (255,120,150), 2) 
            cv2.imshow('Face Recognition', image )
        if confidence > 90:
            move_servo(120)
            time.sleep(10)
            move_servo(0)
        
        else:
            cv2.putText(image, "I dont know,who r u?", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
            cv2.imshow('Face Recognition', image )

    except:
        cv2.putText(image, "No Face Found", (220, 120) , cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        cv2.putText(image, "looking for face", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        cv2.imshow('Face Recognition', image )
        pass
        
        
    if cv2.waitKey(1) == 13: #13 is the Enter Key
        break

    
cap.release()
cv2.destroyAllWindows() 