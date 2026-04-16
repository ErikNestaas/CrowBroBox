
from picamera2 import Picamera2 # Denne kan bare installeres på Raspberry Pi (trenger Linux), og kan dermed ikke tests på andre OSer
import cv2
import os

def camera_take_photo_save():
    JPEG_quality = 70
    home_dir = os.environ['HOME']

    try:        
        picam2 = Picamera2()

        frame = picam2.capture_array()
        ok, jpeg = cv2.imencode(
            ".jpeg",
            frame,
            [int(cv2.IMWRITE_JPEG_QUALITY),JPEG_quality])
        
        if not ok:
            print("Feil under JPEG-koding av bildet.")
            return

        filename = f"{home_dir}/Desktop/trash.jpeg" # OBS! OVERSKRIVER FORRIGE "trash.jpg"
        with open(filename, "wb") as f:
            f.write(jpeg.tobytes())
            size_kb = len(jpeg) / 1024
            
        print(f"Photo saved as {filename}, with size {size_kb:.3f} KB!")
        
    except SystemError:
        print("Klarte ikke å ta bilde. Prøv igjen senere.")
        return

