import wifi
import socketpool
import adafruit_requests

# Wi-Fi Credentials
SSID = "DATO IOT"
PASSWORD = "Admin:123"

# Connect to Wi-Fi
print("Connecting to Wi-Fi...")
wifi.radio.connect(SSID, PASSWORD)
print("Connected! IP Address:", wifi.radio.ipv4_address)

# Create a Socket Server
pool = socketpool.SocketPool(wifi.radio)
server = pool.socket()
server.bind(("0.0.0.0", 8080))  # Listen on port 8080
server.listen(1)

print("Waiting for connection...")

conn, addr = server.accept()
print(f"Connection from {addr}")

while True:
    data = conn.recv(1024)
    if data:
        print("Received:", data.decode())
        conn.send(b"Message received!")  # Send response
