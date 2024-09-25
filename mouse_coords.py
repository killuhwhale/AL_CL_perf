from pynput import mouse, keyboard
import pyautogui

''' A program to find relative screen coordinates.

    When a click is received, the y coordinate is adjusted by the size of the screen and client margin.
'''

SCREEN_TOP_MARGIN = 28
WINDOW_TOP_MARGIN = 35


class MousePOS:
    def __init__(self):
        self.listener = None
        self.key_listener = None

    def on_click(self, x, y, button, pressed):
        if pressed and str(button) == 'Button.left':
            a = 2
            # print(
            #     f'abs coords {int(x)}, {int(y - SCREEN_TOP_MARGIN - WINDOW_TOP_MARGIN)}  Reg:  {int(x)}, {int(y)}')
            pass

        if not pressed:
            a = 2
            # Stop listener
            # return False
            pass

    def on_keypress(self, key):
        try:
            t = 1
            # print(f"Pressed: {key.char} - {key}")
            pass
        except AttributeError:
            # print(f"Special pressed: {key}")
            a = 2
            pass

    def on_release(self, key):
        # print(f'{key} released')

        if key == keyboard.Key.up:
            pyautogui.move(0, -1)
        if key == keyboard.Key.right:
            pyautogui.move(1, 0)
        if key == keyboard.Key.down:
            pyautogui.move(0, 1)
        if key == keyboard.Key.left:
            pyautogui.move(-1, 0)

        x, y = pyautogui.position()
        # print("Relative Coords")
        print(
            f'{int(x)}, {int(y - SCREEN_TOP_MARGIN - WINDOW_TOP_MARGIN)},')

        if key == keyboard.Key.esc:
            # Stop listener
            self.listener.stop()
            self.key_listener.stop()
            return False

    def start(self):
        # self.listener = mouse.Listener(
        #     on_click=self.on_click)
        self.key_listener = keyboard.Listener(
            on_press=self.on_keypress,
            on_release=self.on_release)
        # self.listener.start()
        self.key_listener.start()

        while True:
            pass


if __name__ == "__main__":
    tool = MousePOS()
    tool.start()