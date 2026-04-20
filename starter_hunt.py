from utils import *
from starter_utils import *

def starter_hunt():

    # Decide Starter
    while True:
        starter = input("Enter starter to hunt: ")

        if starter.lower() == "treecko" or starter.lower() == "torchic" or starter.lower() == "mudkip" or starter == "1" or starter == "2" or starter == "3":
            break
    
    click_into_window()

    # Check if encounter file is there and it has already started the hunt
    if os.path.exists("encounter_count.txt"):
        hunt_start_time = load_start_time()
        encounters = load_encounters()
    else:
        hunt_start_time = time.strftime("%H:%M:%S")
        encounters = 0
        with open("encounter_count.txt", "w") as f:

            f.write(f"[{hunt_start_time}] Shiny Hunt Started\n")

    print("Encounters start at: ", encounters)

    while True:
        # Reset game
        reset_game()


        # Select Starter
        select_starter(starter)

        # Wait for battle
        while True:
            frame = capture_emulator()
            if is_in_battle(frame):
                break
            time.sleep(3)

        # Increment Encounter
        encounters += 1
        
        encounter_log(f"Encounter # {encounters}")

        # Proceed to throwing out your pokemon 
        pyautogui.keyDown('x')
        print("hello I am here")
        pyautogui.keyUp('x')
        time.sleep(2)


        # Check for shiny
        shiny = is_shiny(frame, 1)

        if shiny:
            print("✨SHINY FOUND!!!!✨")
            shiny_log("\nshiny found")

            # End Hunt
            print("🛑 End Hunt")
            return
        
        else:
            print("Not shiny, resetting...")

        

if __name__ == "__main__":
    starter_hunt()