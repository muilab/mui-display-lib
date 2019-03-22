# -*- coding: utf-8 -*-

# this is digital clock widget
# please use as a part of your applicaion

import time
from datetime import datetime, timezone
from threading import Thread

try:
    from parts import AbsParts
    from matrix import Matrix
    from muifont import MuiFont
    from widget import Widget
    from text import Text
except ImportError:
    from . import Matrix, MuiFont, Text, Widget



class DigitalClock(Widget):
    """
    Digital Clock Widget
    please use as a part of your application.

    Examples
    ---------
    
    # create clock
    clock = DigitalClock(timezone=timezone) # please set YOUR Timezone
    clock.setPos(10, 0) # x=10, y=0
    clock.addOnUpdateViewListener(listener)

    # start tick
    clock.startTick()

    # stop tick
    # note : when application that set-up clock is invisible or display turn off, please call this API.
    #        because ticker thread require update UI from background every seconds, 
    #        so unnecessary update event occurs and may make bad effect to update performance.
    clock.stopTick()
    """

    def __init__(self, name='digital clock', timezone:timezone=None):
        """
        Parameters
        ------------
        name : str
        timezone : timezone         
        """
        super().__init__(30, 10, name)

        hour = Text('00')
        hour.width = 12
        hour.height = 10
        self.addParts(hour)
        
        coron = Text(':')
        coron.width = 3
        coron.height = 10
        coron.x = 13        
        self.addParts(coron)

        minute = Text('00')
        minute.width = 12
        minute.height = 10
        minute.x = 17
        self.addParts(minute)

        self._views = {}
        self._views["h"] = hour
        self._views["m"] = minute
        self._views[":"] = coron

        self._doTask = False
        self._timezone = timezone

    def startTick(self):
        """
        start clock update
        """
        task = Thread(target= self.updateClock)
        self._doTask = True
        task.start()

    def setPos(self, x, y):
        """
        set view position

        Parameters
        ----------
        x : int
            x position
        y : int
            y position
        """
        self.setSize(x, y, self.width, self.height)

    def stopTick(self):
        """
        stop clock update
        """
        self._doTask = False

    def updateClock(self):        
        while self._doTask:
            sT = time.time()
            if self._timezone is None:
                now = datetime.now()
            else:
                now = datetime.now(self._timezone)

            self._views["h"].setText(now.strftime('%H'))
            self._views["m"].setText(now.strftime('%M'))

            sec = now.second
            self._views[":"].visible = sec % 2 == 0

            self._isChange = True

            if self.OnUpdateRequestListener is not None:
                self.OnUpdateRequestListener.onUpdateView(self)

            eT = time.time()
            next = 1 - (eT - sT)
            if next > 0:
                time.sleep(next)
            

            

