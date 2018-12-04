# mui touch panel event class
# -*- coding: utf-8 -*-

import asyncio
import evdev

EV_SYN = 0x00   # event type sync
SYN_REPORT = 0  # event code sync report

EV_KEY = 0x01       # event type key (touch down or up)
BTN_TOUCH = 0x14a   # event code touch
VALUE_DOWN = 1      # event value down
VALUE_UP = 0        # evnet value up

EV_ABS = 0x03   # event type Axis postion report
ABS_X = 0x00    # event code Axis X
ABS_Y = 0x01    # event code Axis Y

def inputEventListener(action, x, y):
    """
    Callback for input event from mui touch panel 
    """
    pass 

class InputHandler():

    def __init__(self, listener:inputEventListener):
        self.inputEventListener = listener

        # get mui touch panel
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if device.name == 'Atmel maXTouch Touchscreen':
                print(device)
                self.device = device
    
    def startEventLoop(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.eventLoop())

    async def eventLoop(self):
        async for ev in self.device.async_read_loop():
            # handle input event
            pass

    def handleInputEvent(self, action, x, y):
        self.inputEventListener(action, x, y)



