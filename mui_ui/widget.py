# mui ui text view class
# -*- coding: utf-8 -*-

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

    def addParts(self, parts:AbsParts):
        parts.x = self.x + parts.x
        parts.y = self.y + parts.y
        self._partsList.append(parts)


    def dispatchTouchEvent(self, e):
        for p in reversed(list(self._partsList)):
            if p.visible == True:
                result = p.dispatchTouchEvent(e)
                if result == True:
                    break


    def getMatrix(self):
        m = Matrix(self.width, self.height)
        m.startX = self.x
        m.startY = self.y

        for p in self._partsList:
            if p.visible == True:
                m.merge(p.getMatrix())

        return m