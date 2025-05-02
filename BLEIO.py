import time
import board
import busio
import digitalio
from PMW3360 import PMW3360
import usb_hid
from adafruit_hid.mouse import Mouse

# SPI pins
SCK_PIN = board.GP10
MOSI_PIN = board.GP11
MISO_PIN = board.GP12
CS_PIN = board.GP9

# Reset pin
RESET_PIN = board.GP2
reset_pin = digitalio.DigitalInOut(RESET_PIN)
reset_pin.direction = digitalio.Direction.OUTPUT

# Initialize PMW3360
sensor = PMW3360(SCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN)

# USB HID mouse
mouse = Mouse(usb_hid.devices)

# Constants
MOVEMENT_THRESHOLD = 2        # Filter basic noise
MAX_DELTA = 50                # Max speed
SMOOTHING_FACTOR = 0.3        # Some smoothing
CERTIFIED_MIN_MOVEMENT = 5    # Minimum valid movement for cursor move
SENSOR_DPI = 400              # Setting DPI to 400 for controlled movement

# Internal state
previous_dx, previous_dy = 0, 0

def reset_sensor():
    print("Resetting sensor...")
    reset_pin.value = False
    time.sleep(0.05)
    reset_pin.value = True
    time.sleep(0.05)

def initialize_sensor():
    print("Initializing sensor...")
    cpi_value = SENSOR_DPI  # Set DPI to 400
    success = sensor.begin(cpi=cpi_value)
    if success:
        print(f"Sensor initialized with CPI {cpi_value}")
    else:
        print("Sensor initialization failed.")
    return success

def read_motion_data():
    return sensor.read_burst()

# Setup
reset_sensor()
if not initialize_sensor():
    print("Retrying initialization...")
    reset_sensor()
    time.sleep(0.1)
    if not initialize_sensor():
        print("Failed to initialize sensor. Locking...")
        while True:
            pass

# Main Loop
while True:
    motion_data = read_motion_data()

    if motion_data:
        dx = motion_data['dx']
        dy = motion_data['dy']
        is_on_surface = motion_data['is_on_surface']

        # Handle wrap-around
        if dx >= 32768:
            dx -= 65536
        if dy >= 32768:
            dy -= 65536

        # Noise filter - ignore minor fluctuations
        if abs(dx) < MOVEMENT_THRESHOLD:
            dx = 0
        if abs(dy) < MOVEMENT_THRESHOLD:
            dy = 0

        # If there's no valid movement, don't register it
        if abs(dx) < CERTIFIED_MIN_MOVEMENT and abs(dy) < CERTIFIED_MIN_MOVEMENT:
            dx, dy = 0, 0
        else:
            # Apply smoothing to remove sudden spikes in movement
            dx = int(SMOOTHING_FACTOR * previous_dx + (1 - SMOOTHING_FACTOR) * dx)
            dy = int(SMOOTHING_FACTOR * previous_dy + (1 - SMOOTHING_FACTOR) * dy)

            # Update the previous values for the next iteration
            previous_dx, previous_dy = dx, dy

            # Ensure the movement doesn't exceed the max allowed speed (delta)
            dx = max(-MAX_DELTA, min(MAX_DELTA, dx))
            dy = max(-MAX_DELTA, min(MAX_DELTA, dy))

            # Move the mouse only when the movement is significant enough
            if abs(dx) >= CERTIFIED_MIN_MOVEMENT or abs(dy) >= CERTIFIED_MIN_MOVEMENT:
                print(f"Valid Movement: dx={dx}, dy={dy}")
                mouse.move(x=dx, y=dy)

    time.sleep(0.01)  # Sleep to reduce CPU load and control responsiveness

