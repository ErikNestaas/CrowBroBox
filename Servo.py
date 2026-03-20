from gpiozero import AngularServo
servo_degrees = 270
servo_pin = 13
s = AngularServo(servo_pin, min_angle=0, max_angle=servo_degrees)
def set_servo_pos(degrees):
    s.angle = degrees
    if ((s.angle - degrees) < 5):
        return True
    return False



