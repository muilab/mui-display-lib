# mui ui layout parts abstract class
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from evdev import ecodes

try:
    from input import MotionEvent
except ImportError:
    pass
#    from . import InputEventListener
#    from . import MotionEvent


class OnTouchEventListener():

    def onTouch(self, view, e):
        """
        callback method to be invoked when a touched target view.

        Parameters
        -----------
        view : AbsParts
            target view instance
        e : Motionevent
            motion event
        """
        raise NotImplementedError


class OnUpdateRequestListener():

    def onUpdateView(self, view):
        pass



class AbsParts(metaclass=ABCMeta):

    def __init__(self, name=None):
        self._name = name
        self._visible = True
        self._isChange = True
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        self.OnTouchEventListener = None
        self.OnUpdateRequestListener = None

    @abstractmethod
    def getMatrix(self):
        raise NotImplementedError()

    def addOnTouchViewListener(self, listener: OnTouchEventListener):
        self.OnTouchEventListener = listener

    def addOnUpdateViewListener(self, listener: OnUpdateRequestListener):
        self.OnUpdateRequestListener = listener

    def setSize(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._isChange = True

    def dispatchTouchEvent(self, e):
        #print('-- dispatchTouchEvent() --')
        if (self.OnTouchEventListener != None) and (e.action == 0) and self.hitTest(e.x, e.y):
            self.OnTouchEventListener.onTouch(self, e)
            return True

        self.onTouch(e)
        return False

    def onTouch(self, e):
        pass

    def hitTest(self, x, y):
        if self._visible == False:
            return False

        l = self._x
        t = self._y
        r = self._x + self._width
        b = self._y + self._height
        return ((x >= l) and (x <= r) and (y >= t) and (y <= b))


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible):
        self._visible = visible

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self.setSize(x, self._y, self._width, self._height)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self.setSize(self._x, y, self._width, self._height)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self.setSize(self._x, self._y, width, self._height)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self.setSize(self._x, self._y, self._width, height)

        