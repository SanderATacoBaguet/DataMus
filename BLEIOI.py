import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

# Set up BLE radio and UART service
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

while True:
    # Start advertising
    ble.start_advertising(advertisement)
    while not ble.connected:
        time.sleep(0.1)  # Wait for a connection
    
    print("Connected!")
    
    # Once connected, communicate with the client (e.g., send/receive data)
    while ble.connected:
        # Check if there's data from the client to read
        data = uart.read(32)  # Read up to 32 bytes
        if data:
            print("Received:", data)
            uart.write(data)  # Echo the received data back
        time.sleep(0.1)
