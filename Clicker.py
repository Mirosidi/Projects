import keyboard
import mouse
import time

Click = False

def clicker():
    global Click
    Click = not Click

keyboard.add_hotkey('W + s', clicker)

while True:
    if Click:
        mouse.click(button='left')
        time.sleep(0.1)