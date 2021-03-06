# -*- coding: utf-8 -*-

# mui display state management class

from abc import ABCMeta, abstractmethod
from threading import Timer


class DisplayEventListener(metaclass=ABCMeta):

    @abstractmethod
    def onDismissTime(self) -> bool:
        """
        you have to implemet this method and return True if display can turn off.
        If return False, display manager start check timer again.
        """
        raise NotImplementedError()

    @abstractmethod
    def onDismiss(self):        
        raise NotImplementedError()


class DisplayManager(object):
    """
    DisplayManager class is manage display state(on/off) and notify time for turn off display.

    At default setting, you will recevie callback(DisplayEventListener.onDissmissTime()) 
    after 15 seconds from called startDismissTimer().

    If you return True to onDismissTime(), DisplayManager call DisplayEventListener.onDismiss(), so please instruct Display class to turn off.
    If you return False when onDismissTime(), this class restart timer and call callback after 15 seconds. 
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()

        return cls._instance

    def __init__(self, listener: DisplayEventListener, time_to_dismiss:float=15):
        """
        Parameters
        ------------
        listener : DisplayEventListener
            callback
        time_to_dismiss : float
            time to turn off display. default is 15 seconds.
        """
        if listener is None:
            raise ValueError("listener must be set")

        self.listener = listener
        self._time_to_dismiss = time_to_dismiss
        self._timer = None
        self._on = True

    def setEventListener(self, listener: DisplayEventListener):
        self.listener = listener
    

    def startDismissTimer(self):
        if self._timer is not None:
            self._timer.cancel()
            
        self._timer = Timer(self._time_to_dismiss, self._onDismissTime)
        self._timer.start()


    def _onDismissTime(self):
        if self.listener.onDismissTime() is False:
            self.startDismissTimer()

        else:
            self._on = False
            self.listener.onDismiss()
                  

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, on):
        self._on = on

    @property
    def time_to_dismiss(self):
        return self._time_to_dismiss

    @time_to_dismiss.setter
    def time_to_dismiss(self, t):
        self._time_to_dismiss = t