import cv2
import sys

image_file = 0
try:
    image_file = sys.argv[1]
except IndexError as e:
    print(f"USAGE: {sys.argv[0]} <image_file_path>")
    exit()
except ValueError as e:
    print(f"Error: {e}")
    exit()

# Initialize the QR code detector
qrd = cv2.QRCodeDetector()

# Open the image file.
frame = cv2.imread(image_file)
if frame is None:
    print(f"Unable to read from '{sys.argv[1]}'")
    exit(1)

# Detect and decode QR code
data, _, _ = qrd.detectAndDecode(frame)

# If QR code is detected
if data:
    print("-"*20)
    print("[QR Code detected]")
    print(f"{data}")
else:
    print("No QR is detected")

