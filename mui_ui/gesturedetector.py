# -*- coding: utf-8 -*-

# mui touch panel gesture detector class

try:
    from input import MotionEvent, VALUE_UP, VALUE_MOVE, VALUE_DOWN
except ImportError:
    from . import MotionEvent, VALUE_UP, VALUE_MOVE, VALUE_DOWN

from threading import Timer

SLOP_SQUARE = 64
MINIMUM_FLING_VELOCITY = 50
LONG_PRESS_TIMEOUT = 0.5 # sec

class GestureListener():

    def onScroll(self, e1: MotionEvent,  e2: MotionEvent, velocityX, velocityY):
        pass

    def onFling(self, e1: MotionEvent,  e2: MotionEvent, scrollX, scrollY):
        pass

    def onLongPress(self, e: MotionEvent):
        pass


class GestureDetector():
    def __init__(self, listener: GestureListener):
        self._gestureListener = listener
        self._lastX = 0
        self._lastY = 0
        self._lastFocusX = 0
        self._lastFocusY = 0
        self._inTapRegion = False
        self._downMotion = None
        self._longpressTimer = None

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

            self._longpressTimer = Timer(LONG_PRESS_TIMEOUT, self._dispathLongPress)
            self._longpressTimer.start()

        elif e.action == VALUE_MOVE and self._downMotion is not None:
            if self._inTapRegion:
                scrollX = self._lastFocusX - x
                scrollY = self._lastFocusY - y
                deltaX = x - self._lastX
                deltaY = y - self._lastY
                distance = (deltaX * deltaX) + (deltaY * deltaY)
                if distance > SLOP_SQUARE:
                    self._gestureListener.onScroll(self._downMotion, e, scrollX, scrollY)
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
                self._gestureListener.onFling(self._downMotion, e, velX, velY)

            if self._longpressTimer is not None:
                self._longpressTimer.cancel()

        else:
            self._cancel()

    def _dispathLongPress(self):
        self._gestureListener.onLongPress(self._downMotion)



