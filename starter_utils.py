import time
import pyautogui
import cv2
import keyboard as kb

from utils import send_discord_message, send_discord_image

# ---------------------------------------
# CONFIGURATIONS
# ---------------------------------------
X_COORD = 305
Y_COORD = 200

# ---------------------------------------
# FUNCTION: Soft Reset Game
# ---------------------------------------
def reset_game():
    kb.press_and_release('ctrl+r')
    time.sleep(5)
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(1)
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(1)
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(1)
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(1)

# ---------------------------------------
# FUNCTION: Select Starter
# ---------------------------------------
def select_starter(starter):
    
    # Open bag
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(1)

    # Move to desired starter
    if starter == "treecko" or starter == "1":
        pyautogui.keyDown('left')
        pyautogui.keyUp('left') 
        
    if starter == "torchic" or starter == "2":
        pass

    if starter == "mudkip" or starter == "3":
        pyautogui.keyDown('right')
        pyautogui.keyUp('right')

    
    # Press on starter
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(0.5)

    # Confirm starter
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')

# ---------------------------------------
# FUNCTION: Soft Reset Game
# ---------------------------------------
def go_to_summary():

    pyautogui.keyDown('down')
    pyautogui.keyUp('down')
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(1)
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    pyautogui.keyDown('down')
    pyautogui.keyUp('down')
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')


# ---------------------------------------
# FUNCTION: 📷 Get Pokemon Region; 64x64 pixels
# ---------------------------------------
def get_sprite_region(frame):
    height, width, _ = frame.shape

    return frame [
        int(height * 0.2):int(height * 0.6),
        int(width * 0.11):int(width * 0.33)
    ]

# ---------------------------------------
# FUNCTION: Shiny Detection from Pokemon Summary 
# ---------------------------------------
def is_shiny_from_summary(frame):
    x, y = X_COORD, Y_COORD

    b, g, r = frame[y, x]

    target = (173, 239, 239)

    if b == target[0] and g == target[1] and r == target[2]:
        return True
    
    return False
    
'''
    cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
    cv2.imshow("Debug", frame)
    cv2.waitKey(1)
'''