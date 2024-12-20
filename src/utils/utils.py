from enum import Enum
import json
import logging
import os
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from time import time
from typing import AnyStr, Dict, List, Tuple, Union
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import __main__
import cv2
import numpy as np

from selenium.webdriver.chrome.options import Options as ChromeOptions

def nput():
    a = ""
    while True:
        a = input('q to quit')
        if a == 'q':
            break
        a = ''

def safe_find_element(driver, locator, retries=30):
    """ 3 retries @ 10s wait or 30 retries @ 1 sec wait.... Same total wait time in worst case.
    Safely finds an element with retries in case of a StaleElementReferenceException.
    """
    for attempt in range(retries):
        try:
            # Wait for the element to be located
            print(f"Looking for {locator=} {attempt=}")
            element = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException caught, retrying... ({attempt + 1}/{retries})")
            if attempt == retries - 1:
                raise  # Re-raise the exception if we've exhausted all retries





def users_home_dir():
    return os.path.expanduser( '~' )

def file_exists(directory):
    return os.path.exists(directory)

def create_file_if_not_exists(path):
    print("Create path if not exist", path)
    if path and not file_exists(path):
        with open(path, 'w'):
            pass

def get_ip() -> str:
    cmd = ['curl', '-s', "ipinfo.io/ip"]
    outstr = subprocess.run(cmd, check=False, encoding='utf-8',
                                capture_output=True).stdout.strip()
    return outstr

class AppStatus(Enum):
    '''Encompasses all statuses that an app may have at the end of a test run on a single app.'''

    NEEDS_UPDATE = -14                # Playstore crashed
    PLAYSTORE_FAIL = -13                # Playstore crashed
    CRASH_WIN_DEATH = -12               # App crashed on launch
    CRASH_FORCE_RM_ACT_RECORD = -11     # App crashed on launch
    CRASH_ANR = -10                     # App crashed on launch
    CRASH_FDEBUG_CRASH = -9             # App crashed on launch
    CRASH_FATAL_EXCEPTION = -8          # App crashed on launch
    FAILED_TO_LAUNCH = -7               # Fail to launch - should also capture logs for this.
    FAILED_TO_INSTALL = -6              # Genral install error
    NEEDS_PRICE = -5                    # App needs to be purchased
    DEVICE_NONCOMPAT = -4               # Device missing feature
    INVALID = -3                        # App not on playstore anymore
    APP_OLD = -2                        # App targets old SDK
    COUNTRY_NA = -1                     # Country NA
    FAIL = 0                            # General failure with testing
    PASS = 1                            # App launched w/out errors detected.
    LOGGED_IN_GOOGLE = 2                # Logged in via google account
    LOGGED_IN_FB = 3                    # Logged in via facebook account
    LOGGED_IN_EMAIL = 4                 # Logged in via email/password
    INIT = 1337                 # Logged in via email/password


@dataclass()
class _CONFIG:
    save_yolov8_predicts: bool = True
    debug_print: bool = True # Playstore.py, debug color printing by device.
    multi_split_packages: bool = False  # MultiprocessTaskRunner, splits apps across devices or not
    login_facebook: bool = False  # Discover, install and sign into Facebook before running AppValidator.
    skip_pre_multi_uninstall: bool = False  # Skips pre process uninstallation of all apps to be tested.
    skip_install: bool = False # App_validator allow to skip this step
    skip_launch: bool = False # App_validator allow to skip this step
    skip_login: bool = True # App_validator allow to skip this step
    skip_post_uninstall: bool = True  #Skips post process uninstallation of the app just tested.
    base_url: str = "https://appval-387223.wl.r.appspot.com"  #Skips post process uninstallation of the app just tested.

    def __str__(self):
        return ' '.join([f'{item[0]}:{item[1]}' for item in self.__dict__.items()])

# Create an instance of the _CONFIG class
config = _CONFIG()
# Print the values of the class using the __str__ method

CONFIG = _CONFIG()
BASE_PORT = 4723

weights = 'notebooks/yolov5/runs/train/exp007/weights/best_309.pt'
weights = 'notebooks/yolov5/runs/train/exp4/weights/best.pt'  # Lastest RoboFlow Model V1
weights = 'notebooks/yolov5/runs/train/exp6/weights/best.pt'  # Lastest RoboFlow Model V2
weights = 'notebooks/yolov5/runs/train/exp7/weights/best.pt'  # Lastest RoboFlow Model V3
weights = 'notebooks/yolov5/runs/train/exp8/weights/best.pt'  # Lastest RoboFlow Model V4
WEIGHTS = 'notebooks/yolov5/runs/train/exp10/weights/best.pt'  # Lastest RoboFlow Model V5
v8_weights = 'objdetector/weights/best_v5.pt'  # Lastest RoboFlow Model V5 dataset, yolov8 trained.
v8_weights = 'objdetector/weights/best_v5_m.pt'  # Lastest RoboFlow Model V5 dataset, yolov8 trained on medium 	640	50.2	234.7	1.83	25.9	78.9.
v8_weights = 'objdetector/weights/best_v8m_v6d.pt'  # Lastest RoboFlow Model V6 dataset, yolov8 medium trained this was the same as v5, no new images were added by mistake..
v8_weights = 'objdetector/weights/best_v8m_v7.pt'  # Lastest RoboFlow Model V7 dataset, yolov8 medium trained. (missing some FB labels, started failing on login/password for Duolingo when it was previously working well with 90%+ confidence)
v8_weights = 'objdetector/weights/best_v8m_v8.pt'  # Lastest RoboFlow Model V8 dataset
v8_weights = 'objdetector/weights/best_v8n_v8.pt'  # Lastest RoboFlow Model V8 dataset
V8_WEIGHTS = 'objdetector/weights/best_1080_v8m_v1.pt'  # yolo_1080 - all source images were resized to 1920x1080. Then they were relabed. Trained yolov8 Medium v1
V8_WEIGHTS = 'objdetector/weights/last.pt'  # yolo_1080 - all source images were resized to 1920x1080. Then they were relabed. Trained yolov8 Medium v1
V8_WEIGHTS = 'objdetector/weights/best_1080_v8m_v2.pt'  # yolo_1080 - all source images were resized to 1920x1080. Then they were relabed. Trained yolov8 Medium v1
V8_WEIGHTS = 'objdetector/weights/best_1080_fixedlabels_20epcohs.pt'  # yolo_1080 - all source images were resized to 1920x1080. Then they were relabed. Trained yolov8 Medium v1
V8_WEIGHTS = 'objdetector/weights/best_1080_ v8m_v2_fixedlabels.pt'  # yolo_1080 - all source images were resized to 1920x1080. Then they were relabed. Trained yolov8 Medium v1
V8_WEIGHTS = 'objdetector/weights/best_1080_v8m_v3.pt'  # yolo_1080 - all source images were resized to 1920x1080. Then they were relabed. Trained yolov8 Medium v1

# https://docs.ultralytics.com/tasks/detect/?h=model

PLAYSTORE_PACKAGE_NAME = "com.android.vending"
PLAYSTORE_MAIN_ACT = "com.google.android.finsky.activities.MainActivity"
FACEBOOK_PACKAGE_NAME = "com.facebook.katana"
FACEBOOK_APP_NAME = "Facebook"

# Labels for YOLOv5
'''names:
  0: Close
  1: Continue
  2: FBAuth
  3: GoogleAuth
  4: Two
  5: code
  6: loginfield
  7: passwordfield'''

CLOSE = 'Close'
CONTINUE = 'Continue'
FB_ATUH = 'FBAuth'
GOOGLE_AUTH = 'GoogleAuth'
TWO = 'Two'
CODE = 'code'
LOGIN = 'loginfield'
PASSWORD = 'passwordfield'
IMAGE_LABELS = [
    CLOSE,
    CONTINUE,
    FB_ATUH,
    GOOGLE_AUTH,
    TWO,
    CODE,
    LOGIN,
    PASSWORD,
]


##      Appium config & stuff  ##
def android_options(device_name: AnyStr, app_package: AnyStr, main_activity: AnyStr) -> Dict:
    '''
        Formats the Desired Capabilities for Appium Server.
    '''

    options = ChromeOptions()
    options.platform_name = 'Android'
    options.set_capability('platformName', 'Android')
    options.set_capability('appium:udid', device_name)
    # options.set_capability('appium:appPackage', app_package)
    options.set_capability('appium:automationName', 'UiAutomator2')
    options.set_capability('appium:appActivity', main_activity)
    options.set_capability('appium:ensureWebviewHavepages', "true")
    options.set_capability('appium:nativeWebScreenshot', "true")
    options.set_capability('appium:newCommandTimeout', 3600)
    options.set_capability('appium:connectHardwareKeyboard', "true")
    options.set_capability('appium:noReset', False)
    options.set_capability('appium:uiautomator2ServerInstallTimeout', 60000)
    return options

##      Appium config & stuff  ##
def android_des_caps(device_name: AnyStr, app_package: AnyStr, main_activity: AnyStr) -> Dict:
    '''
        Formats the Desired Capabilities for Appium Server.
    '''

    return {
        'platformName': 'Android',
        'appium:udid': device_name,
        'appium:appPackage': app_package,
        'appium:automationName': 'UiAutomator2',
        'appium:appActivity': main_activity,
        'appium:ensureWebviewHavepages': "true",
        'appium:nativeWebScreenshot': "true",
        'appium:newCommandTimeout': 3600,
        'appium:connectHardwareKeyboard': "true",
        'appium:noReset': False,
        "appium:uiautomator2ServerInstallTimeout": 60000,

    }

def dev_scrape_start_at_app(start_package_name: str, app_list: List[List[str]]) -> int:
    ''' Given package name, returns index in the list.'''
    for i, app in enumerate(app_list):
        app_name, package_name = app
        if start_package_name == package_name:
            return i
    raise Exception(f"{start_package_name} not in the list.")


def nested_default_dict():
        return defaultdict(nested_default_dict)

##        NOT CURRENTLY USED          Image utils      NOT CURRENTLY USED         ##
def transform_coord_from_resized(original_size: Tuple, resized_to: Tuple, resized_coords: Tuple) -> Tuple[int]:
    ''' Given original img size, resized image size and resized coords, this will calculate the original coords.

        Args:
            original_size: A tuple defining the size of the original image representing the screen coords.
            resized_to: A tuple defining the size of the resized image.
            resized_coords: A tuple representing the x,y coords reported from detection on the resized image.

            The image is resized from its current size to 1200x800.
            So the bound box is now referencing the resized image.

            For ex, Helios @ 100% = 1536 x 864 => actual point to click = (0.4167, 0.5) x (1536, 864) = (640, 432)
                                  = 1200 x 800 => returns x,y to click @ (500, 400) => % => ([500/1200], [400/800]) = (0.4167, 0.5)

            So, when we resize and new image reports (500, 400) we need to actually click (640, 432)

            Returns:
            A tuple representing the coordinates on the original image.
    '''
    x_coord_factor = resized_coords[0] / resized_to[0]
    y_coord_factor = resized_coords[1] / resized_to[1]
    return (original_size[0]* x_coord_factor, original_size[1] * y_coord_factor)

def save_resized_image(image_bytes: bytes, new_size: Tuple, output_path: str):
    """
    Resize the input PNG image bytes to the given size using OpenCV2 and save it as a PNG file.

    Args:
        image_bytes: The input PNG image as bytes.
        new_size: A tuple (width, height) of the desired new image size.
        output_path: The path to save the resized image file.

    Returns:
        None.
    """
    # Read the image from bytes using OpenCV2
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Get the original image size
    original_size = image.shape[:2][::-1]

    # Resize the image using OpenCV2
    resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)

    # Save the resized image as a PNG file
    cv2.imwrite(output_path, resized_image)

def find_template(large_img, small_img, method=cv2.TM_CCOEFF_NORMED):
    method = cv2.TM_SQDIFF_NORMED
    # Read the images
    large_img = cv2.imread(large_img)
    small_img = cv2.imread(small_img)

    # Convert images to grayscale
    gray_large_img = cv2.cvtColor(large_img, cv2.COLOR_BGR2GRAY)
    gray_small_img = cv2.cvtColor(small_img, cv2.COLOR_BGR2GRAY)

    # Apply template matching
    result = cv2.matchTemplate(gray_large_img, gray_small_img, method)

    # Use the cv2.minMaxLoc() function to find the coordinates of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print("Min/ max", min_val, max_val)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    # Draw a rectangle around the matched region
    bottom_right = (top_left[0] + small_img.shape[1], top_left[1] + small_img.shape[0])
    cv2.rectangle(large_img, top_left, bottom_right, (0, 0, 255), 2)

    # Show the final image
    cv2.imshow('Matched Image', large_img)
    # cv2.imshow('Matched Image', gray_large_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

ADB_KEYCODE_UNKNOWN = "0"
ADB_KEYCODE_MENU = "1"
ADB_KEYCODE_SOFT_RIGHT = "2"
ADB_KEYCODE_HOME = "3"
ADB_KEYCODE_BACK = "4"
ADB_KEYCODE_CALL = "5"
ADB_KEYCODE_ENDCALL = "6"
ADB_KEYCODE_0 = "7"
ADB_KEYCODE_1 = "8"
ADB_KEYCODE_2 = "9"
ADB_KEYCODE_3 = "10"
ADB_KEYCODE_4 = "11"
ADB_KEYCODE_5 = "12"
ADB_KEYCODE_6 = "13"
ADB_KEYCODE_7 = "14"
ADB_KEYCODE_8 = "15"
ADB_KEYCODE_9 = "16"
ADB_KEYCODE_STAR = "17"
ADB_KEYCODE_POUND = "18"
ADB_KEYCODE_DPAD_UP = "19"
ADB_KEYCODE_DPAD_DOWN = "20"
ADB_KEYCODE_DPAD_LEFT = "21"
ADB_KEYCODE_DPAD_RIGHT = "22"
ADB_KEYCODE_DPAD_CENTER = "23"
ADB_KEYCODE_VOLUME_UP = "24"
ADB_KEYCODE_VOLUME_DOWN = "25"
ADB_KEYCODE_POWER = "26"
ADB_KEYCODE_CAMERA = "27"
ADB_KEYCODE_CLEAR = "28"
ADB_KEYCODE_A = "29"
ADB_KEYCODE_B = "30"
ADB_KEYCODE_C = "31"
ADB_KEYCODE_D = "32"
ADB_KEYCODE_E = "33"
ADB_KEYCODE_F = "34"
ADB_KEYCODE_G = "35"
ADB_KEYCODE_H = "36"
ADB_KEYCODE_I = "37"
ADB_KEYCODE_J = "38"
ADB_KEYCODE_K = "39"
ADB_KEYCODE_L = "40"
ADB_KEYCODE_M = "41"
ADB_KEYCODE_N = "42"
ADB_KEYCODE_O = "43"
ADB_KEYCODE_P = "44"
ADB_KEYCODE_Q = "45"
ADB_KEYCODE_R = "46"
ADB_KEYCODE_S = "47"
ADB_KEYCODE_T = "48"
ADB_KEYCODE_U = "49"
ADB_KEYCODE_V = "50"
ADB_KEYCODE_W = "51"
ADB_KEYCODE_X = "52"
ADB_KEYCODE_Y = "53"
ADB_KEYCODE_Z = "54"
ADB_KEYCODE_COMMA = "55"
ADB_KEYCODE_PERIOD = "56"
ADB_KEYCODE_ALT_LEFT = "57"
ADB_KEYCODE_ALT_RIGHT = "58"
ADB_KEYCODE_SHIFT_LEFT = "59"
ADB_KEYCODE_SHIFT_RIGHT = "60"
ADB_KEYCODE_TAB = "61"
ADB_KEYCODE_SPACE = "62"
ADB_KEYCODE_SYM = "63"
ADB_KEYCODE_EXPLORER = "64"
ADB_KEYCODE_ENVELOPE = "65"
ADB_KEYCODE_ENTER = "66"
ADB_KEYCODE_DEL = "67"
ADB_KEYCODE_GRAVE = "68"
ADB_KEYCODE_MINUS = "69"
ADB_KEYCODE_EQUALS = "70"
ADB_KEYCODE_LEFT_BRACKET = "71"
ADB_KEYCODE_RIGHT_BRACKET = "72"
ADB_KEYCODE_BACKSLASH = "73"
ADB_KEYCODE_SEMICOLON = "74"
ADB_KEYCODE_APOSTROPHE = "75"
ADB_KEYCODE_SLASH = "76"
ADB_KEYCODE_AT = "77"
ADB_KEYCODE_NUM = "78"
ADB_KEYCODE_HEADSETHOOK = "79"
ADB_KEYCODE_FOCUS = "80"
ADB_KEYCODE_PLUS = "81"
ADB_KEYCODE_MENU = "82"
ADB_KEYCODE_NOTIFICATION = "83"
ADB_KEYCODE_SEARCH = "84"