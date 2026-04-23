from gpiozero import Servo
from Ultralyd import get_us_distance
from simple_pid import PID
import numpy
from time import sleep

def set_servo_pos(degrees):
    servo = Servo(19, min_pulse_width=0.875/1000, max_pulse_width=2.125/1000)
    if degrees==1:
        servo.mid()
        sleep(0.5)
        servo.max()
        sleep(1)
        servo.mid()
        sleep(0.5)
    else:
        servo.mid()
        sleep(0.5)
        servo.min()
        sleep(1)
        servo.mid()
        sleep(0.5)
        servo.mid()
        sleep(0.5)

"""

def calibrate_servo(NORMAL_DISTANCE):
    pid = PID(1.0, 0.1, 0.05, setpoint=NORMAL_DISTANCE)
    radius = 3

    while True:
        current_value = get_us_distance(17, 4)
        control_signal = numpy.arcsin(pid(current_value)/radius)
        set_servo_pos(control_signal)
"""
