from enum import Enum
from gpiozero import LED
from Ultralyd import get_us_distance
from Stepper import rotate_stepper
from Kamera import camera_take_photo_save
from Servo import set_servo_pos
from Chat import chat_send_promt_with_image
import time
from pathlib import Path
from datetime import datetime

# class syntax
class States(Enum):
    SYSTEM_INACTIVE = 0
    IDLE = 1
    TAKE_PHOTO = 2 
    SEND_TO_API = 3
    TOSS_OUT = 4
    SORT_IN_BIN = 5
    DISPENSE_FOOD = 6

led = LED(27)

INPUT_US_ECHO = 17
INPUT_US_TRIGGER = 4

MAX_RETRY_PHOTO = 5
MAX_TIME_SINCE_PHOTO_S = 100

PHOTO_PATH = "/home/crowbrobox/Desktop/trash.jpg"
STANDARD_PROMT = "Give me only a number between 0 and 1 of how sure you are that the thing on the metal plate in the picture is a non-biodegradeble/artifial. 1 means non-biodegradeble/artifical, 0 means natural"
GARBAGE_PROBABILITY_THRESHOLD = 0.75

SERVO_GARBAGE_DEG = 0
SERVO_NOT_GARBAGE_DEG = 1
STEP_COUNT_ONE_PORTION = 800

FOOD_DISTANCE_THRESHOLD_M = 0
GARBAGE_DISTANCE_THRESHOLD_M = 0.28
SERVO_NORMAL_DIST = 30

TEST_NO = 1

state = States.IDLE
with open("data.txt", "a") as f:
  f.write("test number " + str(TEST_NO) + "\n")

def system_idle():
    global state
    global TEST_NO
    TEST_NO += 1
    #calibrate_servo(SERVO_NORMAL_DIST)
    while state == States.IDLE:
        if get_us_distance(INPUT_US_ECHO, INPUT_US_TRIGGER) < GARBAGE_DISTANCE_THRESHOLD_M:
            state = States.TAKE_PHOTO
            return
        
    return
        
def system_inactive():
    toss_out()
    while state == States.SYSTEM_INACTIVE:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)

def dispense_food():
    global state
    if not rotate_stepper(STEP_COUNT_ONE_PORTION):
        state = States.SYSTEM_INACTIVE
        print("dispense food failed")
        return
    with open("demofile.txt", "a") as f:
        f.write("Food dispensed successfully \n")
    
    state = States.IDLE
    return
    
def take_photo():
    global state
    led.on()
    tries = MAX_RETRY_PHOTO
    camera_take_photo_save() 

    while not check_photo_date(PHOTO_PATH) and tries > 0:
        camera_take_photo_save(PHOTO_PATH)
        tries -= 1

    led.off()

    if tries == 0:
        state = States.SYSTEM_INACTIVE
        return
    
    state = States.SEND_TO_API
    return

def send_to_api():
    global state
    response = chat_send_promt_with_image(STANDARD_PROMT, PHOTO_PATH)
    with open("demofile.txt", "a") as f:
        f.write("API response: " + response + "\n")
    print(response)
    if float(response) > GARBAGE_PROBABILITY_THRESHOLD and float(response) >= 0 and float(response) <= 1:
        state = States.SORT_IN_BIN
        with open("demofile.txt", "a") as f:
            f.write("Plastic detected \n")
    elif float(response) < GARBAGE_PROBABILITY_THRESHOLD and float(response) >= 0 and float(response) <= 1:
        state = States.TOSS_OUT
        with open("demofile.txt", "a") as f:
            f.write("NOT Plastic detected \n")
    else:
        state = States.SYSTEM_INACTIVE
        with open("demofile.txt", "a") as f:
            f.write("Invalid response from API \n")
    return

def sort_in_bin():
    global state
    state = States.DISPENSE_FOOD
    time.sleep(0.3)
    set_servo_pos(1)


def toss_out():
    global state
    state = States.IDLE
    time.sleep(0.3)
    set_servo_pos(0)
    


def check_photo_date(path):
    m_time = datetime.fromtimestamp(Path(path).stat().st_mtime)
    now = datetime.now()
    diff = now - m_time
    print(int(diff.total_seconds()))
    print(int(MAX_TIME_SINCE_PHOTO_S))
    if (int(diff.total_seconds()) > int(MAX_TIME_SINCE_PHOTO_S)):
        print("hello")
        return False
    return True
while 1:
    match state:
        case States.SYSTEM_INACTIVE:
            system_inactive()
        case States.IDLE:
            system_idle()
        case States.TAKE_PHOTO:
            take_photo()
        case States.SEND_TO_API:
            send_to_api()
        case States.TOSS_OUT:
            toss_out()
        case States.SORT_IN_BIN:
            sort_in_bin()
        case States.DISPENSE_FOOD:      
            dispense_food()  
