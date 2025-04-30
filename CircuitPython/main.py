import time
import board
import busio
import digitalio
from PMW3360 import PMW3360  # Ensure this import matches your file structure
import usb_hid
from adafruit_hid.mouse import Mouse  # Import Mouse from adafruit_hid
pin = digitalio.DigitalInOut(board.GP16)  # Use an available pin (e.g., D0)
pin.direction = digitalio.Direction.OUTPUT

# Set up SPI pins
SCK_PIN = board.GP10  # Replace with your SCK pin
MOSI_PIN = board.GP11  # Replace with your MOSI pin
MISO_PIN = board.GP12  # Replace with your MISO pin
CS_PIN = board.GP9     # Replace with your CS pin

# Set up the reset pin
RESET_PIN = board.GP2   # Use GPIO pin 2 for reset
reset_pin = digitalio.DigitalInOut(RESET_PIN)
reset_pin.direction = digitalio.Direction.OUTPUT

# Initialize the PMW3360 sensor
sensor = PMW3360(SCK_PIN, MOSI_PIN, MISO_PIN, CS_PIN)

# Obtain the list of USB HID devices
devices = usb_hid.devices  # This gets the current list of HID devices

# Initialize Mouse for cursor movement with the list of devices
mouse = Mouse(devices)  # Pass the HID devices to the Mouse constructor

# Initialize parameters for movement tracking
MOVEMENT_THRESHOLD = 1    # Set an appropriate threshold for detecting movement
MAX_DELTA = 50            # Maximum allowed delta to filter out noise
SMOOTHING_FACTOR = 0.5    # A balance between responsiveness and smoothness

previous_dx, previous_dy = 0, 0  # Previous movement values for smoothing

def initialize_sensor():
    """Initialize the PMW3360 sensor."""
    cpi_value = 10000  # Set CPI (Counts Per Inch) value
    print("Initializing sensor...")
    if sensor.begin(cpi=cpi_value):
        print("Sensor initialized successfully with CPI:", cpi_value)
        return True
    else:
        print("Sensor initialization failed.")
        return False

def reset_sensor():
    """Reset the PMW3360 sensor by toggling the reset pin."""
    print("Resetting sensor...")
    reset_pin.value = False  # Set reset pin low
    time.sleep(0.1)          # Hold low for a short duration (100 ms)
    reset_pin.value = True   # Set reset pin high
    time.sleep(0.1)          # Allow some time for the sensor to initialize

def read_motion_data():
    """Read motion data from the PMW3360 sensor."""
    data = sensor.read_burst()  # Ensure this method matches your implementation
    if data:
        return data
    return None

# Main execution
reset_sensor()  # Call the reset function initially

# Try initializing the sensor after reset
if not initialize_sensor():
    print("Attempting to reset and reinitialize...")
    reset_sensor()
    time.sleep(0.1)  # Give some time for the reset
    if not initialize_sensor():
        print("Failed to initialize sensor after reset.")
        exit()  # Exit if the sensor cannot initialize

while True:
    motion_data = read_motion_data()  # Read motion data
    if motion_data and motion_data["is_on_surface"]:
        # Get delta values for movement
        dx = motion_data['dx']
        dy = motion_data['dy']
        
        # Print raw motion data for debugging
        print(f"Raw movement data: dx = {dx}, dy = {dy}")

        # Handle wrap-around values
        if dx >= 32768:
            dx -= 65536
        if dy >= 32768:
            dy -= 65536

        # Ignore very small movements to filter out noise
        if abs(dx) < MOVEMENT_THRESHOLD:
            dx = 0
        if abs(dy) < MOVEMENT_THRESHOLD:
            dy = 0

        # Apply smoothing to reduce fluctuations
        smoothed_dx = int(SMOOTHING_FACTOR * previous_dx + (1 - SMOOTHING_FACTOR) * dx)
        smoothed_dy = int(SMOOTHING_FACTOR * previous_dy + (1 - SMOOTHING_FACTOR) * dy)

        # Update previous values for next iteration
        previous_dx, previous_dy = smoothed_dx, smoothed_dy

        # Filter out unrealistic delta values
        if abs(smoothed_dx) > MAX_DELTA:
            smoothed_dx = MAX_DELTA if smoothed_dx > 0 else -MAX_DELTA
        if abs(smoothed_dy) > MAX_DELTA:
            smoothed_dy = MAX_DELTA if smoothed_dy > 0 else -MAX_DELTA

        # Log processed movement data
        print(f"Processed movement data: dx = {dx}, dy = {dy}")
        print(f"Smoothed movement data: smoothed_dx = {smoothed_dx}, smoothed_dy = {smoothed_dy}")

        # Move the cursor based on smoothed values
        mouse.move(x=smoothed_dx, y=smoothed_dy)  # Use the Mouse instance to move cursor
    
    time.sleep(0.05)  # Reduce the delay to improve responsiveness


