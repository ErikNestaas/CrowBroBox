from gpiozero import AngularServo
from Ultralyd import get_us_distance
from simple_pid import PID
import numpy

def set_servo_pos(degrees):
    servo_degrees = 270
    servo_pin = 13
    s = AngularServo(servo_pin, min_angle=0, max_angle=servo_degrees)
    s.angle = degrees
    if ((s.angle - degrees) < 5):
        return True
    return False

def calibrate_servo(NORMAL_DISTANCE):
    pid = PID(1.0, 0.1, 0.05, setpoint=NORMAL_DISTANCE)
    radius = 3

    while True:
        current_value = get_us_distance()
        control_signal = numpy.arcsin(pid(current_value)/radius)
        set_servo_pos(control_signal)