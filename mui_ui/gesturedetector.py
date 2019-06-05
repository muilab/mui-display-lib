# -*- coding: utf-8 -*-

# mui touch panel gesture detector class

try:
    from input import MotionEvent, VALUE_UP, VALUE_MOVE, VALUE_DOWN
except ImportError:
    from . import MotionEvent, VALUE_UP, VALUE_MOVE, VALUE_DOWN

from threading import Timer

SLOP_SQUARE = 64
MINIMUM_FLING_VELOCITY = 50
LONG_PRESS_TIMEOUT = 3 # sec

class GestureListener(object):

    def onScroll(self, e1: MotionEvent,  e2: MotionEvent, scrollX, scrollY) -> bool:
        return False

    def onFling(self, e1: MotionEvent,  e2: MotionEvent, velocityX, velocityY) -> bool:
        """
        this method invoked when swipe event occured.

        Parameters
        ------------
        e1 : MotionEvent
            start position of swipe event
        e2 : MotionEvent
            end position of swipe event
        velocityX : int
            distance between e1.x and e2.x
        velocityY : int
            distance between e1.y and e2.y
        """
        return False

    def onLongPress(self, e: MotionEvent):
        """
        this method invoked when long press event occured.

        Parameters
        ------------
        e : MotionEvent
            event data of started long press
        """
        pass


class GestureDetector(object):
    """
    GestureDetector can determin touch gestures like swipe, scroll, long press.
    When occure these gesture event, call callback method of GestureListener.

    USAGE:

    class App(InputEventListener, GestureListener):
        def __init__(self):
            # create input event handler
            self._input = InputHandler(self)

            # create gesture detector
            self._gesturedetector = GestureDetector(self)

        def mainLoop(self):
            # start capture touch event
            self._input.startEventLoop()

        def onInputEvent(self, e: MotionEvnet):
            # pass motion event data to gesture detector
            self._gesturedetector.onTouchEvent(e)

        def onFling(self, e1: MotionEvent,  e2: MotionEvent, scrollX, scrollY):
            # handling swipe event

        def onLongPress(self e: MotionEvent):
            # handling long press event


    # start application
    app = App()
    app.mainLoop()
    
    """

    def __init__(self, listener: GestureListener, longpress_timeout = LONG_PRESS_TIMEOUT):
        """
        Parameters
        ------------
        listener: GestureListener
            callback

        longpress_timeout: number
            if user keep touch-down and does not move position over this time(seconds), fire long press event.
        """
        self._gestureListener = listener
        self._lastX = 0
        self._lastY = 0
        self._lastFocusX = 0
        self._lastFocusY = 0
        self._inTapRegion = False
        self._downMotion = None
        self._longpressTimer = None
        self._longpress_timeout = longpress_timeout

    def _cancel(self):
        self._lastX = 0
        self._lastY = 0
        self._lastFocusX = 0
        self._lastFocusY = 0
        self._inTapRegion = False
        self._downMotion = None

        if self._longpressTimer is not None:
            self._longpressTimer.cancel()
        self._longpressTimer = None

    def onTouchEvent(self, e: MotionEvent):
        """
        please pass MotionEvent to this method. when determin gesture, fire target event via GestureListener.

        Parameters
        ------------
        e : MotionEvent
            motion event data that you can get from InputHandler class.
        """
        handle = False
        x = e.x
        y = e.y

        if e.action == VALUE_DOWN:
            self._lastX = x
            self._lastY = y
            self._lastFocusX = x
            self._lastFocusY = y
            self._inTapRegion = True
            downMotion = MotionEvent()
            downMotion.copy(e)
            self._downMotion = downMotion

            if self._longpressTimer is not None:
                self._longpressTimer.cancel()

            self._longpressTimer = Timer(self._longpress_timeout, self._dispathLongPress)
            self._longpressTimer.start()

        elif e.action == VALUE_MOVE and self._downMotion is not None:
            if self._inTapRegion:
                scrollX = self._lastFocusX - x
                scrollY = self._lastFocusY - y
                deltaX = x - self._lastX
                deltaY = y - self._lastY
                distance = (deltaX * deltaX) + (deltaY * deltaY)
                if distance > SLOP_SQUARE:
                    handle = self._gestureListener.onScroll(self._downMotion, e, scrollX, scrollY)
                    self._lastFocusX = x
                    self._lastFocusY = y
                    self._inTapRegion = False

            if self._longpressTimer is not None:
                self._longpressTimer.cancel()


        elif e.action == VALUE_UP and self._downMotion is not None:
            deltaT = (e.timestamp - self._downMotion.timestamp) * 1000
            deltaX = abs(x - self._lastX)
            deltaY = abs(y - self._lastY)
            velX = (deltaX / deltaT) * 1000
            velY = (deltaY / deltaT) * 1000
            if (velX > MINIMUM_FLING_VELOCITY) or (velY > MINIMUM_FLING_VELOCITY):
                handle = self._gestureListener.onFling(self._downMotion, e, velX, velY)
                self._cancel()

            if self._longpressTimer is not None:
                self._longpressTimer.cancel()

        else:
            self._cancel()

        return handle

    def _dispathLongPress(self):
        self._gestureListener.onLongPress(self._downMotion)



