# mui ui layout parts abstract class
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class AbsParts(metaclass=ABCMeta):

    def __init__(self, name=None):
        self._name = name
        self._visible = True
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0

    @abstractmethod
    def getMatrix(self):
        raise NotImplementedError()

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
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

        