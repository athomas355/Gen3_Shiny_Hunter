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

        '''
        # Wait for battle
        while True:
            frame = capture_emulator()
            if is_in_battle(frame):
                break
        '''       
        time.sleep(8)

        # Proceed to throwing out your pokemon 
        pyautogui.keyDown('x')
        pyautogui.keyUp('x')

        # Increment Encounter
        encounters += 1
        encounter_log(f"Encounter # {encounters}")


        # Go to pokemon summary
        time.sleep(3.5)
        go_to_summary()
        time.sleep(1)

        
        # Check for shiny
        frame = capture_emulator()
        shiny = is_shiny_from_summary(frame)

        if shiny:
            print("✨SHINY FOUND!!!!✨")
            shiny_log("\nshiny found")
            hunt_end_time = time.time()
            shiny_found_msg = f"\n!!**SHINY FOUND at encounter # {encounters} after {get_elapsed_time(hunt_end_time, hunt_start_time)}**!!"

            filename = f"shiny_found.png"
            cv2.imwrite(filename, get_sprite_region(frame))
            send_discord_image(filename)
            send_discord_message(shiny_found_msg)

            # End Hunt
            print("🛑 End Hunt")
            return
        
        else:
            print("Not shiny, resetting...")

   

if __name__ == "__main__":
    starter_hunt()
