#!/usr/bin/python3

import asyncio, evdev, time, threading

class Controller():
    """
    Buttons:
    'BTN_A' - A
    'BTN_B' - B
    'BTN_X' - X
    'BTN_Y' - Y
    'BTN_TL' - Left Bumper
    'BTN_TR' - Right Bumper
    'BTN_SELECT' - Select
    'BTN_START' - Start
    'BTN_MODE' - Xbox
    'BTN_THUMBL' - Left Thumb Press
    'BTN_THUMBR' - Right Thumb Press

    Axes:
    'ABS_X' - Left X - (-32768, 32767)
    'ABS_Y' - Left Y - (-32768, 32767)
    'ABS_RX' - Right X - (-32768, 32767)
    'ABS_RY' - Right Y - (-32768, 32767)
    'ABS_GAS' - Right Trigger - (0, 255)
    'ABS_BRAKE' - Left Trigger - (0, 255)
    'ABS_HAT0X' - D-Pad X - (-1, 1)
    'ABS_HAT0Y' - D-Pad Y - (-1,1)
    """

    MAX_JOYSTICK = 32767

    left = 0
    right = 0

    def __init__(self, port=0):
        self.xbox = evdev.InputDevice('/dev/input/event' + str(port))
        asyncio.ensure_future(self.print_events(self.xbox))

    async def print_events(self, device):
        async for event in device.async_read_loop():
            if (event.type == evdev.ecodes.EV_KEY):
                btnEvent = evdev.categorize(event)
                if (btnEvent.keystate == evdev.KeyEvent.key_down):
                    if (event.code == evdev.ecodes.ecodes['BTN_A']):
                        pass

            elif (event.type == evdev.ecodes.EV_ABS):
                if (event.code == evdev.ecodes.ecodes['ABS_Y']):
                    self.left = event.value / -self.MAX_JOYSTICK
                elif (event.code == evdev.ecodes.ecodes['ABS_RY']):
                    self.right = event.value / -self.MAX_JOYSTICK

    def start(self, loop):
        self.loop = loop
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def stop(self):
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        self.loop.stop()


if __name__ == '__main__':
    xbox = Controller()
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=xbox.start, args=(loop,))
    t.start()

    time.sleep(10)

    print("Left: " + str(xbox.left))
    print("Right: " + str(xbox.right))

    time.sleep(10)

    print("Left: " + str(xbox.left))
    print("Right: " + str(xbox.right))

    xbox.stop()
