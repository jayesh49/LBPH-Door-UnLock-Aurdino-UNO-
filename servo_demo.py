import pyfirmata
import time 
import keyboard

port="COM3"

board = pyfirmata.Arduino(port)

angle = 90
da = 5

servo1 = board.get_pin('d:2:s')
servo1.write(angle)

def move_servo(angle):
    servo1.write(angle)
    
while True:

    if keyboard.is_pressed('a'): # check if a is pressed
        if angle + da < 180:     # check to make sure new angle will not exceed 180 degrees
            angle = angle + da   # if new angle is OK, change to it
            move_servo(angle)    # set servo position to new angle by calling the function we made earlier
            time.sleep(0.1)      # wait a little bit (0.1 seconds) before checking again
    
    elif keyboard.is_pressed('d'): 
        if angle - da > 0:         # check to make sure new angle will not exceed 0 degrees
            angle = angle - da     
            move_servo(angle)      
            time.sleep(0.1)        
    
    elif keyboard.is_pressed('w'): # if w is pressed, increase da by 1
        if da + 1 < 180:
            da = da + 1
            time.sleep(0.1)
   
    elif keyboard.is_pressed('s'): # if s is pressed, decrease da by 1
        if da - 1 > 0:
            da = da - 1
            time.sleep(0.1)
    
    elif keyboard.is_pressed('r'): # if r is pressed reset a and da
        angle = 90
        da = 5
        move_servo(angle)
        time.sleep(0.1) 

    elif keyboard.is_pressed('esc'): # if esc is pressed, quit script
        break
