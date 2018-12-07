# -*- coding: utf-8 -*-

# mui sample app


import sys
import asyncio
from mui_ui import Display, MuiFont, Text, Widget, Border, TextAlignment, MotionEvent, InputEventListener, InputHandler , OnTouchEventListener   


class SampleUI(InputEventListener, OnTouchEventListener):

    def __init__(self):
        # connect to mui touchpanel
        self.input = InputHandler(self)

        # connect to mui display
        self.display = Display()

        # create application ui
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

        text2 = Text('---')
        text2.x = 0
        text2.y = 0
        text2.width = 100
        text2.height = 32
        self.ui.addParts(text2)
        
        self.views = {}
        self.views['text1'] = text1
        self.views['text2'] = text2

        self.touchCount = 0

    def updateUI(self):
        self.display.setLayout(self.ui.getMatrix())
        self.display.updateLayout()
        self.display.refreshDisplay(0, 100)

    def mainLoop(self):
        self.input.startEventLoop()

    def onInputEvent(self, e: MotionEvent):
        # dispatch touch event to all views
        self.ui.dispatchTouchEvent(e)
        #print(e)

    def onTouch(self, view, e: MotionEvent):
        # 
        if view is self.views['text1']:
            print('touched text view!')
            self.touchCount += 1
            msg = '-{:d}-'
            msg = msg.format(self.touchCount)
            print(msg)
            self.views['text2'].setText(msg)
            self.updateUI()


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

