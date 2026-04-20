import mss
import numpy as np
import cv2
import pygetwindow as gw
import pyautogui
import time
import os
import requests
import keyboard as kb
from pynput import keyboard


# -----------------------------
# CONFIGURATIONS
# -----------------------------
prev_gray = None
sparkle_history = [] 
WEBHOOK_URL = "https://discord.com/api/webhooks/1493433569211846677/xOPN6NSOKOR_rq2Bh3N7ZxXHxEEImATG6p11DVstH2uboQ4n4zqVh_abdzfGUbwdr2e_"
EXIT_PROGRAM = False
# -----------------------------
# FUNCTION: 🪟 Get Emulator Window
# -----------------------------
def get_emulator_window():
    
    for title in gw.getAllTitles():
        if "Playback" in title or "mGBA" in title:  # replace with actual emulator title
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
# FUNCTION: 📷 Get Pokemon Region; 64x64 pixels
# ---------------------------------------
def get_starter_region(frame):
    height, width, _ = frame.shape

    return frame [
        int(height * 0.3):int(height * 0.72),
        int(width * 0.2):int(width * 0.5)
    ]
    
# ---------------------------------------
# FUNCTION: ✨ Detect Shiny Pokemon
# ---------------------------------------
def is_shiny(frame, starter=0, duration=5):
    global encounters

    start_time = time.time()
    #prev_frame = None

    while time.time() - start_time < duration:
        frame = capture_emulator()

        if starter == 1:
            region = get_starter_region(frame)
            check_frame(region)
        else:
            region = get_pokemon_region(frame)

        is_sparkle = detect_sparkle(region)

        #print("Bright pixels:", count)

        if is_sparkle:
            if starter == 1:
                filename = f"shiny_found.png"
                cv2.imwrite(filename, get_starter_region(frame))
                send_discord_image(filename)
            else: 
                filename = f"shiny_found.png"
                cv2.imwrite(filename, get_pokemon_region(frame))
                send_discord_image(filename)
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
# FUNCTION: Stop Listener
# ---------------------------------------
def on_press(key):
    try:
        if key.char == 'q':
            print("Q pressed → stopping bot")
            return KeyboardInterrupt
    except AttributeError:
        if key == keyboard.Key.esc:
            print("ESC pressed → stopping bot")
            return KeyboardInterrupt

# ---------------------------------------
# FUNCTION: ⚔️ Battle Detection
# ---------------------------------------
def is_in_battle(frame):
    global encounters

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
# FUNCTION: Load previous encounters or encounter = 0 
# ---------------------------------------
def load_encounters():
    if os.path.exists("encounter_count.txt"):
        with open("encounter_count.txt", "r") as f:
            content = get_last_line("encounter_count.txt")
            content_arr = content.split()

            if content:
                return int(content_arr[3])
            else:
                print("⚠️ Invalid encounter file, resetting to 0")
                return 0
    return 0

# ---------------------------------------
# FUNCTION: Load previous encounters or encounter = 0 
# ---------------------------------------
def load_start_time():
    if os.path.exists("encounter_count.txt"):
        with open("encounter_count.txt", "r") as f:
            line = f.readline()

            if line:
                return line.split()[0]
            else:
                print("⚠️ Invalid encounter file, resetting to 0")
                return 0
    return 0

# ---------------------------------------
# FUNCTION: save encounters
# ---------------------------------------
def save_encounters(count):
    with open("encounter_count.txt", "w") as f:
        f.write(str(count))

# ---------------------------------------
# FUNCTION: Encounter Log Function
# ---------------------------------------
def encounter_log(message):
    with open("encounter_count.txt", "r") as f:
        lines = f.readlines()

    if len(lines) == 1:
        hunt_start_time = time.strftime("%H:%M:%S")
        full_message = f"[{hunt_start_time}] Encounter # 1"
        with open("encounter_count.txt", "w") as f:
            lines.append(full_message)
            f.writelines(lines)
            return

    timestamp = time.strftime("%H:%M:%S")
    full_message = f"[{timestamp}] {message}"

    print(full_message)
    if len(lines) >= 2:
        lines[1] = full_message

    with open("encounter_count.txt", "w") as f:
        f.writelines(lines)

# ---------------------------------------
# FUNCTION: Shiny Log Function
# ---------------------------------------
def shiny_log(message):
    with open("encounter_count.txt", "r") as f:
        lines = f.readlines()

    if len(lines) == 2:
        full_message = f"{message}"
        with open("encounter_count.txt", "w") as f:
            lines.append(full_message)
            f.writelines(lines)
            return

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
# FUNCTION: Get Last line of txt file
# ---------------------------------------
def get_last_line(filename):
    with open(filename, 'rb') as f:
        try:
            # Seek to the second to last byte (avoiding a trailing newline)
            f.seek(-2, os.SEEK_END)
            # Read backward until a newline character is found
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            # Handle files with only one line by seeking to the start
            f.seek(0)
        
        return f.readline().decode().strip()
    
# ---------------------------------------
# FUNCTION: Discord Notification
# ---------------------------------------
def send_discord_message(message):

    message = "✨ " + message + " ✨"
    data = {
        "content": message
    }

    requests.post(WEBHOOK_URL, json=data)

# ---------------------------------------
# FUNCTION: Send Shiny Image to Discord
# ---------------------------------------
def send_discord_image(image_path):
    with open(image_path, "rb") as f:
        files = {"file": f}

        requests.post(WEBHOOK_URL, files=files)

# ---------------------------------------
# FUNCTION: Click into Window
# ---------------------------------------
def click_into_window():
    # Time to click into game window 
    print("Click into Game...")
    print("Beginning Hunt...")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("Shiny Hunt Started")

# ---------------------------------------
# FUNCTION: 🪲 Debug Window
# ---------------------------------------
def check_frame(frame):
    cv2.imshow("Region", frame)
    cv2.waitKey(1)
    

