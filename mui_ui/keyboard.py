# -*- coding: utf-8 -*-

# this is key board widget
# if you want input words on mui like a simple IME, please use this class

try:
    from text import Text
    from widget import Widget
    from image import Image
    from input import MotionEvent, VALUE_DOWN, VALUE_MOVE, VALUE_UP
except ImportError:
    from . import Text, Widget, Image, MotionEvent, VALUE_DOWN, VALUE_MOVE, VALUE_UP

import os
dir = os.path.dirname(os.path.abspath(__file__))


class KeyboardListener(object):

    def onInput(self, char:str):
        pass

    def onDelete(self):
        pass

    def onForward(self):
        pass

    def onBack(self):
        pass

NUMERIC_LIST = ["1","2","3","4","5","6","7","8","9","0"," ",
            "!","@","#","$","%","^","&","*","(",")","'",
            "\"","=","_","`",":",";","?","~","|",".",",",
            "/","\\","+","-","[","]","{","}","<",">"
]

ALPHABET_LOWER = ["a","b","c","d","e","f","g","h","i","j",
            "k","l","m","n","o","p","q","r","s","t",
            "u","v","w","x","y","z"
]

ALPHABET_UPPER = ["A","B","C","D","E","F","G","H","I","J",
            "K","L","M","N","O","P","Q","R","S","T","" +
            "U","V","W","X","Y","Z"
]

MODE_NUMRIC = 0
MODE_ALPHABET = 1
MODE_ALPHABET_UPPER = 2

class Keyboard(Widget):

    def __init__(self, name='keyboard', listener: KeyboardListener=None):
        super().__init__(151, 19, name)

        btnMode = Text('123')
        btnMode.setSize(0, 11, 22, 8)
        self.addParts(btnMode)
        self._btnMode = btnMode
        

        btnUp = Text('↑')
        btnUp.setSize(26, 0, 8, 8)
        btnUp.visible = False
        self.addParts(btnUp)
        self._btnUp = btnUp

        btnDown = Text('↓')
        btnDown.setSize(26, 11, 8, 8)
        self.addParts(btnDown)
        self._btnDown = btnDown

        self._key_numeric_path = os.path.normpath(os.path.join(dir, './assets/keyboard_numeric.png'))
        self._key_alpha_lower_path = os.path.normpath(os.path.join(dir, './assets/keyboard_alpha_lower.png'))
        self._key_alpha_upper_path = os.path.normpath(os.path.join(dir, './assets/keyboard_alpha_upper.png'))
        keytop = Image(self._key_numeric_path)
        keytop.setSize(36, 0, 88, 20)
        self.addParts(keytop)
        self._keytop = keytop

        btnDel = Text('del')
        btnDel.setSize(128, 0, 18, 8)
        self.addParts(btnDel)
        self._btnDel = btnDel

        self.mode = MODE_NUMRIC
        self.current_top_line = 0
        self._keyboardListener = listener

    def addEventListener(self, listener: KeyboardListener):
        self._keyboardListener = listener


    def dispatchTouchEvent(self, e: MotionEvent):
        action = e.action
        if (action != VALUE_UP):
            return

        x = e.x
        y = e.y

        keytop = self._keytop
        btnMode = self._btnMode
        btnUp = self._btnUp
        btnDown = self._btnDown
        btnDel = self._btnDel

        if keytop.hitTest(x, y):
            selectedChar = None
            tX = x - keytop.x
            tY = y - self.y

            xIndex = tX // 8
            yIndex = tY // 10 + self.current_top_line

            targetIndex = (10 * yIndex) + xIndex

            if self.mode == MODE_NUMRIC:

                targetIndex = (11 * yIndex) + xIndex
                if targetIndex < len(NUMERIC_LIST):
                    selectedChar = NUMERIC_LIST[targetIndex]

            elif self.mode == MODE_ALPHABET:
                if targetIndex < len(ALPHABET_LOWER):
                    selectedChar = ALPHABET_LOWER[targetIndex]

            elif self.mode == MODE_ALPHABET_UPPER:
                if targetIndex < len(ALPHABET_UPPER):
                    selectedChar = ALPHABET_UPPER[targetIndex]

            if (self._keyboardListener is not None) and selectedChar is not None:
                self._keyboardListener.onInput(selectedChar)

        elif btnMode.hitTest(x, y):
            if self.mode == MODE_NUMRIC:
                self.mode = MODE_ALPHABET
                keytop.setImage(self._key_alpha_lower_path)
                btnMode.setText('abc')
            elif self.mode == MODE_ALPHABET:
                self.mode = MODE_ALPHABET_UPPER
                keytop.setImage(self._key_alpha_upper_path)
                btnMode.setText('ABC')
            elif self.mode == MODE_ALPHABET_UPPER:
                self.mode = MODE_NUMRIC
                keytop.setImage(self._key_numeric_path)
                btnMode.setText('123')

            self.current_top_line = 0
            keytop.offset_y = 0
            btnUp.visible = False
            btnDown.visible = True
            self.updateRequest()

        elif btnDown.hitTest(x, y):
            if self.mode == MODE_NUMRIC:
                keytop.offset_y = keytop.offset_y + 10
                if keytop.offset_y == 30:
                    btnDown.visible = False

            elif self.mode == MODE_ALPHABET or self.mode == MODE_ALPHABET_UPPER:
                keytop.offset_y = 10
                btnDown.visible = False

            self.current_top_line += 1
            btnUp.visible = True
            self.updateRequest()

        elif btnUp.hitTest(x, y):
            if self.mode == MODE_NUMRIC:
                keytop.offset_y = keytop.offset_y - 10
                if keytop.offset_y == 0:
                    btnUp.visible = False

            elif self.mode == MODE_ALPHABET or self.mode == MODE_ALPHABET_UPPER:
                keytop.offset_y = 0
                btnUp.visible = False

            self.current_top_line -= 1
            btnDown.visible = True
            self.updateRequest()

        elif btnDel.hitTest(x, y):
            if (self._keyboardListener is not None):
                self._keyboardListener.onDelete()



