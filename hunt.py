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
    hunt_start_time = time.time()
    shiny_log("Shiny hunt started")

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

                
                # Check for Shiny
                shiny = is_shiny(frame)

                # If: Shiny found; stop the Hunt
                if shiny:
                    print("✨SHINY FOUND!!!!✨")
                    hunt_end_time = time.time()
                    shiny_log((f"!!**SHINY FOUND at encounter #{encounter} after {get_elapsed_time(hunt_end_time, hunt_start_time)}**!!"))
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
    

if __name__ == "__main__":
    hunt()