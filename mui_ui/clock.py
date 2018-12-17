# -*- coding: utf-8 -*-

# this is digital clock widget
# please use as a part of your applicaion

import time
from datetime import datetime
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

    def __init__(self, name='digital clock'):
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

    def startTick(self):
        task = Thread(target= self.updateClock)
        self._doTask = True
        task.start()

    def setSize(self, x, y, w, h):
        super().setSize(x, y, w, h)

        if hasattr(self, '_views'):
            hour = self._views.get('h')
            if hour is not None:   
                print(hour.x, hour.y)


    def stopTick(self):
        self._doTask = False


    def updateClock(self):        
        while self._doTask:
            sT = time.time()
            now = datetime.now()
            self._views["h"].setText(now.strftime('%H'))
            self._views["m"].setText(now.strftime('%M'))

            sec = now.second
            self._views[":"].visible = sec % 2 == 0

            if self.OnUpdateRequestListener != None:
                self.OnUpdateRequestListener.onUpdateView(self)

            eT = time.time()
            next = 1 - (eT - sT)
            if next > 0:
                time.sleep(next)
            

            

