import time
from typing import List
from google.cloud import storage

from utils.logging_utils import AppLogger

from utils.app_utils import close_app, open_app

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException

from appium.webdriver import Remote
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass, field


from playstore.inspector import InspectAL

# Instantiates a client
storage_client = storage.Client()
# inspector = InspectAL()



def get_domain(url):
    domain = ""
    if url.startswith('http://'):
        domain = url[7:]
    elif url.startswith('https://'):
        domain = url[8:]
    else:
        domain = url
    return domain.split(".")[0]


def titleIsReady(expectedTitle):
    def checkTitle(d):
        try:
            print(f"{d=}")
            doc_title = d.execute_script("return document.title").lower()
            body_found = d.execute_script("return document.body !== null;")
            # body_found = EC.presence_of_element_located((AppiumBy.TAG_NAME, "body"))
            print(f"{expectedTitle.lower()} in {doc_title=} {body_found=}")

            return expectedTitle.lower() in doc_title and body_found
        except Exception as err:
            print(f"Doc ready err: ", err)
        return ""

    return checkTitle

def safe_find_element(driver, locator, retries=3):
    """
    Safely finds an element with retries in case of a StaleElementReferenceException.
    """
    for attempt in range(retries):
        try:
            # Wait for the element to be located
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException caught, retrying... ({attempt + 1}/{retries})")
            if attempt == retries - 1:
                raise  # Re-raise the exception if we've exhausted all retries


@dataclass(order=True, unsafe_hash=True)
class AppStats:
    load_time: float = 0 # Average load time
    app_name: str = "name-here"
    num_loaded: int = 0# Number of time app was loaded
    load_times: List[float] = field(default_factory=list)

    def __str__(self):
        return f"{self.app_name};{self.load_time};{self.num_loaded};{self.load_times}"

class AppValidator:
    ''' Main class to validate a broken app. Discovers, installs, opens and
          logs in to apps.
    '''
    def __init__(
            self,
            driver: Remote,
            app_logger: AppLogger,
        ):
        self.__driver = driver
        self.__app_logger = app_logger
        self.dev_ss_count = 8
        self.__stats: List[AppStats] = []

    def __print_stats(self):

        print()
        print("Session Stats: ")
        print("_______________")
        print("Name;Load Time;Num Loaded;Load Times")
        for stat in self.__stats:
            print(stat)
        print()


    def __newTabButtonExists(self):
        try:
            self.__driver.find_element(AppiumBy.ACCESSIBILITY_ID, "New tab")  # May vary based on localization
            return True
        except Exception as err:
            print("New tab DNE")
        return False

    def __closeTabs(self):
        print("Closing tabs")
        # The button to access the tab overview can be located by its content description
        try:
            tab_menu = safe_find_element(self.__driver, (AppiumBy.ACCESSIBILITY_ID, "Switch or close tabs"))
            tab_menu.click()

            chrome_menu = self.__driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Customize and control Google Chrome")
            chrome_menu.click()

            close_all_item = self.__driver.find_element(AppiumBy.ID, "com.android.chrome:id/close_all_tabs_menu_id")
            close_all_item.click()

            confirm_btn = self.__driver.find_element(AppiumBy.ID, "com.android.chrome:id/positive_button")
            confirm_btn.click()



            # close_button = self.__driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, '''new UiSelector().descriptionMatches(\"^Close.*\")''')
        except Exception as err:
            print("Unable to open tab overview: ", err)
            return


    def __check_site(self, url) -> float:
        try:

            # search_bar = self.__driver.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
            # Enter the URL to navigate to and hit enter
            print("Opening site: ", url)

            # search_bar.send_keys(url)

            self.__closeTabs()
            self.__driver.get(url)

            # Get available contexts
            print(f"{self.__driver.contexts=}")  # This will print a list of contexts like ['NATIVE_APP', 'WEBVIEW_1']
            WebDriverWait(self.__driver, 20).until(lambda x: 'WEBVIEW_chrome' in self.__driver.contexts)
            print(f"{self.__driver.contexts=}")
            # Switch to web context
            self.__driver.switch_to.context('WEBVIEW_chrome')  # You need to switch to the web context for Chrome

            print("Start timing the page load")
            start_time = time.time()

            print("self.__driver: ", dir(self.__driver))
            # No more webview context...
            # Wait for the page to load (use some element on the page to verify)

            WebDriverWait(self.__driver, 20).until(titleIsReady(get_domain(url)))

            end_time = time.time()
            print("Stop the timer")

            # Calculate the time taken to load the page
            load_time = end_time - start_time
            print(f"Page loaded in {load_time:.2f} seconds")




            # Switch back to native context if needed
            self.__driver.switch_to.context('NATIVE_APP')

            return load_time
        except Exception as err:
            print("Error checking site: ", err)

        return 100

    def __new_tab(self):
        try:
            print("Opening new tab")
            # Thiws button is actually hidden currently, maybe we can change window size, click, maximzie
            # new_btn_button = self.__driver.find_element(AppiumBy.ACCESSIBILITY_ID, "New tab")  # May vary based on localization
            # new_btn_button.click()
            # new_btn_button.click()
            for _ in range(4):
                self.__driver.press_keycode(61)  # KEYCODE_TAB
                time.sleep(0.5)  # Add a small delay between presses

            # Press the Up Arrow key once
            self.__driver.press_keycode(19)  # KEYCODE_DPAD_UP
            time.sleep(0.5)

            # Press the Enter key
            self.__driver.press_keycode(66)  # KEYCODE_ENTER
            print("new tab clicked")
            # Press the Tab key 4 times
        except Exception as err:
            print("Unable to open new tab: ", err)
        print("new tab opened")


    def __inspect_site(self, package_name: str):
        print("Inspecting: ", package_name)
        # Site is open, open inspector
        # inspector.open_inspector(package_name)

        # Press reload record....
        # Download data

        # Close inspector
        # inspector.close_current_window()
        # inspector.switch_driver_to_main_window()



    def __process_app(self, package_name: str):
        '''


            In the log you posted, we see a variety of 0001, 0003, and 0000 events. These correspond to the following:

            0001: This indicates a key press event.
            0003: This indicates an absolute position event (touchscreen coordinates).
            0000: This marks the end of an event batch.
            Steps to Identify the Key Press (Enter/Submit):
            Keycode Line: The line that starts with 0001 014a 00000001 is the key event itself:

            0001: This indicates a key event.
            014a: This is the keycode (in hexadecimal) for the key that was pressed.
            00000001: This indicates the key press action (where 1 means key down, and 0 means key up).
            Translate the Keycode: The keycode in hex 014a needs to be converted to a decimal value to match Android keycodes.

            014a (hex) = 330 (decimal).
            Check the Keycode Mapping: According to Android's keycode reference, keycode 330 corresponds to KEY_OK, which is typically used for "action" buttons, often corresponding to an enter or submit action on a virtual keyboard.
        '''

        print("\n\n  Navigate to websites and check stuff here: \n\n\n")
        load_time = self.__check_site(package_name)
        # self.__inspect_site(package_name)



        print("Done testing on browser!")

    def __read_apps(self):
        apps = []
        try:
            with open("apps.csv" , 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    apps.append(line.split(",")[0].strip("\n"))
        except Exception as err:
            print(f"Error reading apps: ", err)
        return apps

    ##  Main Loop
    def run(self):
        '''
            Main loop of the Playstore class, starts the cycle of discovering,
            installing, logging in and uninstalling each app from self.__package_names.

            It ensures that the playstore is open at the beginning and that
            the device orientation is returned to portrait.
        '''
        print("Starting process_app!")

        # self.__driver.orientation = 'PORTRAIT'

        # Load devices before navigating to website
        # inspector.open_devices()
        print("Done openings device tab...")

        app_names = self.__read_apps()
        print("Testing apps: ", app_names)

        for app in app_names:
            print("Processing: ", app)
            self.__process_app(app)

        self.__print_stats()


if __name__ == "__main__":
    pass