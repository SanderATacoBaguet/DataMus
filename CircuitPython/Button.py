import time
import board
import digitalio
import usb_hid
from adafruit_hid.mouse import Mouse

# Initialize the mouse
mouse = Mouse(usb_hid.devices)

# Define GPIO pins for buttons
LEFT_CLICK_PIN = board.GP2     # Left mouse button (Button 1)
RIGHT_CLICK_PIN = board.GP3    # Right mouse button (Button 2)
BACK_BUTTON_PIN = board.GP4    # Browser Back
FORWARD_BUTTON_PIN = board.GP5 # Browser Forward

# Function to set up buttons
def setup_button(pin):
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP  # Uses an internal pull-up resistor
    return button

# Initialize buttons
left_click = setup_button(LEFT_CLICK_PIN)
right_click = setup_button(RIGHT_CLICK_PIN)
back_button = setup_button(BACK_BUTTON_PIN)
forward_button = setup_button(FORWARD_BUTTON_PIN)

# Main loop to check for button presses
while True:
    if not left_click.value:  # Button pressed (active LOW)
        mouse.press(Mouse.LEFT_BUTTON)
        time.sleep(0.1)  # Debounce delay
        mouse.release(Mouse.LEFT_BUTTON)

    if not right_click.value:
        mouse.press(Mouse.RIGHT_BUTTON)
        time.sleep(0.1)
        mouse.release(Mouse.RIGHT_BUTTON)

    if not back_button.value:
        mouse.press(Mouse.BUTTON_4)  # Backward navigation button
        time.sleep(0.1)
        mouse.release(Mouse.BUTTON_4)

    if not forward_button.value:
        mouse.press(Mouse.BUTTON_5)  # Forward navigation button
        time.sleep(0.1)
        mouse.release(Mouse.BUTTON_5)

    time.sleep(0.01)  # Small delay to avoid excessive CPU usage
