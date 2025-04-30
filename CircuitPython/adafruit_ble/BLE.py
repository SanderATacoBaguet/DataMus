from adafruit_ble import BLERadio
from adafruit_ble.services.standard.hid import HIDService
import time

# Initialize the BLE radio
ble = BLERadio()

# Initialize the HID service
hid_service = HIDService()

# Start scanning for BLE devices
print("Scanning for BLE HID devices...")
found_device = None

# Scan for devices that advertise HID service
while not found_device:
    for advertisement in ble.start_scan():
        # Check if the advertisement contains the HID service
        if HIDService in advertisement.services:
            print(f"Found HID device: {advertisement.address}")
            found_device = advertisement
            break

# Once we find a device, connect to it
if found_device:
    print("Connecting to HID device...")
    peer = ble.connect(found_device)
    
    # Now that we're connected, print out the HID service information
    print(f"Connected to {peer.address}")
    print(f"Protocol mode: {peer.hid.protocol_mode}")
    print(f"Report map: {peer.hid.report_map}")

    # You can interact with the device (sending/receiving data) here.
    # This is just a simple example where we keep the connection alive.
    try:
        while True:
            time.sleep(1)  # Keep the connection alive
    except KeyboardInterrupt:
        print("Disconnected.")
        ble.disconnect(peer)
