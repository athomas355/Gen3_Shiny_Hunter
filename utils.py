import mss
import numpy as np
import cv2
import pygetwindow as gw
import pyautogui
import time
import keyboard
from pynput import keyboard

# -----------------------------
# CONFIGURATIONS
# -----------------------------


# -----------------------------
# FUNCTION: 🪟 Get Emulator Window
# -----------------------------
def get_emulator_window():
    
    for title in gw.getAllTitles():
        if "Playback" in title:  # replace with actual emulator title
            return gw.getWindowsWithTitle(title)[0]
    return None

# -----------------------------
# FUNCTION: 📷 Capture Emulator Screen
# -----------------------------
def capture_emulator():

    win = get_emulator_window()
    if win is None:
        print("Emulator window not found")
        return None

    monitor = {
        "top": win.top,
        "left": win.left,
        "width": win.width,
        "height": win.height
    }

    with mss.mss() as sct:
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame
    
# ---------------------------------------
# FUNCTION: ✨ Detect Sparkle Animation
# ---------------------------------------
def detect_sparkle():
    return None

# ---------------------------------------
# FUNCTION: 📷 Get Pokemon Region; 64x64 pixels
# ---------------------------------------
def get_pokemon_region():
    return None

# ---------------------------------------
# FUNCTION: ✨ Detect Shiny Pokemon
# ---------------------------------------
def is_shiny():
    return None

# ---------------------------------------
# FUNCTION: 💫 Spin in Place
# ---------------------------------------
def spin_in_place():
    for d in ['up', 'right', 'down', 'left']:
        pyautogui.keyDown(d)
        time.sleep(0.016)
        pyautogui.keyUp(d)
        time.sleep(0.05)

# ---------------------------------------
# FUNCTION: ⚔️ Battle Detection
# ---------------------------------------
def is_in_battle(frame):
    height, width, _ = frame.shape

    #bottom region of screen 
    region = frame[int(height * 0.75):int(height * 0.95), int(width * 0.2):int(width * 0.8)]

    #Convert to numpy array
    region = np.array(region)

    #Detect teal/green textbox color rgba(107, 162, 165)
    lower = np.array([160, 160, 100])
    upper = np.array([170, 170, 110])

    mask = cv2.inRange(region, lower, upper)

    count = cv2.countNonZero(mask)

    return count > 5000

# ---------------------------------------
# FUNCTION: 🏃‍♂️‍➡️ Run from Battle
# ---------------------------------------
def run_from_battle():
    #right
    pyautogui.keyDown('right')
    time.sleep(0.005)
    pyautogui.keyUp('right')
    time.sleep(0.5)

    #down
    pyautogui.keyDown('down')
    time.sleep(0.005)
    pyautogui.keyUp('down')
    time.sleep(0.5)

    #confirm
    pyautogui.keyDown('x')
    time.sleep(0.005)
    pyautogui.keyUp('x')
    time.sleep(2)

    #confirm 2
    pyautogui.keyDown('x')
    time.sleep(0.005)
    pyautogui.keyUp('x')
    time.sleep(3)

# ---------------------------------------
# FUNCTION: 🪲 Debug Window
# ---------------------------------------
def check_frame(frame):
    cv2.imshow("Region", frame)
    cv2.waitKey(1)

