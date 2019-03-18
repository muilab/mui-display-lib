# -*- coding: utf-8 -*-

import time
from threading import Thread
from threading import Timer

try:
    from text import Text, Border, TextAlignment
except ImportError:
    from . import Text, Border, TextAlignment

class AutoScrollText(Text):
    """
    AutoScroll Text


    this class inherit Text view.
    if text length is too long according to view size, when text is full on view area, start auto scroll and show left text.


    See Also
    --------
    Text
    TypeWriterEventListener
    """

    def __init__(self, text:str=None, border:Border=Border.NONE, name='auto scroll textview'):
        super().__init__(text, border, name)
        self._srcText = self._text
        self._scrolling = False
        self._draw_out_area = True

    def setText(self, text:str, textAlignment:TextAlignment=None):
        super().setText(text, textAlignment)
        self._srcText = self._text

    def addText(self, text: str):
        super().addText(text)
        self._srcText = self._text

    def _onTextFull(self, text_index):
        if self._scrolling is True:
            return

        t = Timer(2, self._scroll, [text_index])
        t.start()        


    def _scroll(self, text_index):
        self._scrolling = True
        l = self.OnUpdateRequestListener
        if l is None:
            return

        org_y = self.y
        for y in range(0, self.height, 2):
            self._y -= 2
            self._neddRenderContent = False
            l.onUpdateView(self)
            time.sleep(0.05)

        # next text
        newText = self._srcText[text_index+1:]
        # print(newText)

        self._scrolling = False
        self._y = org_y

        # set new text        
        self.setText(newText)
        l.onUpdateView(self)
