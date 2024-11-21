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
from playstore.config import get_save_coords, get_coords

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
        # print(f"found!")
        # # Draw a rectangle around the found template in the screenshot (for visualization)
        # h, w, _ = template.shape
        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(screenshot, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

        # # Show the result with rectangles (optional)

        return True
    else:
        # print(f"not found.")
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
    __coords = get_coords()


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


    def click_desktop_device(self):
        pt = self.__coords["click_desktop_device"]
        self.__click(pt)

    def click_analyze_page_load(self):
        pt = self.__coords["click_analyze_page_load"]
        self.__click(pt)

    def click_download_menu(self):
        pt = self.__coords["click_download_menu"]
        self.__click(pt)

    def click_download(self):
        pt = self.__coords["click_download"]
        self.__click(pt)

    def click_save(self):
        pt = self.__coords["click_save"]
        self.__click(pt)

    def click_new_report(self):
        pt = self.__coords["click_new_report"]
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

    def is_img_showing(self, filename, retries=3):
        cur_dir = "/".join(os.path.abspath(__file__).split("/")[:-1])
        template_path = f'{cur_dir}/{filename}'

        res = False
        for _ in range(retries):
            screenshot = capture_screenshot()
            res = find_in_screenshot(screenshot, template_path)
            retries -= 1
            if res or retries < 0:
                break
            sleep(1)

        print(f"{'Found' if res else 'Failed to find'}: {filename}")
        return res


    def is_need_https_showing(self,):
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
                "requestedUrl": f"{self.__url}",
                "runWarnings": [""],
                "audits": {
                    "metrics": {
                        "errorMessage": f"Failed to load {self.__url}",
                        "details": {
                            'items': [
                                {
                                    "firstContentfulPaint": -1,
                                    "largestContentfulPaint": -1,
                                    "interactive": -1,
                                    "speedIndex": -1,
                                    "totalBlockingTime": -1,
                                    "maxPotentialFID": -1,
                                    "cumulativeLayoutShift": -1,
                                    "cumulativeLayoutShiftMainFrame": -1,
                                    "lcpLoadStart": -1,
                                    "lcpLoadEnd": -1,
                                    "timeToFirstByte": -1,
                                    "observedTimeOrigin": -1,
                                    "observedTimeOriginTs": -1,
                                    "observedNavigationStart": -1,
                                    "observedNavigationStartTs": -1,
                                    "observedFirstPaint": -1,
                                    "observedFirstPaintTs": -1,
                                    "observedFirstContentfulPaint": -1,
                                    "observedFirstContentfulPaintTs": -1,
                                    "observedFirstContentfulPaintAllFrames": -1,
                                    "observedFirstContentfulPaintAllFramesTs": -1,
                                    "observedLargestContentfulPaint": -1,
                                    "observedLargestContentfulPaintTs": -1,
                                    "observedLargestContentfulPaintAllFrames": -1,
                                    "observedLargestContentfulPaintAllFramesTs": -1,
                                    "observedTraceEnd": -1,
                                    "observedTraceEndTs": -1,
                                    "observedLoad": -1,
                                    "observedLoadTs": -1,
                                    "observedDomContentLoaded": -1,
                                    "observedDomContentLoadedTs": -1,
                                    "observedCumulativeLayoutShift": -1,
                                    "observedCumulativeLayoutShiftMainFrame": -1,
                                    "observedFirstVisualChange": -1,
                                    "observedFirstVisualChangeTs": -1,
                                    "observedLastVisualChange": -1,
                                    "observedLastVisualChangeTs": -1,
                                    "observedSpeedIndex": -1,
                                    "observedSpeedIndexTs": -1
                                }
                            ]
                        }
                    }
                }


            }
        try:
            download_dir = f"{os.path.expanduser( '~' )}/Downloads"
            url = self.__url
            url = url.replace("https://", '')
            url = url.replace("http://", '')

            with open(f"{download_dir}/{url}-{datetime.now().strftime('%Y%m%dT%H%M%S')}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f)
        except Exception as err:
            print(f"Error writing error json file for: {self.__url}", err)


    def open_lh_panel(self):
        print("Pressing shortcut ctl+shift+p")
        pyautogui.hotkey('ctrl', 'shift', 'p')
        sleep(2)
        self.keyboard.type("lighthouse")
        sleep(1)
        self.keyboard.press(Key.enter)
        self.keyboard.release(Key.enter)




    def start_analysis(self):
        '''
            1. Check if we have lighthouse panel open or not.
              - Select an element in the page to inspect it - Ctrl + Shift + C
        '''


        # nput()

        # if the add new report button is not showing, open panel..

        if not self.is_img_showing("lighthouseText.png"):
            sleep(1)
            self.open_lh_panel()
            sleep(2)
            self.click_desktop_device()
            sleep(2)
            self.click_new_report() # Doesnt hurt to click after opening....
        else:
            self.click_new_report()

        # nput()

        sleep(2)
        # Check for errors first
        if self.is_img_showing("https_error.png"):
            print("Error loading page: need_https_showing")
            self.__download_failed_report()
            return False

        self.click_analyze_page_load()
        print("Do some polling image detection here.... open-cv should work")

        sleep(5) # Let lighthouse startup
        while self.is_cancel_btn_showing():
            sleep(3)

        # On captcha pages, the last reload places the inspector panel back to inpect, need to go back to lighthouse tab
        sleep(2)

        if not self.is_img_showing("lighthouseText.png"):
            self.open_lh_panel()

        sleep(1)
        self.click_download_menu()
        sleep(2)
        self.click_download()
        sleep(2)
        self.click_save()
        sleep(2)
        return True


