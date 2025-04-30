import board
import digitalio
import usb_hid
from adafruit_hid.mouse import Mouse
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialize HID devices
mouse = Mouse(usb_hid.devices)
keyboard = Keyboard(usb_hid.devices)

# Define GPIO pins for buttons
button_pins = [board.GP14, board.GP15, board.GP16, board.GP17]

# Map buttons to actions
button_actions = {
    0: "LEFT_CLICK",           # GPIO14 -> Left Mouse Button
    1: "RIGHT_CLICK",          # GPIO15 -> Right Mouse Button
    2: "FORWARD_NAV",          # GPIO16 -> Browser Forward
    3: "BACKWARD_NAV"          # GPIO17 -> Browser Back
}

# Initialize buttons as inputs with pull-ups
buttons = []
for pin in button_pins:
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append(button)

# State tracking for debouncing
button_states = [False] * len(buttons)

print("Mouse and navigation handler ready!")

while True:
    for i, button in enumerate(buttons):
        # Check the current state of the button (active low)
        pressed = not button.value

        # If the button state has changed
        if pressed != button_states[i]:
            button_states[i] = pressed

            # Perform the action for the button
            if pressed:
                print(f"Button {i} pressed!")
                if button_actions[i] == "LEFT_CLICK":
                    mouse.press(Mouse.LEFT_BUTTON)
                elif button_actions[i] == "RIGHT_CLICK":
                    mouse.press(Mouse.RIGHT_BUTTON)
                elif button_actions[i] == "FORWARD_NAV":
                    keyboard.press(Keycode.ALT, Keycode.RIGHT_ARROW)  # ALT + Right Arrow for forward
                elif button_actions[i] == "BACKWARD_NAV":
                    keyboard.press(Keycode.ALT, Keycode.LEFT_ARROW)   # ALT + Left Arrow for back
            else:
                print(f"Button {i} released!")
                if button_actions[i] in ["LEFT_CLICK", "RIGHT_CLICK"]:
                    mouse.release(Mouse.LEFT_BUTTON if button_actions[i] == "LEFT_CLICK" else Mouse.RIGHT_BUTTON)
                elif button_actions[i] in ["FORWARD_NAV", "BACKWARD_NAV"]:
                    keyboard.release_all()
