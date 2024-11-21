
"""Main entry point to running search, install, launch, login, reporting.
                                    SILLR
To run this script with the CLI:
Syntax:
python3 main.py [-c --clean] -i --ip <ip-addresses>

Arguments:
    ips: (Required) ip addresses of the DUT.

Example:
    # Pixel Tablet
    python3 main.py -i 192.168.1.167:34713
    python3 main.py -i 192.168.1.125:5555 192.168.1.113:5555       # Single run
    python3 main.py -i 192.168.1.238:5555 -n 1  # Single run w/ 1 app (starting from beginning of list)
    python3 main.py -p -i 192.168.1.125:5555 192.168.1.113:5555    # Parallel Run
"""

import argparse
from datetime import datetime
from appium import webdriver
import logging
from playstore.app_validator import AppValidator

from serviceManager.appium_service_manager import AppiumServiceManager
from utils.device_utils import Device, adb_connect
from utils.logging_utils import AppLogger, logger
from utils.utils import BASE_PORT, CONFIG, PLAYSTORE_MAIN_ACT, PLAYSTORE_PACKAGE_NAME, android_des_caps, android_options
from uuid import uuid1





IP = ""

def main():
    parser = argparse.ArgumentParser(description="App validation.")
    parser.add_argument("-c", "--clean",
                        help="Clean up appium server..",
                        action='store_true')
    parser.add_argument("-i", "--ips",
                        help="Ip address of DUTs.",
                        nargs="*",
                        default=[], type=str)

    run_id = uuid1(1337, 42)
    ts = int(datetime.now().timestamp()*1000)
    args = parser.parse_args()
    ips = args.ips


    logger.print_log(f"CLI input: {ips=}\n")
    logger.print_log(f"Config", CONFIG, '\n')
    logger.print_log(f"{run_id=}\n")
    logger.print_log(f"Start time {ts=}\n")

    ip = ips[0] if not args.clean else ""
    IP = ip
    service_manager = AppiumServiceManager([ip])
    if args.clean:
        service_manager.cleanup_services()  # Will exit
    service_manager.start_services()

    adb_connect(ip)


    print("Creating driver...")
    PACKAGE = "com.chrome.canary"
    ACTIVITY = "com.google.android.apps.chrome.Main"
    try:

        options = android_options(
            ip,
            PACKAGE,
            ACTIVITY
        )
        caps = android_des_caps(
            ip,
            PACKAGE,
            ACTIVITY
        )

        driver = webdriver.Remote(
            f"http://localhost:{BASE_PORT}/wd/hub",
            caps
        )
        print("Starting to wait")
        driver.implicitly_wait(5)
        driver.wait_activity(ACTIVITY, 5)

        print("Starting validator!")
        validator = AppValidator(
            driver,
            None,
            chrome_channel="com.chrome.canary",
        )
        validator.run()
    except Exception as err:
        print("Error in main: ")
        print(err)
        # print( err.with_traceback())


if __name__ == "__main__":
    try:
        logging.basicConfig(filename='crash.log', filemode='w', level=logging.ERROR)
        main()
    except Exception as e:
        logging.critical("main crashed")
        print("Main crashed: ", e)

    service_manager = AppiumServiceManager([IP])
    service_manager.cleanup_services()  # Will exit


