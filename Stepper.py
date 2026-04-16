from gpiozero import OutputDevice
from time import sleep

class StepperA4988:
    def __init__(self, step_pin, dir_pin, enable_pin=None, delay=0.001):
        self.step = OutputDevice(step_pin)
        self.dir = OutputDevice(dir_pin)
        self.enable = OutputDevice(enable_pin) if enable_pin is not None else None
        self.delay = delay

        if self.enable:
            self.enable.off()  # aktiv LOW på mange A4988 (enable = 0)

    def set_direction(self, direction):
        """
        direction = 1 (med klokka)
        direction = 0 (mot klokka)
        """
        if direction:
            self.dir.on()
        else:
            self.dir.off()

    def move_steps(self, steps, direction=1):
        self.set_direction(direction)

        for _ in range(steps):
            self.step.on()
            sleep(self.delay)
            self.step.off()
            sleep(self.delay)

    def disable(self):
        if self.enable:
            self.enable.on()

    def enable_motor(self):
        if self.enable:
            self.enable.off()

def rotate_stepper(steps):
    motor = StepperA4988(step_pin=18, dir_pin=16, enable_pin=25, delay=0.0008)

    try:
        motor.move_steps(steps, direction=1)

    finally:
        motor.disable()