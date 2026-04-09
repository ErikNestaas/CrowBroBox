from gpiozero import OutputDevice
from time import sleep

STEP = OutputDevice(18)
DIR  = OutputDevice(16)
EN   = OutputDevice(25)

EN.off()   # A4988 enable is active-low
DIR.on()

delay = 1  # slow

while True:
    STEP.on()
    sleep(delay)
    STEP.off()
    sleep(delay)
    print("running")

