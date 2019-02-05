# -*- coding: utf-8 -*-

# this is confirm dialog widget
# if you want display yes/no confirm dialog, please use this class

try:
    from text import Text
    from widget import Widget
    from input import MotionEvent, VALUE_DOWN, VALUE_MOVE, VALUE_UP
except ImportError:
    from . import Text, Widget, Image, MotionEvent, VALUE_DOWN, VALUE_MOVE, VALUE_UP


class DialogListener(object):

    def onPositive(self):
        pass

    def onNegative(self):
        pass


class Dialog(Widget):

    def __init__(self, name='dialog', message: str='', pos_text: str='yes', nega_text: str='no', listener: DialogListener=None):
        super().__init__(200, 32, name)

        confirm_message = Text(message)
        confirm_message.setSize(0, 0, 200, 32)
        self.addParts(confirm_message)
        self._message = confirm_message


        btnPositive = Text(pos_text)
        btnPositive.setSize(115, 24, 20, 8)
        self.addParts(btnPositive)
        self._btnPositive = btnPositive

        btnNegative = Text(nega_text)
        btnNegative.setSize(149, 24, 20, 8)
        self.addParts(btnNegative)
        self._btnNegative = btnNegative

        separator = Text('/')
        separator.setSize(138, 24, 8, 8)
        self.addParts(separator)

        self._dialogListener = listener

    def addEventListener(self, listener: DialogListener):
        self._dialogListener = listener

    def setMessage(self, message: str):
        self._message.setText(message)

    def setPositiveText(self, pos_text: str):
        self._btnPositive.setText(pos_text)

    def setNeagativeText(self, nega_text: str):
        self._btnNegative.setText(nega_text)

    def dispatchTouchEvent(self, e: MotionEvent):
        action = e.action
        if (action != VALUE_UP):
            return

        x = e.x
        y = e.y

        btnPositive = self._btnPositive
        btnNegative = self._btnNegative

        if btnPositive.hitTest(x, y):
            if self._dialogListener is not None:
                self._dialogListener.onPositive()

        elif btnNegative.hitTest(x, y):
            if self._dialogListener is not None:
                self._dialogListener.onNegative()


    