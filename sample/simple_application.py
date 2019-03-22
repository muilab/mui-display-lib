# -*- coding: utf-8 -*-

# mui simple application sample

from mui_ui import Display, Text, Widget, AbsApp, Message
from mui_ui import MotionEvent, InputEventListener, InputHandler, OnTouchEventListener, AppEventListener, OnUpdateRequestListener  
from mui_ui import GestureListener, GestureDetector

from threading import Lock
mutex = Lock()


class SimpleApplication(AbsApp, InputEventListener, OnTouchEventListener, GestureListener):

    def __init__(self, parameter_list):
        super().__init__(None)

        # connect to mui display
        self.display = Display()

        # you can choice LED brightness(1 - 100)
        self.display.setDuty(100)

        # connect to mui touchpanel(and set InputEventListener)
        self.input = InputHandler(self)

        # create gesture detector for swipe and long press event(and set GestureListener)
        self._gestureDetector = GestureDetector(self)

        # create UI
        text = Text('Hello world')
        text.setSize(0, 0, 100, 32) # set position and size (x, y, width, height)
        self.addView(text) # add view to this application
        self.setView(text, 'text') # set view with reference key. when you'd like to access this view, you can get this view via self.getView('key')
        self.addOnTouchViewListener(self) # set callback method(onTouch()) to catch touch event. 


    def mainLoop(self):
        # start touch event loop
        self.input.startEventLoop()

    def startTask(self):
        pass

    def stopTask(self):
        pass

    def updateUI(self, fade=0):
        """
        update UI.
        """
        with mutex:
            if fade > 0:
                # fade out(0 - 4 : 0 is do not fade, 4 is very slow)
                self.display.turnOff(fade)

            # set layout data
            self.display.setLayout(self.getUI())
            # update Display internal data buffer (do not refesh display until call refreshDisplay())
            self.display.updateLayout()
            # refresh Display
            self.display.refreshDisplay()

            if fade > 0:
                # fade in(0 - 4)
                self.display.turnOn(fade)

    def onInputEvent(self, e: MotionEvent):
        # dispatch touch event to all views
        self.dispatchTouchEvent(e)

        # determin gesture
        self._gestureDetector.onTouchEvent(e)

    def onTouch(self, view, e: MotionEvent):
        # handling touch events
        pass

    def onFling(self, e1: MotionEvent,  e2: MotionEvent, x, y):
        # handling swipe event
        print('*** swipe ***')



if __name__ == "__main__":
    try:
        app = SimpleApplication()

        # draw UI
        app.updateUI()

        app.startTask()

        # start capture touch panel event
        app.mainLoop()

    except (KeyboardInterrupt, EOFError):
        pass

    sys.exit(0)
