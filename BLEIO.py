from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.attributes import Attribute

# Create a BLE radio instance
ble = BLERadio()

# Create a UART service
uart_service = UARTService()

# Set security level for the characteristic of the UART service
uart_service.characteristic.security = Attribute.ENCRYPT_WITH_MITM

# Now the UART service requires encrypted communication with MITM protection
