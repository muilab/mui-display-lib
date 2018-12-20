# -*- coding: utf-8 -*-

# mui sample app


import sys
import asyncio
import time

from threading import Lock
mutex = Lock()

from mui_ui import Display, MuiFont, Text, Image, Widget, Border, AbsApp, Message, DigitalClock
from mui_ui import TextAlignment, MotionEvent, InputEventListener, InputHandler, OnTouchEventListener, AppEventListener, OnUpdateRequestListener  
from mui_ui import GestureListener, GestureDetector

import os
dir = os.path.dirname(os.path.abspath(__file__))

class SampleUI(InputEventListener, OnTouchEventListener, GestureListener):

    def __init__(self):
        # connect to mui touchpanel
        self.input = InputHandler(self)

        # connect to mui display
        self.display = Display()

        # create application ui

        # clicable text view
        self.ui = Widget(200, 32) # max size
        text1 = Text('Hello\nPlease touch!')
        text1.setTextAlignment(TextAlignment.CENTER)
        text1.setBorder(Border.AROUND)
        text1.x = 100
        text1.y = 0
        text1.width = 100
        text1.height = 32
        text1.addOnTouchViewListener(self)
        self.ui.addParts(text1)

        # text view as label
        text2 = Text('---')
        text2.x = 0
        text2.y = 0
        text2.width = 100
        text2.height = 10
        self.ui.addParts(text2)

        # add weather icon
        fileName1 = os.path.normpath(os.path.join(dir, './icon_weather.png'))
        icon1 = Image(fileName1)
        icon1.addOnTouchViewListener(self)
        # add clock icon
        fileName2 = os.path.normpath(os.path.join(dir, './icon_clock.png'))
        icon2 = Image(fileName2)
        # add clock icon
        fileName4 = os.path.normpath(os.path.join(dir, './icon_sound.png'))
        icon4 = Image(fileName4)
        # add voice icon
        fileName3 = os.path.normpath(os.path.join(dir, './icon_voice.png'))
        icon3 = Image(fileName3)
        
        # create icon widget
        icons = Widget((icon1.width + icon2.width + icon4.width + icon3.width), max(icon1.height, icon2.height, icon3.height, icon4.height))
        icons.x = 0
        icons.y = 32 - icons.height
        self.ui.addParts(icons)

        # add icons to icon widget
        icons.addParts(icon1)
        icon2.x = icon1.width
        icons.addParts(icon2)
        icon4.x = icon2.x + icon2.width
        icons.addParts(icon4)
        icon3.x = icon4.x + icon4.width
        icons.addParts(icon3)

        # create gesture detector (for catch swipe action)
        self._gestureDetector = GestureDetector(self)

        self.views = {}
        self.views['text1'] = text1
        self.views['text2'] = text2
        self.views['icons'] = icons
        self.views['icon_weather'] = icon1

        self.touchCount = 0

    def updateUI(self, fade=0):
        mutex.acquire()
        # set layout data
        self.display.setLayout(self.ui.getMatrix())
        # update Display internal data buffer (does not refesh display)
        self.display.updateLayout()
        # refresh Display
        self.display.refreshDisplay(fade, 100)
        mutex.release()

    def mainLoop(self):
        self.input.startEventLoop()

    def onInputEvent(self, e: MotionEvent):
        # dispatch touch event to all views
        self.ui.dispatchTouchEvent(e)

        # determin gesture
        self._gestureDetector.onTouchEvent(e)

    def onTouch(self, view, e: MotionEvent):
        # handling touch events
        if view is self.views['text1']:
            print('touched text view!')

            # increment touch count
            self.touchCount += 1
            msg = '-{:d}-'
            self.views['text2'].setText(msg.format(self.touchCount))

            # toggle icon visible
            # when views is invisible, do not occur touch event
            self.views['icons'].visible = not self.views['icons'].visible

            # update UI
            self.updateUI()

        elif view is self.views['icon_weather']:
            print('touched weather icon')

    def onScroll(self, e1: MotionEvent,  e2: MotionEvent, x, y):
        # handling scroll event
        print('** scroll **')

    def onFling(self, e1: MotionEvent,  e2: MotionEvent, x, y):
        # handling swipe event
        print('*** swipe ***')



if __name__ == "__main__":
    try:
        app = SampleUI()

        # draw UI
        app.updateUI()

        # start capture touch panel event
        app.mainLoop()
    except (KeyboardInterrupt, EOFError):
        pass

    sys.exit(0)

