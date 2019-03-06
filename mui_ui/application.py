# -*- coding: utf-8 -*-

# mui application abstraction class

from abc import ABCMeta, abstractmethod

import time

try:
    from matrix import Matrix
    from parts import AbsParts
    from input import MotionEvent
except ImportError:
    from . import Matrix, AbsParts, MotionEvent


class AppEventListener():

    def requestUpdateDisplay(self, app, fade):
        raise NotImplementedError

    def setNextApp(self, app):
        raise NotImplementedError

    def onCloseApp(self, app):
        raise NotImplementedError

    def onChangeDuty(self, duty):
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

    def onTurnOffDisplay(self) -> bool:
        """
        return True / False
        True: allow turn off display
        """
        raise NotImplementedError

    def dispatchTouchEvent(self, e):
        views = self._views
        for v in reversed(list(views)):
            if v.visible is True:
                result = v.dispatchTouchEvent(e)
                if result is True:
                    return True

        return False

    def dispatchScrollEvent(self, start_event: MotionEvent, end_event: MotionEvent, scrollX, scrollY):
        pass

    def dispathFlingEvent(self,  start_event: MotionEvent, end_event: MotionEvent, veocityX, veocityY):
        pass

    def dispathLongPressEvent(self, event: MotionEvent):
        pass

    def close(self):
        self.stopTask()
        if self.appEventListener is not None:
            self.appEventListener.onCloseApp(self)

    def updateRequest(self, fade):
        if self.appEventListener is not None:
            self.appEventListener.requestUpdateDisplay(self, fade)

    def setNextApp(self, app):
        if self.appEventListener is not None:
            self.appEventListener.setNextApp(app)

    def changeDuty(self, duty):
        if self.appEventListener is not None:
            self.appEventListener.onChangeDuty(duty)

    def getUI(self)-> Matrix:
        # s = time.time()
        m = Matrix(200, 32)
        m.startX = 0
        m.startY = 0

        views = self._views

        for v in views:
            if v.visible is True:
                m.merge(v.getMatrix())

        # e = time.time()
        # print('!!!*** merge to UI ', (e - s))
        return m