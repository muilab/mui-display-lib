# -*- coding: utf-8 -*-

import time
from threading import Thread
from threading import Timer

try:
    from text import Text, Border, TextAlignment
except ImportError:
    from . import Text, Border, TextAlignment


class TypeWriterEventListener(object):
    """
    callback for TypeWirterText view events
    """

    def onTypeFinished(self):
        """
        callback to be invoked when finished text type effect.
        """
        pass

    def onScrollStart(self):
        """
        callback to be invoked when start scroll text.
        """
        pass

    def onScrollFinished(self):
        """
        callback to be invoked when finish scroll text.
        """
        pass


class TypeWriterText(Text):
    """
    TypeWriter Text


    this class inherit Text view and add effect like a TypeWriter for UI drawing.
    if text length is too long according to view size, when text is full on view area, start auto scroll and show left text.


    See Also
    --------
    Text
    TypeWriterEventListener
    """

    def __init__(self, text:str=None, border:Border=Border.NONE, name='typewriter textview'):
        super().__init__(text, border, name)
        self._srcText = text
        self._orgText = text
        self._typedTextCount = 0
        self._scrolling = False
        self._draw_out_area = False
        self._doTask = False
        self._task = None
        self._typewriterEventListener = None

    def addTypeWriterEvent(self, l: TypeWriterEventListener):
        self._typewriterEventListener = l

    def setText(self, text:str, textAlignment:TextAlignment=None):
        if self._task is not None and self._task.is_alive() is True:
            self._task.join()
            time.sleep(0.5)

        super().setText('', textAlignment)
        self._srcText = text
        self._orgText = text
        self._typedTextCount = 0

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
        if self._task is not None:
            self._task.join()


    def _doTypewriter(self):
        # print('---- start type writer ----', self._srcText)
        l = self.OnUpdateRequestListener
        if l is None:
            self._doTask = False
            return

        for s in self._srcText:
            tS = time.time()
            super().addText(s)
            self._typedTextCount += 1
            l.onUpdateView(self)

            if self._doTask is False:
                break

            tE = time.time()
            diff = tE - tS
            if diff < 0.15:
                time.sleep(0.15 - diff)

        self._doTask = False

        # if typed all text, notify all task finish        
        if (self._typedTextCount == len(self._orgText)) and self._typedTextCount > 0:
            if self._typewriterEventListener is not None:
                self._typewriterEventListener.onTypeFinished()


    def _onTextFull(self, text_index):
        """
        text_index is drawn text index when text is full in current view region
        """
        if self._scrolling is True:
            return

        self._doTask = False
        t = Timer(0.2, self._scroll, [text_index])
        t.start()        


    def _scroll(self, text_index):
        self._scrolling = True

        l = self.OnUpdateRequestListener
        if l is None:
            return

        # notify scroll start
        if self._typewriterEventListener is not None:
            self._typewriterEventListener.onScrollStart()

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

        # notify scroll finish
        if self._typewriterEventListener is not None:
            self._typewriterEventListener.onScrollFinished()

        # set new text
        #super().setText(newText)
        self._doTask = False
        super().setText('')
        self._srcText = newText
        l.onUpdateView(self)
        self.startTypewriter()
        #l.onUpdateView(self)

