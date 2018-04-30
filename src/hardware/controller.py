#!/usr/bin/python3

import asyncio, evdev, time, threading

class Controller():
    """
    Requires xboxdrv already running.  Use the command:
    'sudo xboxdrv -s -d --deadzone 15% --trigger-as-button --dpad-as-button &'

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
    'ABS_HAT0Y' - D-Pad Y - (-1, 1)
    """

    MAX_JOYSTICK = 32767

    callbacks = {}

    leftX = 0
    leftY = 0
    rightX = 0
    rightY = 0

    def __init__(self, port=0):
        self.xbox = evdev.InputDevice('/dev/input/event' + str(port))
        asyncio.ensure_future(self.handleEvent(self.xbox))

    def bindCommand(self, button, callback):
        code = evdev.ecodes.ecodes[button]
        self.callbacks[code] = callback

    async def handleEvent(self, device):
        async for event in device.async_read_loop():
            print(str(event))
            if (event.type == evdev.ecodes.EV_KEY):
                btnEvent = evdev.categorize(event)
                if (btnEvent.keystate == evdev.KeyEvent.key_down):
                    if (event.code in self.callbacks):
                        self.callbacks[event.code]()

            elif (event.type == evdev.ecodes.EV_ABS):
                if (event.code == evdev.ecodes.ecodes['ABS_X']):
                    self.leftX = event.value / self.MAX_JOYSTICK
                elif (event.code == evdev.ecodes.ecodes['ABS_Y']):
                    self.leftY = event.value / -self.MAX_JOYSTICK
                elif (event.code == evdev.ecodes.ecodes['ABS_RX']):
                    self.rightX = event.value / self.MAX_JOYSTICK
                elif (event.code == evdev.ecodes.ecodes['ABS_RY']):
                    self.rightY = event.value / -self.MAX_JOYSTICK

    def start(self, loop):
        self.loop = loop
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def stop(self):
        print("Controller Stop")
        asyncio.gather(*asyncio.Task.all_tasks()).cancel()
        self.loop.stop()
