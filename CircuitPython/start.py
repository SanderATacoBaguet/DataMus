import time
import board
import busio
import adafruit_bluefruit_connect

# Set up UART connection to the Bluefruit LE module
uart = busio.UART(board.TX, board.RX, baudrate=115200)

# Initialize Bluefruit
bluefruit = adafruit_bluefruit_connect.Bluefruit(uart)

# Connect to the Bluefruit module
bluefruit.connect()

# Main loop to send some data (e.g., mouse events)
while True:
    # Simulating sending mouse movement (for example)
    bluefruit.write(b'Mouse move')
    time.sleep(1)
