# -*- coding: utf-8 -*-

# this is confirm dialog widget
# if you want display yes/no confirm dialog, please use this class

try:
    from text import Text, Border
    from widget import Widget
    from input import MotionEvent, VALUE_DOWN, VALUE_MOVE, VALUE_UP
except ImportError:
    from . import Text, Border, Widget, Image, MotionEvent, VALUE_DOWN, VALUE_MOVE, VALUE_UP


class DialogListener(object):
    """
    Interface definition class for a callback to be invoked when touch dialog buttons.
    If you want to receive user selection, please override onPositive and onNegative method.
    
    """

    def onPositive(self):
        """
        callback to be invoked when user selected positive button.
        """
        pass

    def onNegative(self):
        """
        callback to be invoked when user selected negative button.
        """
        pass


class Dialog(Widget):
    """
    Simple confirmation dialog widget.

    Examples
    ---------
    from mui_ui import AbsApp, AppEventListener, Dialog, DialogListener

    class App(AbsApp, DialogListener, OnUpdateRequestListener):

        def __init__(self, appEventListener: AppEventListener):
            super().__init__(appEventListener)

            # create dialog(on application class)
            dialog = Dialog(
                message='dialog message', 
                pos_text='positive selection button text', 
                nega_text='negative selection button text', 
                listener=self)
            dialog.visible = False # first state of dialog
            self.addView(dialog)
            self.setView(dialog, 'dialog')
    
            # open dialog
            dialog.visible = True
            self.updateRequest(2) # with fede-in/out

        def onPositive(self):
            # user selected positive button

            # close dialog
            self.getView('dialog').visible = False
            self.updateRequest(2)


        def onNegative(self):
            # user selected negative button

            # close dialog
            self.getView('dialog').visible = False
            self.updateRequest(2)

    See Also
    --------
    DialogListener

    """

    def __init__(self, name='dialog', message: str='', pos_text: str='yes', nega_text: str='no', listener: DialogListener=None):
        """
        Parameters
        ------------
        message : str
            message text of confirmation
        pos_text : str
            positive button text (ex. yes
        nega_text : str
            neagative button text (ex. no
        listener : DialogListener
            callback
        """
        super().__init__(200, 32, name)

        confirm_message = Text(message)
        confirm_message.setSize(0, 0, 200, 32)
        self.addParts(confirm_message)
        self._message = confirm_message


        btnPositive = Text(pos_text, border= Border.BOTTOM)
        btnPositive.setSize(110, 23, 20, 9)
        self.addParts(btnPositive)
        self._btnPositive = btnPositive

        btnNegative = Text(nega_text, border= Border.BOTTOM)
        btnNegative.setSize(143, 23, 25, 9)
        self.addParts(btnNegative)
        self._btnNegative = btnNegative

        separator = Text('/')
        separator.setSize(133, 24, 8, 8)
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


    