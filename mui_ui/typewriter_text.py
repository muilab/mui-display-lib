# -*- coding: utf-8 -*-

import time
from threading import Thread
from threading import Timer

try:
    from text import Text, Border, TextAlignment
except ImportError:
    from . import Text, Border, TextAlignment

class TypeWriterText(Text):

    def __init__(self, text:str=None, border:Border=Border.NONE, name='auto scroll textview'):
        super().__init__(text, border, name)
        self._srcText = text
        self._scrolling = False
        self._draw_out_area = False
        self._doTask = False
        self._task = None


    def setText(self, text:str, textAlignment:TextAlignment=None):
        if self._task is not None and self._task.is_alive() is True:
#            self.stopTypewriter()
            self._task.join()
            time.sleep(0.5)

        super().setText('', textAlignment)
        self._srcText = text

        t = Timer(0.1, self.startTypewriter)
        t.start()

    def startTypewriter(self):
        if self._doTask is True:
            return

        self._task = Thread(target= self._doTypewriter)
        self._doTask = True
        self._task.start()

    def stopTypewriter(self):
        self._doTask = False


    def _doTypewriter(self):
        print('---- start type writer ----', self._srcText)
        l = self.OnUpdateRequestListener

        for s in self._srcText:
            tS = time.time()
            super().addText(s)
            l.onUpdateView(self)

            if self._doTask is False:
                print('**** break!! ****')
                break

            tE = time.time()
            diff = tE - tS
            # print("--- time : {0} ---", diff)
            if diff < 0.15:
                time.sleep(0.15 - diff)

        self._doTask = False

    def _onTextFull(self, text_index):
        if self._scrolling is True:
            return

        print('----- on text full -----')
        self._doTask = False
        t = Timer(0.2, self._scroll, [text_index])
        t.start()        


    def _scroll(self, text_index):
        print('----- start scroll ----')
        self._scrolling = True
        l = self.OnUpdateRequestListener
        if l is None:
            print('---- listener is null ---')
            return

        org_y = self.y
        for y in range(0, self.height, 4):
            self._y -= 4
            self._neddRenderContent = False
            l.onUpdateView(self)
            time.sleep(0.15)

        # next text
        newText = self._srcText[text_index+1:]
        # print(newText)

        self._scrolling = False
        self._y = org_y

        # set new text
        #super().setText(newText)
        self._doTask = False
        super().setText('')
        self._srcText = newText
        l.onUpdateView(self)
        self.startTypewriter()
        #l.onUpdateView(self)

