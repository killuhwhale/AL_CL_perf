from enum import Enum
from appium.webdriver import Remote
from dataclasses import dataclass
import os
import re
import subprocess
from typing import Dict, Union
import __main__
from time import sleep, time
from appium.webdriver.common.appiumby import AppiumBy
from utils.device_utils import ArcVersions
from utils.utils import FACEBOOK_PACKAGE_NAME, file_exists


def get_root_path():
    ''' Returns root path /home/user/pathto/appium/src '''
    root_path = os.path.realpath(__main__.__file__).split("/")[1:-1]
    root_path = '/'.join(root_path)
    #root_path = 'Users/ethancox/Documents/appium/src'
    return f"/{root_path}"

def create_dir_if_not_exists(directory):
    print("Create dir if not exist", directory)
    if not os.path.exists(directory):
        print("Creating dir: ", directory)
        os.makedirs(directory)



def is_installed(package_name: str, transport_id: str) -> bool:
    """Returns whether package_name is installed.
    Args:
        package_name: A string representing the name of the application to
            be targeted.
    Returns:
        A boolean representing if package is installed.
    """
    cmd = ('adb', '-t', transport_id, 'shell', 'pm', 'list', 'packages')
    outstr = subprocess.run(cmd, check=True, encoding='utf-8',
        capture_output=True).stdout.strip()
    full_pkg_regexp = fr'^package:({re.escape(package_name)})$'
    regexp = full_pkg_regexp

    # IGNORECASE is needed because some package names use uppercase letters.
    matches = re.findall(regexp, outstr, re.MULTILINE | re.IGNORECASE)
    if len(matches) == 0:
        print(f'No installed package matches "{package_name}"')
        return False
    if len(matches) > 1:
        print(f'More than one package matches "{package_name}":')
        for p in matches:
            print(f' - {p}')
        return False

    return True

def uninstall_app(package_name: str, transport_id: str, force_rm: bool= False):
    '''
        Uninstalls app and waits 40 seconds or so while checking if app is still installed.
        Returns True once app is fianlly unisntalled.
        Returns False if it takes too long to unisntall or some other unexpected error.
    '''
    if  package_name in ['com.android.vending'] and not force_rm:
        print(f"Not uninstalling {package_name}")
        return False

    uninstalled = False
    try:
        print("Uninstalling ", package_name)
        cmd = ( 'adb', '-t', transport_id, 'uninstall', package_name)
        outstr = subprocess.run(cmd, check=True, encoding='utf-8', capture_output=True).stdout.strip()
        sleep(1)
        uninstalled = True
    except Exception as e:
        print("Error uninstalling: ", package_name, e)

    if uninstalled:
        try:
            sleep_cycle = 0
            while is_installed(package_name) and sleep_cycle <= 20:
                sleep(2)
                sleep_cycle += 1
        except Exception as e:
            return False
    return True

def is_ANR(dumpsys_act_text: str, package_name: str) -> bool:
    ''' Given a string, dumpsys_act_text, determine if an ANR window is present.

        ANR Text:
            mFocusedWindow=Window{afc9fce u0 Application Not Responding: com.thezeusnetwork.www}

        Params:
            dumpsys_act_text: Output from ADB dumpsys activity.
            package: The app's package name.

        Returns True if ANR text is present.
    '''
    regex = rf".*Application Not Responding: {package_name}.*"
    is_ANR_res = re.search(regex, dumpsys_act_text)
    print(f"{is_ANR_res=}")
    return not is_ANR_res is None

def dumpysys_activity(transport_id: str, ArcVersion: ArcVersions) -> str:
    try:
        keyword = ""
        if ArcVersion == ArcVersions.ARC_P:
            keyword = "mResumedActivity"
        if ArcVersion == ArcVersions.ARC_R:
            keyword = "mFocusedWindow"
        cmd = ('adb', '-t', transport_id, 'shell', 'dumpsys', 'activity', '|', 'grep', keyword)
        return subprocess.run(cmd, check=False, encoding='utf-8',
            capture_output=True).stdout.strip()
    except Exception as err:
            print("Err dumpysys_activity ", err)
    return ''

def get_cur_activty(transport_id: str, ArcVersion: ArcVersions, package_name: str) -> Dict:
    ''' Gets the current activity running in the foreground.
         adb shell dumpsys activity | grep mFocusedWindow

        Google Smart lock/ Save passwords to Google is problematic
        text=mFocusedWindow=Window{81b9105 u0 android}


        ARC-P
            mResumedActivity: ActivityRecord{9588d06 u0 com.netflix.mediaclient/o.cwK t127}
        ARC-R
            mFocusedWindow=Window{b3ef1fc u0 NotificationShade} ## Sleep
            mFocusedWindow=Window{3f50b2f u0 com.netflix.mediaclient/com.netflix.mediaclient.acquisition.screens.signupContainer.SignupNativeActivity}


        Failing on Barnes and Noble => Has pop up asking to join wifi networks...
            text = mFocusedWindow=Window{7cc92bd u0 android}

        Params:
            transport_id: The transport id of the connected android device.
            ArcVersion: ArcVersion Enum for the device.

        Returns:
            - A Dict containing:
                package_name: current focused package.
                act_name: The current focused activity.
                is_ANR_thrown: boolean indicating if ANR window is present.
                ANR_for_package: package name found in ANR message or empty string if is_ANR_thrown is False.
    '''
    MAX_WAIT_FOR_OPEN_APP = 420  # 7 mins
    t = time()
    while int(time() - t) < MAX_WAIT_FOR_OPEN_APP:
        text = dumpysys_activity(transport_id, ArcVersion)
        query = r".*{.*\s.*\s(?P<package_name>.*)/(?P<act_name>[\S\.]*)\s*.*}"
        result = re.search(query, text)

        if result is None:
            is_ANR_thrown = is_ANR(text, package_name)
            if "Software Agreement" in text:
                print("Software agreement is showing.", text)
            else:
                print("Cant find current activity.", f"{is_ANR_thrown=}", text)
            return {
                "package_name": '',
                "act_name": '',
                "is_ANR_thrown": is_ANR_thrown,
                "ANR_for_package": 'packge_name here'
            }

        print(f"get_cur_activty: {result.group('package_name')=} {result.group('act_name')=}")
        return  {
            "package_name": result.group("package_name"),
            "act_name": result.group("act_name"),
            "is_ANR_thrown": False,
            "ANR_for_package": ''
        }

    return {
        "package_name": '',
        "act_name": '',
        "is_ANR_thrown": False,
        "ANR_for_package": ''
    }


def check_and_close_smartlock(driver: Remote):
    cred_picker_acts = ["com.google.android.gms.auth.api.credentials.ui.CredentialPickerActivity", ".auth.api.credentials.ui.CredentialPickerActivity"]
    if driver.current_activity in cred_picker_acts:
        try:
            text = "NONE OF THE ABOVE"
            content_desc = f'''new UiSelector().className("android.widget.Button").text("{text}")'''
            el = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=content_desc)
            el.click()
        except Exception as error:
            print("Failed to click NONE OF THE ABOVE on Google Smart Lock.")



def open_app():
    ''' Opens an app using ADB monkey and waits until the app is open.

        Params:
            package_name: The name of the package to check crash logs for.
            transport_id: The transport id of the connected android device.
            ArcVersion: ArcVersion Enum for the device.
    '''
    # packages = [package_name, "com.google.android.permissioncontroller", "org.chromium.arc.applauncher"]
    app_name = "Chrome - Clank"
    package_name = "com.android.chrome/com.google.android.apps.chrome.Main"
    try:
        cmd = ["adb", "shell", "am", "start", "-n", "com.android.chrome/com.google.android.apps.chrome.Main"]

        outstr = subprocess.run(cmd, check=True, encoding='utf-8',
                                capture_output=True).stdout.strip()
        print(f"Starting {package_name} w/ monkey...")

    except Exception as err:
        print("Error opening app with monkey", err)
        return False

    return True

def is_app_open(package_name: str, transport_id: int):
    '''Open app looks for an act. But if something opens in fotn that is not associated with the package, likeSoftw3are Agreement or permissions, we wont detect properly
        instead of checking current package to see if app is open, we should check another command:
          - adb shell dumpsys activity processes | grep -i com.adsk.sketchbook

        If this returns anything, there the package is open.
    '''
    cmd = ['adb', '-t', transport_id, 'shell', 'dumpsys', 'activity', 'processes', "|", "grep", "-i", package_name]
    outstr = subprocess.run(cmd, check=False, encoding='utf-8',
                                capture_output=True).stdout.strip()
    return len(outstr) > 0

def close_app(package_name: str):
    '''
        Opens an app using ADB monkey.
        adb shell am broadcast -a android.intent.action.ACTION_SHUTDOWN

        Params:
            package_name: The name of the package to check crash logs for.
            transport_id: The transport id of the connected android device.
    '''
    try:
        cmd = ('adb', 'shell', 'am', 'force-stop', package_name)
        outstr = subprocess.run(cmd, check=True, encoding='utf-8',
                                capture_output=True).stdout.strip()
        print(f"Closed {package_name}...")
    except Exception as err:
        print("Error closing app ", err)
        return False
    return True

def clear_app(package_name: str, transport_id: str):
    ''' Clears an app's storage and cache data.
            adb shell pm clear <package_name>
    '''
    try:
        cmd = ('adb','-t', transport_id, 'shell', 'pm', 'clear', package_name)
        outstr = subprocess.run(cmd, check=True, encoding='utf-8',
                                    capture_output=True).stdout.strip()
        print(f"Clear app {outstr=}")
        return True
    except Exception as error:
        print(f"Error clearing {package_name=}: {error}")
    return False


def close_save_password_dialog(driver):
        '''
            Checks for a Not now button.

            We know a generic window show: mFocusedWindow=Window{81b9105 u0 android}
             where 81b9105 changes ea time.
        '''
        try:
            content_desc = f'''new UiSelector().className("android.widget.Button").text("Never")'''
            driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=content_desc).click()
        except Exception as error:
            print("Failed to click Never btn")

        try:
            content_desc = f'''new UiSelector().className("android.widget.Button").text("NOT NOW")'''
            driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=content_desc).click()
        except Exception as error:
            print("Failed to click NOt NOW btn")

        try:
            content_desc = f'''new UiSelector().className("android.widget.Button").text("NO THANKS")'''
            driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value=content_desc).click()
        except Exception as error:
            print("Failed to click No Thanks")


def is_package_installed(transport_id: str, package_name: str):
    ''' Checks if package is installed via ADB. '''
    # Call the adb shell pm list packages command
    result = subprocess.run(
        ['adb', '-t', transport_id, 'shell', 'pm', 'list', 'packages'],
        check=False, encoding='utf-8', capture_output=True
    ).stdout.strip()
    # Check the output for the package name
    return package_name in result

def is_download_in_progress(transport_id: str, package_name: str):
    ''' Runs the command:
        adb shell dumpsys activity services | grep <package_name>
        and if anything is returned, then return True as there is a download in progress.
        Good for waiting for games to downlaod extra content.
        adb shell dumpsys activity services | grep com.google.android.finsky.assetmoduleservice.AssetModuleService:com.xyz
    '''
    try:
        # command = f'adb -t {transport_id} shell dumpsys activity services | grep com.google.android.finsky.assetmoduleservice.AssetModuleService:{package_name}'
        # output = subprocess.check_output(command, shell=True).decode('utf-8')

        result = subprocess.run(
            ['adb', '-t', transport_id, 'shell', 'dumpsys', 'activity', 'services', "|", "grep", f"com.google.android.finsky.assetmoduleservice.AssetModuleService:{package_name}"],
            check=False, encoding='utf-8', capture_output=True
        ).stdout.strip()
        print(f"is_download_in_progress {result=}")
        return bool(result)
    except Exception as error:
        print("Error w/ checking download in progress")
        print(error)
    return False

def get_views(transport_id: str):
    ''' Creates an XML dump of current UI hierarchy.
    '''
    #  adb exec-out uiautomator dump /dev/tty
    result = subprocess.run(
            ['adb', '-t', transport_id, 'exec-out', 'uiautomator', 'dump', '/dev/tty'],
            check=False, encoding='utf-8', capture_output=True
        ).stdout.strip()
    print(f"Get_views {result=}")

# app_info_pattern = r".*(?:name='[0-9a-zA-Z.]*')?.*(?:versionCode='[0-9a-zA-Z.]*')?.*(?:versionName='[0-9a-zA-Z.]*')?.*(?:compileSdkVersion='[0-9a-zA-Z.]*')?.*(?:compileSdkVersionCodename='[0-9a-zA-Z.]*')?.*(?:platformBuildVersionName='[0-9a-zA-Z.]*')?"


class AppType(Enum):
    app = "App"
    game = "Game"
    pwa = "PWA"

@dataclass(frozen=True)
class AppData:
    ''' Represents app information that may be found in the Manifest file. '''
    name: str = ""
    versionCode: str = ""
    versionName: str = ""
    compileSdkVersion: str = ""
    compileSdkVersionCodename: str = ""
    platformBuildVersionName: str = ""
    app_type: AppType = AppType.app


class AppInfo:
    '''
        Manages the process of pulling APK from device, extracting the
         manifest text and parsing the manifest text for the information in
         @dataclass AppData

        package: name='air.com.lunime.gachaclub' versionCode='1001001' versionName='1.1.0'
        package: name='com.plexapp.android' versionCode='855199985' versionName='9.15.0.38159' compileSdkVersion='33' compileSdkVersionCodename='13'
        package: name='com.tumblr' versionCode='1280200110' versionName='28.2.0.110' compileSdkVersion='33' compileSdkVersionCodename='13'
    '''
    def __init__(self, transport_id: str, package_name: str, dprinter):
        self.transport_id = transport_id
        self.package_name = package_name
        self.__dprint = dprinter
        self.__info = {
                'name': '',
                'versionCode': '',
                'versionName': '',
                'compileSdkVersion': '',
                'compileSdkVersionCodename': '',
                'platformBuildVersionName' : '',
                'app_type': "",
            }
        self.__process_app()


    def __get_aapt_version(self) -> str:
        ''' Get the latest version of aapt on host device.

            Returns:
             - path of the latest version of aapt installed on host device.
        '''
        android_home = os.environ.get("ANDROID_HOME")
        # aapt = f"{android_home}/build-tools/*/aapt"
        aapt = f"{android_home}/build-tools/"
        items = os.listdir(aapt)

        # Iterate over the items
        for item in items[::-1]:
            return  os.path.join(aapt, item, "aapt")
        return ""

    def __check_chromium_webapk(self, manifest: str) -> bool:
        ''' Checks app's manifest to detect if the app is a PWA.

            Args:
             - manifest: A str containing the entire manifest text.

            Returns:
             - True if org.chromium.webapk.shell_apk is present in the manifest text.
        '''
        pattern = r".*org\.chromium\.webapk\.shell_apk.*"
        matches = re.findall(pattern, manifest, flags=re.MULTILINE)
        print(f"{matches=}")
        return True if matches else False

    def __has_surface_name(self) -> bool:
        ''' Checks SurfaceFlinger for a surface matching the package name.

            Returns:
                - True if there is a matching surface name.
        '''
        pattern_with_surface = f"""^SurfaceView\s*-\s*(?P<package>{self.package_name})/[\w.#]*$"""
        re_surface = re.compile(pattern_with_surface, re.MULTILINE | re.IGNORECASE | re.VERBOSE)
        cmd = ('adb', '-t', self.transport_id, 'shell', 'dumpsys', 'SurfaceFlinger', '--list')
        surfaces_list = subprocess.run(cmd, check=True, encoding='utf-8', capture_output=True).stdout.strip()
        last = None

        for match in re_surface.finditer(surfaces_list):
            print(f"Found surface match: ", match)
            last = match
        if last:
            if self.package_name != last.group('package'):
                self.__dprint(f"Found match for wrong package.")
                return False
            # UE4 games have at least two SurfaceView surfaces. The one
            # that seems to in the foreground is the last one.
            # return last.group()
            return True

        # Some apps will report a surface in use but will not have a SurfaceView.
        # E.g. Facebook messenger has surfaces views present while the user is on the login screen but it does not report a 'SurfaceView'

        # pattern_without_surface = rf"""^(?P<package>{package_name})/[\w.#]*$"""
        # re_without_surface = re.compile(pattern_without_surface, re.MULTILINE | re.IGNORECASE | re.VERBOSE)
        # # Fallback: SurfaceView was not found.
        # matches_without_surface = re_without_surface.search(surfaces_list)
        # if matches_without_surface:
        #     if package_name != matches_without_surface.group('package'):
        #         return False
        #         # return (f'Surface not found for package {package_name}. '
        #         #                 'Please ensure the app is running.')
        #     # return matches_without_surface.group()
        #     return True
        return False

    def __get_apk(self) -> bool:
        ''' Grabs the APK from device.

            adb shell pm path package_name

            package:/data/app/~~-TjCwRkZEFass6mjqTzMtg==/com.netflix.mediaclient-mPHhWQM2xwIJco8coL6OYg==/base.apk
            # package:/data/app/~~-TjCwRkZEFass6mjqTzMtg==/com.netflix.mediaclient-mPHhWQM2xwIJco8coL6OYg==/split_config.en.apk
            # package:/data/app/~~-TjCwRkZEFass6mjqTzMtg==/com.netflix.mediaclient-mPHhWQM2xwIJco8coL6OYg==/split_config.mdpi.apk
            # package:/data/app/~~-TjCwRkZEFass6mjqTzMtg==/com.netflix.mediaclient-mPHhWQM2xwIJco8coL6OYg==/split_config.x86_64.apk

            JUST NEED BASE APK FOR MAIN INFO

            Grabs APK via ADB PULL /path/to/apk
            and stores it in /apks/<package_name>

            Returns:
             - True when APK is in required location. False otherwise.
        '''
        print("Gettign APK ", self.package_name)
        if not is_package_installed(self.transport_id, self.package_name):
            return False

        root_path = get_root_path()
        dl_dir = f"{root_path}/apks/{self.package_name}"
        create_dir_if_not_exists(dl_dir)

        cmd = ('adb', '-t', self.transport_id, 'shell', 'pm', 'path', self.package_name )
        outstr = subprocess.run(cmd, check=True, encoding='utf-8',
                                    capture_output=True).stdout.strip()
        apk_path = None
        for line in outstr.split("\n"):
            # Remove package name from the line and check because asset exists
            # in the package name: com.cassette.aquapark
            rm_name_line = line.replace(self.package_name, "")
            if 'base.apk' in rm_name_line and not "asset" in rm_name_line:
                apk_path = line[len("package:"):]
        print(f"Found apk path: {apk_path}")
        if apk_path is None:
            self.__dprint(f"Failed to find APK path for {self.package_name}!!!!!!s\n", outstr)
            return False
        print("Pulling APK: ", self.package_name, dl_dir)
        cmd = ('adb', '-t', self.transport_id, 'pull', apk_path, dl_dir )
        outstr = subprocess.run(cmd, check=True, encoding='utf-8',
                                    capture_output=True).stdout.strip()
        return True

    def __download_manifest(self) -> str:
        ''' Grabs Manifest from the APK using aapt dump bading.

            Returns:
                - the manifest text.
        '''
        # /Android/Sdk/tools/bin/apkanalyzer manifest print /path/to/app.apk
        #     N: android=http://schemas.android.com/apk/res/android
        #   E: manifest (line=0)
        #     A: android:versionCode(0x0101021b)=(type 0x10)0xc49f
        #     A: android:versionName(0x0101021c)="8.52.2 build 14 50335" (Raw: "8.52.2 build 14 50335")
        # Need to download APK tho....
        # aapt dump badging my.apk | sed -n "s/.*versionName='\([^']*\).*/\1/p"
        # ./aapt2 dump xmltree --file AndroidManifest.xml /home/killuh/Downloads/com.netflix.mediaclient_8.52.2\ build\ 14\ 50335.apk
        # ./aapt dump xmltree /home/killuh/Downloads/com.netflix.mediaclient_8.52.2\ build\ 14\ 50335.apk AndroidManifest.xml
        # ./aapt dump xmltree app.apk AndroidManifest.xml


        aapt = self.__get_aapt_version()
        root_path = get_root_path()
        manifest_path = f"{root_path}/apks/{self.package_name}/manifest.txt"
        apk_path = f"{root_path}/apks/{self.package_name}/base.apk"

        if file_exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                return f.read()
        manifest = ""
        try:
            cmd = (aapt, "dump", "badging", apk_path)
            manifest = subprocess.run(cmd, check=False, encoding='utf-8',
                                    capture_output=True).stdout.strip()
        except Exception as error:
            print("Error getting manifest: ", error)
            return manifest

        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(manifest)

        return manifest

    def __populate_app_info(self, manifest_text: str):
        ''' Populates the App information from manifest text.

            Args:
             - manifest_text: Text from the apps manifest file in the APK.
        '''
        if not manifest_text:
            return Dict()
        info_line = manifest_text.split("\n")[0][len("package: "):]
        # package: name='com.netflix.mediaclient' versionCode='50352' versionName='8.56.0 build 12 50352' compileSdkVersion='33' compileSdkVersionCodename='13'
        regex = r"(?P<name>name='[\s\w\.]*')?(?P<versionCode>versionCode='[\s\w]*')?(?P<versionName>versionName='[\s\w\.]*')?(?P<compileSdkVersion>compileSdkVersion='[\s\w]*')?(?P<compileSdkVersionCodename>compileSdkVersionCodename='[\s\w\d]*')?(?P<platformBuildVersionName>platformBuildVersionName='[\s\w0-9]*')?"
        matches = re.finditer(regex, info_line)
        for matchNum, match in enumerate(matches, start=1):
            if match.end() - match.start() == 0:
                continue
            # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
            pieces = match.group().replace("'", "").split("=")
            self.__info[pieces[0]] = pieces[1]

        if self.__check_chromium_webapk(manifest_text):
            self.__info['app_type'] = AppType.pwa
        elif self.__has_surface_name():
            self.__info['app_type'] = AppType.game
        else:
            self.__info['app_type'] = AppType.app

    def __process_app(self) -> Union[AppData, None]:
        ''' Downloads APK & manifest from App and extracts information from Manifest.

            Returns:
                - A dict containing the app's information.
        '''
        if self.__get_apk():
            manifest = self.__download_manifest()
            if not manifest:
                self.__dprint("No manifest found!!!!")
                return None
            self.__populate_app_info(manifest)

    def info(self):
        return AppData(**self.__info)
