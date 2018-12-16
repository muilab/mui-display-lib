# -*- coding: utf-8 -*-

# mui application abstraction class

from abc import ABCMeta, abstractmethod

try:
    from matrix import Matrix
    from parts import AbsParts
except ImportError:
    from . import Matrix
    from . import AbsParts


class AppEventListener():

    def requestUpdateDisplay(self, app, fade):
        raise NotImplementedError

    def onCloseApp(self, app):
        raise NotImplementedError


class AbsApp(metaclass=ABCMeta):
    
    def __init__(self, appEventListener: AppEventListener):
        self._views = []
        self.appEventListener = appEventListener

    @abstractmethod
    def startTask(self):
        raise NotImplementedError

    @abstractmethod
    def stopTask(self):
        raise NotImplementedError


    def dispatchTouchEvent(self, e):
        for v in reversed(list(self._views)):
            if v.visible == True:
                result = v.dispatchTouchEvent(e)
                if result == True:
                    break

    def dispatchScrollEvent(self, scrollX, scrollY):
        pass

    def dispathFlingEvent(self, veocityX, veocityY):
        pass

    def close(self):
        self.stopTask()
        if self.appEventListener != None:
            self.appEventListener.onCloseApp(self)


    def getUI(self)-> Matrix:
        m = Matrix(200, 32)
        m.startX = 0
        m.startY = 0

        for v in self._views:
            if v.visible == True:
                m.merge(v.getMatrix())

        return m