# -*- coding: utf-8 -*-

# mui ui / slider parts class

try:
    from matrix import Matrix
    from widget import Widget
    from image import Image
    from input import MotionEvent, VALUE_DOWN, VALUE_MOVE, VALUE_UP
except ImportError:
    from . import Matrix, Widget, Image, MotionEvent, VALUE_DOWN, VALUE_MOVE, VALUE_UP

import os
dir = os.path.dirname(os.path.abspath(__file__))


class SliderEventListener:

    def onSliderValueChanged(self, prevVal, newVal):
        pass


class Slider(Widget):
    def __init__(self, width, maxVal, name='slider'):
        super().__init__(width=width, height=11, name=name)

        self._max = maxVal    
        self._thumbPos = 0   

        # add base line
        sliderBar = Image()
        sliderBar.setSize(0, 6, width, 1)
        barData = Matrix(width, 1)
        for x in range(width):
            barData.matrix[0][x] = 1
        sliderBar.setImageData(barData)
        self.addParts(sliderBar)

        # add thumb
        sourceName = './assets/slider_thumb_large.png'
        sourcePath = os.path.normpath(os.path.join(dir, sourceName))
        sliderThub = Image(sourcePath)
        sliderThub.setSize((width // 2) - 4, 2, 9, 9)
        self.addParts(sliderThub)

        self._views = {}
        self._views["thumb"] = sliderThub

        self._isMoving = False
        self._lastUpdate = 0

        self._sliderListener = None


    def addEventListener(self, listener: SliderEventListener):
        self._sliderListener = listener

    def getValue(self):
        return int((self._thumbPos // (self.width / self._max)))

    def setValue(self, value):
        if value > self._max:
            value = self._max
        elif value < 0:
            value = 0

        self._thumbPos = int((self.width / self._max) * value)
        self._views["thumb"].x = self.x + (self._thumbPos - 4)


    def dispatchTouchEvent(self, e: MotionEvent):
        action = e.action
        if (action == VALUE_MOVE) and self._isMoving is False:
            return

        if (action != VALUE_MOVE) and (self.hitTest(e.x, e.y) is False):
            self._isMoving = False
            return

        self._isMoving = True
        if action == VALUE_UP:
            self._isMoving = False

        oldValue = self.getValue()
        oldX = self._views["thumb"].x

        self._thumbPos = e.x - self.x
        if self._thumbPos < 0:
            self._thumbPos = 0
        elif self._thumbPos > self.width:
            self._thumbPos = self.width

        newX = self.x + (self._thumbPos - 4)
        if newX > (self.x + self.width - 6):
            newX = self.x + self.width - 6
        self._views["thumb"].x = newX

        # no need to change
        if newX == oldX:
            if action == VALUE_UP and self._sliderListener is not None:
                self._sliderListener.onSliderValueChanged(oldValue, self.getValue())
            return

        self._isChange = True
        time = e.timestamp
        if time - self._lastUpdate < 0.015:
            # if very close to previous update time, skip this update request
            self._lastUpdate = time
            return
        
        self._lastUpdate = time

        # display update request
        if self.OnUpdateRequestListener is not None:
            self.OnUpdateRequestListener.onUpdateView(self)





    
