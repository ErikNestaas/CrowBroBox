
from picamera2 import Picamera2
from time import sleep
def camera_take_photo_save():
    try:        
        filename = "/home/crowbrobox/Desktop/trash.jpg"
        camera = Picamera2()
        camera.start()
        camera.capture_file(filename)
        print(f"Photo saved as {filename}!")
        camera.close()
    except SystemError:
        print("Klarte ikke å ta bilde. Prøv igjen senere.")
