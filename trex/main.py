import numpy as np
import time
import matplotlib.pyplot as plt
import pyautogui
from skimage.measure import regionprops, label
from skimage.morphology import * 
import cv2
import mss


size_screen = pyautogui.size()
pyautogui.PAUSE = 0.0001                                                                                         
def enemy_here(binary):
    area = binary[130:150  ,390:423]
    # plt.imshow(area)  
    # plt.show()                                                                        
    if len(regionprops(label(area))) > 0 :
        pyautogui.keyUp('down')    
        pyautogui.press('space')   
        time.sleep(0.25 ) 
        pyautogui.keyDown   ( 'down')   
        #  
         
                 
           
             
is_down_pressed = False                          
 
monitor = {'left': 300, 'top': 300, 'width': 426, 'height': 145}
print("AAAAAAAAAAAAAAAA")
time.sleep(2)
start_time = time.time()


while True:
    with mss.mss() as sct:
        screenshot = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(frame, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            
            # Гарантируем, что клавиша вниз нажата
        if not is_down_pressed:
            pyautogui.keyDown('down')
            is_down_pressed = True

        enemy_here(binary)                  
     