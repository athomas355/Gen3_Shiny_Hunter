from utils import *

listener = keyboard.Listener()
listener.start()

def hunt():

    # Command to start Shiny Hunt
    while True:
        cmd = input("Type 'hunt' to begin: ")

        if cmd.lower() == "hunt":
            break
    
    click_into_window()

    # Check if encounter file is there and it has already started the hunt
    if os.path.exists("encounter_count.txt"):
        hunt_start_time = load_start_time()
        encounters = load_encounters()
    else:
        hunt_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        encounters = 0
        with open("encounter_count.txt", "w") as f:

            f.write(f"[{hunt_start_time}] Shiny Hunt Started\n")

    
    print("Encounters start at: ", encounters)

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
                encounters += 1 
                encounter_log(f"Encounter # {str(encounters)}")

                
                # Check for Shiny
                shiny = is_shiny(frame)

                # If: Shiny found; stop the Hunt
                if shiny:
                    print("✨SHINY FOUND!!!!✨")
                
                    # send notification message to discord
                    hunt_end_time = datetime.now()
                    shiny_found_msg = f"\n!!**SHINY FOUND at encounter # {encounters} after {get_elapsed_time(hunt_end_time, hunt_start_time)}**!!"
                    shiny_log((shiny_found_msg))
                    send_discord_message(shiny_found_msg)

                    # End Hunt
                    print("🛑 End Hunt")
                    return
                
                # Else: No Shiny; run from battle 
                else:
                    print("Not shiny, running...")
                    run_from_battle()
                
            # Else: Spin in Place
            spin_in_place()

    # Interrupt Loop and Stop the Hunt
    except KeyboardInterrupt:
        print("Hunt Ended")

    finally:
        listener.stop()

if __name__ == "__main__":
    hunt()