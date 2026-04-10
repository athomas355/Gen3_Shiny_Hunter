import mss
import numpy as np
import cv2
import pygetwindow as gw
import pyautogui
import time
import keyboard
from pynput import keyboard

# -----------------------------
# CONFIGURATION
# -----------------------------
pyautogui.FAILSAFE = True  # move mouse to top-left to stop
MOVE_DURATION = 0.00005        # duration of each movement in seconds
PAUSE_BETWEEN_MOVES = 0.2  # small pause to make movement smoother
running = True
'''
REFERENCE_COLORS = {
    "wurmple": np.array([90, 81, 206]),
    "zigzagoon": np.array([173, 154, 165]),
    "poochyena": np.array([41,65,74])
}

sprite_avg_colors = {
    name: get_average_color(img)
    for name, img in sprite_templates.items()
}
'''
sprite_templates = {
    "wurmple": cv2.imread("ruby_sapphire_sprites/265.png"),
    "zigzagoon": cv2.imread("ruby_sapphire_sprites/263.png"),
    "poochyena": cv2.imread("ruby_sapphire_sprites/261.png")
}
# -----------------------------
# FUNCTION: Get Emulator Window
# -----------------------------
def get_emulator_window():
    """
    Automatically finds the emulator window.
    Replace "GB Operator" with your emulator's window name.
    """
    for title in gw.getAllTitles():
        if "Playback" in title:  # replace with actual emulator title
            return gw.getWindowsWithTitle(title)[0]
    return None

# -----------------------------
# FUNCTION: Capture Emulator Screen
# -----------------------------
def capture_emulator():
    """
    Captures the emulator window dynamically.
    Returns a frame (numpy array) or None if window not found.
    """
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
    
# -----------------------------
# FUNCTION: HSV from {pokemon}.png files
# -----------------------------
def get_hsv_from_image(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #Filter low saturation; removes background
    mask = hsv[:, :, 1] > 50
    filtered = hsv[mask]

    if len(filtered) == 0:
        avg = hsv.mean(axis=(0, 1))
    else:
        avg = filtered.mean(axis=0)

    return avg

# ----------------------------- 
# FUNCTION: Move Character
# -----------------------------
def move(key, duration):
    """
    Presses and holds a key for `duration` seconds.
    """
    pyautogui.keyDown(key)
    time.sleep(duration)
    pyautogui.keyUp(key)
    time.sleep(PAUSE_BETWEEN_MOVES)

# -----------------------------
# FUNCTION: Tap Key
# -----------------------------
def tap(key):
    pyautogui.keyDown(key)
    time.sleep(0.01)
    pyautogui.keyUp(key)

# -----------------------------
# FUNCTION: Spin in place
# -----------------------------
def spin_in_place():
    for d in ['up', 'right', 'down', 'left']:
        print(d)
        tap(d)
        time.sleep(0.05)

# -----------------------------
# STOP LISTENER
# -----------------------------
def on_press(key):
    global running
    try:
        if key.char == 'q':
            print("Q pressed → stopping bot")
            running = False
    except AttributeError:
        if key == keyboard.Key.esc:
            print("ESC pressed → stopping bot")
            running = False

listener = keyboard.Listener(on_press=on_press)
listener.start()

# -----------------------------
# Function: Battle Detection
# -----------------------------
def is_in_battle(frame):
    """
    Detects if we are in a battle by checking the bottom text box area.
    """
    height, width, _ = frame.shape

    #bottom region of screen 
    region = frame[int(height * 0.75):height, 0:width]

    """
    #convert to grayscale
    gray = cv2.cvtColor(bottom_region, cv2.COLOR_BGR2GRAY)

    #get brightness average
    avg_brightness = gray.mean()
    print("Brightness: ", avg_brightness)
    return avg_brightness < 50
    """

    #Convert to numpy array
    region = np.array(region)

    #Detect teal/green textbox color rgba(107, 162, 165)
    lower = np.array([160, 160, 100])
    upper = np.array([170, 170, 110])

    mask = cv2.inRange(region, lower, upper)

    count = cv2.countNonZero(mask)

    #print("Pixel Count: ", count)
    return count > 5000

# -----------------------------
# Function: Run From Battle
# -----------------------------
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
    
# -----------------------------
# Function: Wait for Pokemon
# -----------------------------
def wait_for_pokemon(frame, timeout = 5):
    start = time.time()

    while time.time() - start < timeout:
        frame = capture_emulator()

        color = get_sample_color(frame)

        if not (color[1] > 200 and color[0] > 200):
            return frame
        
        time.sleep(0.1)
    
    return frame

# -----------------------------
# Function: Get Pokemon Region
# -----------------------------
def get_pokemon_region(frame):
    height, width, _ = frame.shape

    return frame[
        int(height * 0.2):int(height * 0.46),
        int(width * 0.55):int(width * 0.8)
    ]

def debug_pixel(frame):
    import cv2

    clone = frame.copy()

    h, w, _ = frame.shape

    # test point (we'll adjust this)
    x = int(w * 0.69)
    y = int(h * 0.40)

    color = frame[y, x]
    print("Pixel color:", color)

    # draw dot so you SEE where you're sampling
    cv2.circle(clone, (x, y), 5, (0, 0, 255), -1)

    cv2.imshow("Debug", clone)
    cv2.waitKey(1)

# -----------------------------
# Function: Get Sample Color
# -----------------------------
def get_sample_color(frame):
    height, width, _ = frame.shape

    x = int(width * 0.69)
    y = int(height * 0.40)

    return frame[y, x]


# -----------------------------
# Function: Get Average Color
# -----------------------------
def get_average_color(region):
    # return np.mean(region, axis=(0,1))

    #Convert to HSV
    hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)

    #Filter Low Saturation; Removes background/white/gray
    mask = hsv[:, :, 1] > 50 
    filtered = hsv[mask]

    if len(filtered) == 0:
        return hsv.mean(axis=(0, 1))
    
    return filtered.mean(axis=(0))



# -----------------------------
# Function: HSV Distance
# -----------------------------
def hsv_distance(a, b):
    #Hue circular distance
    dh = min(abs(a[0] - b[0]), 180 - abs(a[0] - b[0]))

    #saturation + value difference 
    ds = abs(a[1] - b[1])
    dv = abs(a[2] - b[2])

    return dh * 2  + ds * 0.5 + dv * 0.2 #weighted

# -----------------------------
# Function: Match {Pokemon}.png template over pokemon region to see best fit
# -----------------------------
def match_template(frame):

    # Convert to grayscale; template matching works best in grayscale
    gray_region = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    scores = {}

    for name, template in sprite_templates.items():
        if template is None:
            print(f"Template missing for {name}")
            continue
    
        # Convert template to grayscale
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Resize template to match region scale
        th, tw = gray_template.shape

        #Skip if template is bigger than region 
        if th > gray_region.shape[0] or tw > gray_region.shape[1]:
            continue

        # Template Matching
        result = cv2.matchTemplate(gray_region, gray_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        scores[name] = max_val

    return scores

# -----------------------------
# Function: Identify Pokemon
# -----------------------------
def identify_pokemon(frame):
    
    # Wait for Pokemon to appear and the frame to settle
    frame = capture_emulator()
    frame = wait_for_pokemon(frame)
    region = get_pokemon_region(frame)

    #debug frame 
    cv2.imshow("Frame", region)
    cv2.waitKey(1)

    #get best template match
    template_scores = match_template(region)
    best_template_match = max(template_scores, key=template_scores.get)

    # Average the pokemon frame colors
    color = get_average_color(region)

    print("Average HSV Color of Pokemon Region: ", color)

    # Compare against references 
    color_scores = {}
    for name, ref in REFERENCE_COLORS.items():
            color_scores[name] = hsv_distance(color, ref)
        
    
    # Pick best match 
    best_color_match = min(color_scores, key=color_scores.get)

    print("Scores: ", color_scores)
    print("HSV Detected: ", best_color_match)
    print("Template Detected: ", best_template_match)

    return best_color_match, best_template_match, color_scores

# -----------------------------
# Function: Shiny Detection
# -----------------------------
def is_shiny(frame, pokemon_name, threshold = 40):
    #avg_color = get_average_color(region)
    color = get_sample_color(frame)
    ref_color = REFERENCE_COLORS[pokemon_name]

    diff = np.linalg.norm(color - ref_color)

    print(f"{pokemon_name} diff: ", diff)
    
    return diff > threshold

# -----------------------------
# MAIN PROGRAM
# -----------------------------
# Wait for user to type 'start'
'''
sprite_avg_colors = {
    name: get_average_color(img)
    for name, img in sprite_templates.items()
}
''' 

REFERENCE_COLORS = {
    name: get_hsv_from_image(img)
    for name, img in sprite_templates.items()
}

while True:
    command = input("Type 'start' to begin movement: ").strip().lower()
    if command == "start":
        break

print("Starting in 3 seconds... click into your emulator!")
time.sleep(3)

try:
    while running:
        frame = capture_emulator()

        if frame is None:
            continue

        if is_in_battle(frame):
            print("Battle detected!")

            time.sleep(4)
            
            pyautogui.keyDown('x')
            time.sleep(0.005)
            pyautogui.keyUp('x')
            time.sleep(2)
            pyautogui.keyDown('x')
            time.sleep(0.005)
            pyautogui.keyUp('x')
            time.sleep(1) #Probably need to adjust this for time for shiny detection might not matter

            #if not Shiny then run else if shiny then stop the program
            frame = wait_for_pokemon(frame)
            #print("pixel")
            #debug_pixel(frame)
            #region = get_pokemon_region(frame)
            #name, score = identify_pokemon(frame)
            print("Sprite Average HSV Colors: ", REFERENCE_COLORS)
            hsv_name, template_name, scores = identify_pokemon(frame)
            print("HSV Detected: ", hsv_name, "Template Detected: ", template_name, "Scores: ", scores)
            '''
            if is_shiny(region, name):
                frame = wait_for_pokemon(frame)
                print("pixel")
                debug_pixel(frame)
                region = get_pokemon_region(frame)
                print("Reference Color: ", get_sample_color(region))
                print("✨ SHINY FOUND! STOPPING BOT ✨")
                running = False
                break
            else:
                frame = wait_for_pokemon(frame)
                print("pixel")
                debug_pixel(frame)
                region = get_pokemon_region(frame)
                print("Reference Color: ", get_sample_color(region))
                run_from_battle()
                continue
            '''
            run_from_battle() #get rid of this
        '''
        # Move character
        time.sleep(PAUSE_BETWEEN_MOVES)
        move('right', MOVE_DURATION)
        move('down', MOVE_DURATION)
        move('left', MOVE_DURATION)
        move('up', MOVE_DURATION)
        '''
        #spin in place
        
        spin_in_place()

        """
        #Optional: display emulator capture
        if frame is not None:
            cv2.imshow("Emulator Capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quit requested")
                break
        """

except KeyboardInterrupt:
    print("Stopping bot...")


finally:
    #keyboard.unhook_all()
    listener.stop()
    print("bot has stopped.")

"""
cv2.destroyAllWindows()
"""