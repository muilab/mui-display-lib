# -*- coding: utf-8 -*-

# mui application abstraction class

from abc import ABCMeta, abstractmethod

import time

try:
    from matrix import Matrix
    from parts import AbsParts
except ImportError:
    from . import Matrix
    from . import AbsParts


class AppEventListener():

    def requestUpdateDisplay(self, app, fade):
        raise NotImplementedError

    def setNextApp(self, app):
        raise NotImplementedError

    def onCloseApp(self, app):
        raise NotImplementedError


class AbsApp(metaclass=ABCMeta):
    
    def __init__(self, appEventListener: AppEventListener):
        self._views = []
        self._vDic = {}
        self.appEventListener = appEventListener

    def addView(self, v: AbsParts):
        self._views.append(v)

    def setView(self, v: AbsParts, name: str):
        self._vDic[name] = v

    def getView(self, name: str) -> AbsParts:
        return self._vDic.get(name) 

    @abstractmethod
    def startTask(self):
        raise NotImplementedError

    @abstractmethod
    def stopTask(self):
        raise NotImplementedError


    def dispatchTouchEvent(self, e):
        views = self._views
        for v in reversed(list(views)):
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
        s = time.time()
        m = Matrix(200, 32)
        m.startX = 0
        m.startY = 0
        e1 = time.time()

        views = self._views

        for v in views:
            if v.visible is True:
                m.merge(v.getMatrix(), True)

        e = time.time()
        print('!!!*** merge to UI ', (e - s))
        # print('???*** create UI ', (e1 - s))
        return m