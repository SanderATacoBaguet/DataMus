import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising import Advertisement

# Initialize the BLE radio
ble = BLERadio()

# Check if the BLE adapter is available
if ble is None:
    print("No BLE adapter found")
else:
    print("BLE adapter is ready")

# Create a simple advertisement (this is what will make your Pico W discoverable via Bluetooth)
advertisement = Advertisement()
advertisement.complete_name = "Pico_W_BLE"  # Name the BLE device for easy identification

# Start advertising
print("Starting BLE advertisement...")
ble.start_advertising(advertisement)

while True:
    print("Advertising...")
    time.sleep(1)
