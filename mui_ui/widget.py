# mui ui text view class
# -*- coding: utf-8 -*-

import time

try:
    from parts import AbsParts
    from matrix import Matrix
    from input import MotionEvent
except ImportError:
    from . import AbsParts
    from . import Matrix


class Widget(AbsParts):
    """
    Widget is multi parts(view) holder.
    If you'd like to treat multi parts as one view, please add to widget
    """

    def __init__(self, width=0, height=0, name='widget'):
        super().__init__(name)
        self._partsList = []
        self.width = width
        self.height = height
        #self.m = Matrix(width, height)

    def addParts(self, parts:AbsParts):
        parts.x = self.x + parts.x
        parts.y = self.y + parts.y
        self._partsList.append(parts)

    def setSize(self, x, y, width, height):
        diffX = x - self._x
        diffY = y - self._y

        super().setSize(x, y, width, height)

        for p in list(self._partsList):
            p.x = p.x + diffX
            p.y = p.y + diffY


    def dispatchTouchEvent(self, e):
        parts = self._partsList
        for p in reversed(list(parts)):
            if p.visible is True:
                result = p.dispatchTouchEvent(e)
                if result is True:
                    return True

        return False


    def getMatrix(self):

        # s = time.time()
        # if self._isChange is False:
        #     return self.m
        # else:
        #     self.m = Matrix(self.width, self.height)
        #     self.m.startX = self.x
        #     self.m.startY = self.y

        # m = self.m
        m = Matrix(self.width, self.height)
        m.startX = self.x
        m.startY = self.y
        parts = self._partsList

        for p in parts:
            if p.visible == True:
                m.merge(p.getMatrix())


        # e = time.time()
        # print('*** merge ', (e - s))
        self._isChange = False
        return m