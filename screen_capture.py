import mss 
import numpy as np
import cv2

def capture_screen():
    with mss.mss() as sct:
        screen = sct.monitors[1]

        screen_width = screen["width"]
        screen_height = screen["height"]

        # 👇 Make this bigger or smaller
        capture_width = int(screen_width * 0.6)
        capture_height = int(screen_height * 0.7)

        # 👇 Center it
        left = int((screen_width - capture_width) / 2)
        top = int((screen_height - capture_height) / 2)

        monitor = {
            "top": top,
            "left": left,
            "width": capture_width,
            "height": capture_height
        }

        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        return frame

while True:
    frame = capture_screen()

    cv2.imshow("Screen", frame)

    #Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

