
from picamera2 import Picamera2

def camera_take_photo_save():
    try:        
        filename = filename = "/home/CrowBroBox/Desktop/trash.jpg"
        camera = Picamera2()
        camera.capture_file(filename)
        print(f"Photo saved as {filename}!")
    except SystemError:
        print("Klarte ikke å ta bilde. Prøv igjen senere.")