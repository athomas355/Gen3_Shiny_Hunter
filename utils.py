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
prev_gray = None
sparkle_history = [] 
encounter = 0
log_file = "shiny_log.txt"

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
def detect_sparkle(frame):
    global prev_gray, sparkle_history

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Bright sparkle color range (while/yellow stars)
    lower = np.array([20, 100, 200])
    upper = np.array([40, 255, 255])

    mask_color = cv2.inRange(hsv, lower, upper)

    # Convert to grayscale for motion detection
    gray = cv2.cvtColor(get_pokemon_region(frame), cv2.COLOR_BGR2GRAY)
    
    if prev_gray is None or prev_gray.shape != gray.shape:
        prev_gray = gray
        return False

    # Frame difference (motion detection)
    diff = cv2.absdiff(gray, prev_gray)
    _, motion_mask = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    prev_gray = gray

    # Ensure same type
    motion_mask = motion_mask.astype(np.uint8)
    mask_color = mask_color.astype(np.uint8)

    # Ensure same size (extra safety)
    if mask_color.shape != motion_mask.shape:
        motion_mask = cv2.resize(motion_mask, (mask_color.shape[1], mask_color.shape[0]))


    # Combine: bright AND moving
    sparkle_mask = cv2.bitwise_and(mask_color, motion_mask)

    # Count sparkle pixels
    sparkle_pixels = cv2.countNonZero(sparkle_mask)

    #print("Sparkle pixels:", sparkle_pixels)

    # Track history (last few frames)
    sparkle_history.append(sparkle_pixels)
    if len(sparkle_history) > 10:
        sparkle_history.pop(0)

    # Detect spike pattern
    if len(sparkle_history) >= 3:
        prev_vals = sparkle_history[:-1]
        current = sparkle_history[-1]

        avg_prev = np.mean(prev_vals)

        # Spike condition
        if current > avg_prev * 2.5 and current > 50:
            print("✨ SHINY DETECTED ✨")
            return True
    
    return False

# ---------------------------------------
# FUNCTION: 📷 Get Pokemon Region; 64x64 pixels
# ---------------------------------------
def get_pokemon_region(frame):
    height, width, _ = frame.shape

    return frame [
        int(height * 0.1):int(height * 0.5),
        int(width * 0.55):int(width * 0.82)
    ]
    
# ---------------------------------------
# FUNCTION: ✨ Detect Shiny Pokemon
# ---------------------------------------
def is_shiny(frame, duration=5):
    global encounter

    start_time = time.time()
    #prev_frame = None

    while time.time() - start_time < duration:
        frame = capture_emulator()

        region = get_pokemon_region(frame)

        is_sparkle = detect_sparkle(region)

        #print("Bright pixels:", count)

        if is_sparkle:
            print("✨ SHINY DETECTED ✨")
            shiny_log(f"!!**SHINY FOUND at encounter #{encounter}**!!")
            return True

        #prev_frame = region
        time.sleep(0.03)  # ~30 FPS

    return False

# ---------------------------------------
# FUNCTION: 💫 Spin in Place
# ---------------------------------------
def spin_in_place():
    for d in ['up', 'down']:
        pyautogui.keyDown(d)
        pyautogui.keyUp(d)

# ---------------------------------------
# FUNCTION: ⚔️ Battle Detection
# ---------------------------------------
def is_in_battle(frame):
    global encounter

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

    if count > 5000:
        encounter += 1
        shiny_log(f"Encounter #{encounter}")

    return count > 5000

# ---------------------------------------
# FUNCTION: 🏃‍♂️‍➡️ Run from Battle
# ---------------------------------------
def run_from_battle():

    # Pressing A through the dialogue
    time.sleep(4) # Could probably adjust
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(2) # Could probably adjust
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(1)

    #right
    pyautogui.keyDown('right')
    pyautogui.keyUp('right')

    #down
    pyautogui.keyDown('down')
    pyautogui.keyUp('down')

    #confirm
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(2)

    #confirm 2
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')
    time.sleep(3)

# ---------------------------------------
# FUNCTION: Log Function
# ---------------------------------------
def shiny_log(message):
    timestamp = time.strftime("%H:%M:%S")
    full_message = f"[{timestamp}] {message}"

    print(full_message)

    with open(log_file, "a") as f:
        f.write(full_message + "\n")

# ---------------------------------------
# FUNCTION: Time Elapsed
# ---------------------------------------
def get_elapsed_time(end_time, start_time):
    elapsed = int(end_time - start_time)

    hours = elapsed // 3600
    minutes = (elapsed % 3600) // 60
    seconds = elapsed % 60

    return f"{hours:02}:{minutes:02}:{seconds:02}"
    

# ---------------------------------------
# FUNCTION: 🪲 Debug Window
# ---------------------------------------
def check_frame(frame):
    cv2.imshow("Region", frame)
    cv2.waitKey(1)
    

