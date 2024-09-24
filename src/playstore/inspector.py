from random import gauss
import pyautogui
from pynput.keyboard import Key, Controller

from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC
import time



pyautogui.FAILSAFE = False

SCREEN_TOP_MARGIN = 28
WINDOW_TOP_MARGIN = 35


# Inspector UR bar
I_URL_BAR = (164, 67 + SCREEN_TOP_MARGIN + WINDOW_TOP_MARGIN) # x,y
keyboard = Controller()

def press(key):
    keyboard.press(key)
    keyboard.release(key)

@dataclass()
class InspectAL:

    url = "https://youtube.com"
    inspect_link_pattern = "//span[contains(text(), 'inspect')]"
    __driver = None
    __wait = None
    __window_height = 0
    __window_width = 0
    __x = 0
    __y = 0

    main_handle = None



    def open_devices(self):
        chrome_options = Options()
        chrome_service = Service()
        self.__driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.__driver.get("chrome://inspect/#devices")

        # Get Window info
        self.__window_width = self.__driver.get_window_size().get("width")
        self.__window_height = self.__driver.get_window_size().get("height")

        self.__x = self.__driver.get_window_position().get('x')
        self.__y = self.__driver.get_window_position().get('y')

        self.main_handle = self.__driver.window_handles[0]

        # Setup wait
        self.__wait = WebDriverWait(self.__driver, 10)
        time.sleep(3) # Wait for devices to appear


    def open_inspector(self, package_name):
        # Open inspector
        inspect_link = self.__driver.find_element(By.XPATH, self.inspect_link_pattern)
        inspect_link.click()
        self.__wait.until(EC.number_of_windows_to_be(2))
        new_window_handle = self.__driver.window_handles[-1]
        self.__driver.switch_to.window(new_window_handle)
        self.__driver.maximize_window()

    def switch_driver_to_main_window(self):
        self.__driver.switch_to.window(self.main_handle)

    def close_current_window(self):
        self.__driver.close()


    def __on_end(self):
        self.__driver.quit()


    def __click(self, pt=None):
        if pt is None:
            return
        x, y = pt
        print(f"Clicking: {x} {y} ")
        # TODO Randomize move tos
        pyautogui.moveTo(x, y, duration=gauss(0.4, .1))
        pyautogui.click()





    def __go_to_url(self, url):
        # using python to Click around, lets click on URL bar
        self.__click(I_URL_BAR)
        pyautogui.typewrite(url, 0.100)
        press(Key.enter)
        time.sleep(1000)


    def run(self):
        # self.open_devices()

        # self.__go_to_url("https://youtube.com/")

        # self.__on_end()
        pass



if __name__ == "__main__":
    inspect = InspectAL()
    # inspect.run()