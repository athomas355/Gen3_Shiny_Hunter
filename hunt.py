from utils import *

def hunt():

    # Command to start Shiny Hunt
    while True:
        cmd = input("Type 'hunt' to begin: ")

        if cmd.lower() == "hunt":
            break
    
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
    print("Start")

    # Hunt Sequence Loop starts
    try:
        while True:

            # Get Frame
            frame = capture_emulator()

            if frame is None:
                continue

            # Check if in Battle 
            if is_in_battle(frame):
                print("Battle detected!")

                # Pressing A through the dialogue
                time.sleep(4)
                pyautogui.keyDown('x')
                time.sleep(0.005)
                pyautogui.keyUp('x')
                time.sleep(2)
                pyautogui.keyDown('x')
                time.sleep(0.005)
                pyautogui.keyUp('x')
                time.sleep(1) #Probably need to adjust this for time for shiny detection

                # Check for Shiny

                # If: Shiny found; stop the Hunt

                # Else: No Shiny; run from battle 
                run_from_battle()
                
            # Else: Spin in Place
            spin_in_place()

    # Interrupt Loop and Stop the Hunt
    except KeyboardInterrupt:
        print("Stopped.")
    

if __name__ == "__main__":
    hunt()