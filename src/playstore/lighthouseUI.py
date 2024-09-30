from datetime import datetime
import json
import os
from utils.utils import nput

from dataclasses import dataclass
from random import gauss
from time import sleep
import cv2
import numpy as np
import pyautogui
from pynput.keyboard import Controller, Key
from playstore.config import get_save_coords

SCREEN_TOP_MARGIN = 28
WINDOW_TOP_MARGIN = 35


def capture_screenshot():
    # Capture a screenshot of the entire screen
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a NumPy array and then to a format OpenCV can work with
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    return screenshot

def find_in_screenshot(screenshot, template_path, threshold=0.8):
    # Load the cancel button image as the template
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)

    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

    # Get locations where the match exceeds the threshold
    loc = np.where(result >= threshold)

    if len(loc[0]) > 0:
        print(f"found!")
        # # Draw a rectangle around the found template in the screenshot (for visualization)
        # h, w, _ = template.shape
        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

        # # Show the result with rectangles (optional)

        return True
    else:
        print(f"not found.")
        # cv2.imshow('Failed to detect Cancel Button', screenshot)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return False


@dataclass
class LighthouseUI:

    # This class will Click on the light house download buttons
    __init = True
    keyboard = Controller()
    __save_coords = get_save_coords()
    __url = ""


    def setURL(self, url):
        self.__url = url


    def __click(self, pt=None):
        if pt is None:
            return
        x, y = pt
        print(f"Clicking: {x} {y} ")
        # TODO Randomize move tos
        pyautogui.moveTo(x, y + SCREEN_TOP_MARGIN + WINDOW_TOP_MARGIN, duration=gauss(0.4, .1))
        pyautogui.click()


    def click_menu(self):
        pt = (2481, 67,)
        self.__click(pt)


    def click_lighthouse(self):
        pt = (2342, 287,)
        self.__click(pt)


    def click_desktop_device(self):
        pt = (2306, 430,)
        self.__click(pt)

    def click_analyze_page_load(self):
        pt = (2418, 205,)
        self.__click(pt)

    def click_download_menu(self):
        pt = (2534, 125,)
        self.__click(pt)

    def click_download(self):
        pt = (2463, 297,)
        self.__click(pt)

    def click_save(self):
        self.__click(self.__save_coords)

    def click_new_report(self):
        pt = (2280, 95,)
        self.__click(pt)


    def is_cancel_btn_showing(self):
        current_file_path = os.path.abspath(__file__)
        print(f"{current_file_path=}")
        # current_file_path='/home/killuh/ws_p38/AL_CL_perf/src/playstore/lighthouseUI.py'
        cur_dir = "/".join(current_file_path.split("/")[:-1])
        print(f"{cur_dir=}")
        template_path = f'{cur_dir}/cancel.png'  # Replace with your actual path

        # Capture the screenshot of the current screen
        screenshot = capture_screenshot()

        # Find the button in the screenshot
        return find_in_screenshot(screenshot, template_path)


    def is_need_https_showing(self):
        current_file_path = os.path.abspath(__file__)
        cur_dir = "/".join(current_file_path.split("/")[:-1])
        template_path = f'{cur_dir}/https_error.png'  # Replace with your actual path
        # Capture the screenshot of the current screen
        screenshot = capture_screenshot()
        # Find the button in the screenshot
        return find_in_screenshot(screenshot, template_path)

    def __download_failed_report(self):

        '''
            Download failed report

            fileName = www.youtube.com-20240924T230012.json


                report = {
                    "error": r['runWarnings'] in ERRORS,
                    "metrics": r['audits']['metrics']['details']['items'][0] if r else {}
                }


        '''
        data = {

                "error": f"Failed to load {self.__url}",
                "metrics": {
                    "audits": {
                        "metrics": {
                            "details": {
                                'items': [
                                    {
                                        "firstContentfulPaint": 0,
                                        "largestContentfulPaint": 0,
                                        "interactive": 0,
                                        "speedIndex": 0,
                                        "totalBlockingTime": 0,
                                        "maxPotentialFID": 0,
                                        "cumulativeLayoutShift": 0,
                                        "cumulativeLayoutShiftMainFrame": 0,
                                        "lcpLoadStart": 0,
                                        "lcpLoadEnd": 0,
                                        "timeToFirstByte": 0,
                                        "observedTimeOrigin": 0,
                                        "observedTimeOriginTs": 0,
                                        "observedNavigationStart": 0,
                                        "observedNavigationStartTs": 0,
                                        "observedFirstPaint": 0,
                                        "observedFirstPaintTs": 0,
                                        "observedFirstContentfulPaint": 0,
                                        "observedFirstContentfulPaintTs": 0,
                                        "observedFirstContentfulPaintAllFrames": 0,
                                        "observedFirstContentfulPaintAllFramesTs": 0,
                                        "observedLargestContentfulPaint": 0,
                                        "observedLargestContentfulPaintTs": 0,
                                        "observedLargestContentfulPaintAllFrames": 0,
                                        "observedLargestContentfulPaintAllFramesTs": 0,
                                        "observedTraceEnd": 0,
                                        "observedTraceEndTs": 0,
                                        "observedLoad": 0,
                                        "observedLoadTs": 0,
                                        "observedDomContentLoaded": 0,
                                        "observedDomContentLoadedTs": 0,
                                        "observedCumulativeLayoutShift": 0,
                                        "observedCumulativeLayoutShiftMainFrame": 0,
                                        "observedFirstVisualChange": 0,
                                        "observedFirstVisualChangeTs": 0,
                                        "observedLastVisualChange": 0,
                                        "observedLastVisualChangeTs": 0,
                                        "observedSpeedIndex": 0,
                                        "observedSpeedIndexTs": 0
                                    }
                                ]
                            }
                        }
                    }

                }
            }
        try:
            with open(f"{self.__url}"-{datetime.now()}, 'w', 'utf-8') as f:
                json.dump(data, f)
        except Exception as err:
            print(f"Error writing error json file for: {self.__url}", err)



    def start_analysis(self):
        if self.__init:
            # nput()
            # Instead of a 3 clicker, sometimes that button isnt in same spot
            # Lets do ctl + sht + p
            # Typewrite: lighthouse + enter
            sleep(2)
            print("Pressing shortcut ctl+shift+p")
            pyautogui.hotkey('ctrl', 'shift', 'p')
            sleep(2)
            self.keyboard.type("lighthouse")
            sleep(1)
            self.keyboard.press(Key.enter)
            self.keyboard.release(Key.enter)
            sleep(2)
            # nput()
            self.click_desktop_device()
            sleep(2)


            self.__init = False
        else:
            self.click_new_report()


        sleep(2)
        # Check for errors first
        if self.is_need_https_showing():
            print("Error loading page: need_https_showing")
            self.__download_failed_report()
            return False

        self.click_analyze_page_load()
        print("Do some polling image detection here.... open-cv should work")

        sleep(5) # Let lighthouse startup
        while self.is_cancel_btn_showing():
            sleep(3)

        sleep(1)
        self.click_download_menu()
        sleep(2)
        self.click_download()
        sleep(2)
        self.click_save()
        sleep(2)
        return True





