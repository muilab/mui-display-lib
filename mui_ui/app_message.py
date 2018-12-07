# -*- coding: utf-8 -*-

# mui message applicaion class

import time
from threading import Thread

try:
    from application import AbsApp, AppEventListener
    from parts import AbsParts, OnTouchEventListener
    from text import Text
except ImportError:
    from . import AbsApp, AppEventListener, AbsParts, Text, OnTouchEventListener



class Message(AbsApp, OnTouchEventListener):

    def __init__(self, appEventListener: AppEventListener):
        super().__init__(appEventListener)
        self._doTask = False

        # create text view
        textView = Text(name = 'message view')
        textView.width = 200
        textView.height = 32
        textView.addOnTouchViewListener(self)
        self._views.append(textView)
        self._textView = textView
        self._msg = ''
        self._task = None

    def setMessage(self, msg: str):
        if self._task != None:
            return

        self._msg = msg
        self._task = Thread(target= self.showMessage)
        self._doTask = True
        self._task.start()
        

    def showMessage(self):
        for s in self._msg:
            print("--- call task ---")
            tS = time.time()
            self._textView.addText(s)
            self.appEventListener.requestUpdateDisplay(self, 0)
            tE = time.time()
            diff = tE - tS
            print("--- time : {0} ---", diff)
            if diff < 0.25:
                time.sleep(0.25 - (tE - tS))

            if self._doTask == False:
                break

        time.sleep(10)
        self.close()


    def onTouch(self, view, e):
        print('-- touched message --')
        self.stopTask()
        self.close()


    def startTask(self):
        pass

    def stopTask(self):
        self._doTask = False


