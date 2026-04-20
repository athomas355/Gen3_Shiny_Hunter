import time
import pyautogui
import keyboard as kb

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
        time.sleep(0.5)
        
    if starter == "torchic" or starter == "2":
        pass

    if starter == "mudkip" or starter == "3":
        pyautogui.keyDown('right')
        pyautogui.keyUp('right')
        time.sleep(0.5)

    
    # Press on starter
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(1)

    # Confirm starter
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    
