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


class AppEventListener(object):
    """
    callback for application events.

    please set to application class that inherit AbsApp and implements callback methods for handling application events.
    """

    def requestUpdateDisplay(self, app, fade):
        """
        update UI request from application

        Parameters
        ----------
        app : AbsApp
            application what request update UI
        fade : int
            fade in/out level (0 - 4 : 0 is do not fade in/out)
        """
        raise NotImplementedError

    def setNextApp(self, app):
        """
        change application request

        Parameters
        -----------
        app : AbsApp
            next application
        """
        raise NotImplementedError

    def onCloseApp(self, app):
        """
        close application request

        Parameters
        ----------
        app : AbsApp
            close target application
        """
        raise NotImplementedError

    def onChangeDuty(self, duty):
        """
        change UI brightness request

        Parameters
        ----------
        duty : int
            brightness level (1 - 100)
        """
        raise NotImplementedError


class AbsApp(metaclass=ABCMeta):
    """
    AbsApp is convinience abstract class for you create custom Applications.

    Examples
    --------
    please see sample.py

    See Also
    --------
    AppEventListener
    """
    
    def __init__(self, appEventListener: AppEventListener):
        self._views = []
        self._vDic = {}
        self.appEventListener = appEventListener

    def addView(self, v: AbsParts):
        """
        add view to this application.
        application get Matrix from all views when called getUI(). 
        
        Notes
        ------
        all views stacked, so UI drawing is take from bottom to top, but touch event is handling top to bottom.

        """
        self._views.append(v)

    def setView(self, v: AbsParts, name: str):
        """
        this method is convinience for view reference. when access to any view on this application, please get from getView().

        Parameters
        ----------
        v : AbsParts
            target view
        name : str
            id of target view

        See Also
        --------
        getView
        """
        self._vDic[name] = v

    def getView(self, name: str) -> AbsParts:
        """
        this method is convinience for view reference. you can get view by name which set via setView().

        Parameters
        ----------
        name : str
            id of target view
        
        Returns
        -------
        AbsParts
             target view
        """
        return self._vDic.get(name) 

    @abstractmethod
    def startTask(self):
        """
        if application has a task to start when application become front of UI(such as API call for get weather information), 
        please start here that tasks.
        """
        raise NotImplementedError

    @abstractmethod
    def stopTask(self):
        """
        if application has a task what running background, 
        please stop all tasks here. 
        """
        raise NotImplementedError

    def onTurnOffDisplay(self) -> bool:
        """
        this method to be invoked by DisplayManager before DisplayManager call onDissmiss().
        please return True or False which you want to turn off display or not.

        Returns
        --------
        True : bool
            allow turn off display
        False : bool
            don't allow turn off, when application is running some operation and you do not like turn off
        """
        raise NotImplementedError

    def dispatchTouchEvent(self, e: MotionEvent) -> bool:
        """
        dispath touch event to views on this application.
        when any view handle touch event, no longer dispath touch event to bottom views.

        Parameters
        ----------
        e : MotionEvent

        Returns
        -------
        bool
            True means any view handled touch event.
        """
        views = self._views
        for v in reversed(list(views)):
            if v.visible is True:
                result = v.dispatchTouchEvent(e)
                if result is True:
                    return True

        return False

    def dispatchScrollEvent(self, start_event: MotionEvent, end_event: MotionEvent, scrollX, scrollY):
        """
        dispath scroll event
        """
        pass

    def dispathFlingEvent(self,  start_event: MotionEvent, end_event: MotionEvent, velocityX, velocityY):
        """
        dispath swipe event.
        if you want to take any action when swipe event occured, please override this method and implements action.

        Parameters
        ----------
        start_event : MotionEvent
            touch event information which start fling action
        end_event : MotionEvent
            touch event information which end fling action
        velocityX : int
            velocity of x direction
        velocityY : int
            velocity of y direction

        See Also
        --------
        GestureDetector
        """
        pass

    def dispathLongPressEvent(self, event: MotionEvent):
        """
        dispath long press event.
        if you want to take any action when long press event occured, please override this method and implements action.

        Parameters
        ----------
        event : MotionEvent
            touch event information.

        See Also
        --------
        GestureDetector
        """
        pass

    def close(self):
        """
        close this application
        """
        self.stopTask()
        if self.appEventListener is not None:
            self.appEventListener.onCloseApp(self)

    def updateRequest(self, fade):
        """
        update UI request

        Parameters
        ----------
        fade : int
            fade in/out effect for update
        """
        if self.appEventListener is not None:
            self.appEventListener.requestUpdateDisplay(self, fade)

    def setNextApp(self, app):
        """
        change to next application

        Parameters
        ----------
        app : AbsApp
            next application
        """
        if self.appEventListener is not None:
            self.appEventListener.setNextApp(app)

    def changeDuty(self, duty):
        """
        change display brightness level

        Parameters
        ----------
        duty : int
            brightness level(1 - 100)
        """
        if self.appEventListener is not None:
            self.appEventListener.onChangeDuty(duty)

    def getUI(self)-> Matrix:
        """
        get UI layout matrix data

        Returns
        -------
        Matrix : layout matrix data
        """
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