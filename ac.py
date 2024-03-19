# importing time and threading
import time
import threading
from pynput.mouse import Button, Controller

# pynput.keyboard is used to watch events of keyboard for start and stop of auto-clicker
from pynput.keyboard import Listener, KeyCode, Key

# four variables are created to control the auto-clicker
delay = 20.0
# sword_slot_number = KeyCode(char="1")
# food_slot_number = KeyCode(char="3")
start_stop_key = KeyCode(char="`")
quit_key = Key.f4


# threading.Thread is used to control clicks
class ClickMouse(threading.Thread):
    # delay and button is passed in class to check execution of auto-clicker
    def __init__(self, delay):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button_attack = Button.left
        self.running = False
        self.program_running = True

        ### For Food!! ###
        # self.food_slot_number = food_slot_number
        # self.sword_slot_number = sword_slot_number
        self.hit_count = 0
        self.hit_limit = 99999

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    # method to check and run loop until it is true another loop will check
    # if it is set to true or not, for mouse click it set to button and delay.
    def run(self):
        while self.program_running:
            while self.running:
                try:
                    # Eat if the hit count is over a limit
                    if self.hit_count >= self.hit_limit:
                        # Swap to the food slot in the hotbar
                        #mouse.click(button=self.food_slot_number)
                        #kb.press(food_slot_number)

                        # Hold right click to eat and sleep for 3 seconds
                        print(
                            f"Eating using SLOT #{str(self.food_slot_number)}"
                        )
                        mouse.press(Button.right)
                        time.sleep(3)
                        mouse.release(Button.right)
                        # reset the hit count
                        self.hit_count = 0

                    # If we dont need to eat, just attack
                    mouse.click(self.button_attack)
                    self.hit_count += 1
                    print(f"Clicked button: {str(self.button_attack)} (hit #{str(self.hit_count)})")
                    time.sleep(self.delay)
                except Exception as ex:
                    print(f"[ERROR] EXCEPTION: {str(ex)}")
                    click_thread.exit()
                    listener.stop()
            time.sleep(0.1)


# instance of mouse controller is created
mouse = Controller()
#kb = Controller()
click_thread = ClickMouse(delay)
click_thread.start()


# on_press method takes key as argument
def on_press(key):

    # start_stop_key will stop clicking if running fblag is set to true
    if key == start_stop_key:
        if click_thread.running:
            click_thread.stop_clicking()
            print("Paused.")
        else:
            print("Starting...")
            click_thread.start_clicking()

    # here exit method is called and when key is pressed it terminates auto clicker
    elif key == quit_key:
        print("Exiting...")
        click_thread.exit()
        listener.stop()
        exit(0)


with Listener(on_press=on_press) as listener:
    listener.join()
