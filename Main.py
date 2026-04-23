from enum import Enum
from gpiozero import LED
from Ultralyd import get_us_distance
from Stepper import rotate_stepper
from Kamera import camera_take_photo_save
from Servo import set_servo_pos, calibrate_servo
from Chat import chat_send_promt_with_image
from stoppeklokke import fetch_time
import time
from pathlib import Path
import datetime

# class syntax
class States(Enum):
    SYSTEM_INACTIVE = 0
    IDLE = 1
    TAKE_PHOTO = 2 
    SEND_TO_API = 3
    TOSS_OUT = 4
    SORT_IN_BIN = 5
    DISPENSE_FOOD = 6

led = LED(19)

INPUT_US_ECHO = 18
INPUT_US_TRIGGER = 19
FOOD_US_ECHO = 88
FOOD_US_TRIGGER = 99

MAX_RETRY_PHOTO = 5
MAX_TIME_SINCE_PHOTO_MS = 10

PHOTO_PATH = "Desktop/trash.jpg"
STANDARD_PROMT = "Give me only a number between 0 and 1 of how sure you are that the thing in the picture is garbage. 1 means garbage, 0 means not garbage"
GARBAGE_PROBABILITY_THRESHOLD = 0.75

SERVO_GARBAGE_DEG = 90
SERVO_NOT_GARBAGE_DEG = -90
STEP_COUNT_ONE_PORTION = 2

FOOD_DISTANCE_THRESHOLD_M = 0
GARBAGE_DISTANCE_THRESHOLD_M = 30
SERVO_NORMAL_DIST = 30

TEST_NO = 1

state = States.IDLE


with open("data.txt", "a") as f:
  f.write("Test number " + str(TEST_NO) + " | Dato: " + str(datetime.datetime.now()) + "\n")
while 1:
    match state:
        case States.SYSTEM_INACTIVE:
            system_inactive()
        case States.IDLE:
            START_TIME = system_idle()
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

def system_idle():
    TEST_NO += 1
    calibrate_servo(SERVO_NORMAL_DIST)
    while state == States.IDLE:
        if get_us_distance(INPUT_US_ECHO, INPUT_US_TRIGGER) < GARBAGE_DISTANCE_THRESHOLD_M:
            state = States.TAKE_PHOTO
            start_time = fetch_time()
            return start_time
        
    return
        
def system_inactive():
    toss_out()
    while state == States.SYSTEM_INACTIVE:
        led.on()
        time.sleep(1)
        led.off()
        time.sleep(1)

def dispense_food():
    if get_us_distance(FOOD_US_ECHO, FOOD_US_TRIGGER) > FOOD_DISTANCE_THRESHOLD_M:
        state = States.SYSTEM_INACTIVE
        with open("demofile.txt", "a") as f:
            f.write("Not enough food left \n")
        return
    
    if not rotate_stepper(STEP_COUNT_ONE_PORTION):
        state = States.SYSTEM_INACTIVE
        return
    with open("demofile.txt", "a") as f:
        f.write("Food dispensed successfully \n")
    if get_us_distance(FOOD_US_ECHO, FOOD_US_TRIGGER) > FOOD_DISTANCE_THRESHOLD_M:
        state = States.SYSTEM_INACTIVE
        with open("demofile.txt", "a") as f:
            f.write("Not enough food left \n")
        return
    
    state = States.IDLE
    return
    
def take_photo():
    led.on()
    tries = MAX_RETRY_PHOTO
    camera_take_photo_save(PHOTO_PATH) 

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
    response = chat_send_promt_with_image(STANDARD_PROMT, PHOTO_PATH)
    with open("demofile.txt", "a") as f:
        f.write("API response: " + response + "\n")
    if int(response) > GARBAGE_PROBABILITY_THRESHOLD and int(response) > 0 and int(response) < 1:
        state = States.SORT_IN_BIN
        with open("demofile.txt", "a") as f:
            f.write("Plastic detected \n")
    elif int(response) < GARBAGE_PROBABILITY_THRESHOLD and int(response) > 0 and int(response) < 1:
        state = States.TOSS_OUT
        with open("demofile.txt", "a") as f:
            f.write("NOT Plastic detected \n")
    else:
        state = States.SYSTEM_INACTIVE
        with open("demofile.txt", "a") as f:
            f.write("Invalid response from API \n")

    stop_time = fetch_time()
    with open("demofile.txt", "a") as f:
        f.write(f"Time from start to descision: {stop_time - START_TIME} seconds. \n")
    return

def sort_in_bin():
    time.sleep(0.3)
    set_servo_pos(SERVO_GARBAGE_DEG)
    time.sleep(5)


def toss_out():
    time.sleep(0.3)
    set_servo_pos(SERVO_NOT_GARBAGE_DEG)
    time.sleep(5)


def check_photo_date(path):
    m_time = datetime.datetime.fromtimestamp(Path(path).stat().st_mtime)
    diff = datetime.now() - m_time
    if int(diff) > MAX_TIME_SINCE_PHOTO_MS:
        return False
    return True