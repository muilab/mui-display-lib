Usage
===========

please see also sample.py!


control mui's display
-----------------------

you can control mui's display via Display class.
::
    from mui_ui import Display, Matrix

    display = Display()
    # set brightness level (1 -100)
    display.setDuty(100)
    # clear 
    display.clearDisplay()
    # turn on
    display.turnOn(0)

    # create data for display(display size is x : 200, y : 32)
    m = Matrix(200, 32)
    # set dot on top-left side
    m.matrix[0][0] = 1 # [y][x], 1 mean LED On

    # set matrix data and update display
    # note : please pass always max size Matrix of display to Display class.
    display.setLayout(m)
    display.updateLayout()
    display.refreshDisplay()


you can also some View class for drawing
::
    from mui_ui import Display, Widget, Text

    # create UI
    ui = Widget(200, 32)

    # create Text View and set text
    text = Text('Hello world)
    # set text position and drawing area size(x : 0, y : 0, width : 100, height : 8)
    text.setSize(0, 0, 100, 8)

    # add Text View to UI
    ui.addParts(text)

    display.setLayout(ui.getMatrix())
    display.updateLayout()
    display.refreshDisplay()


    # create Image View and set file path
    image = Image('full path to image file')
    # set image position(x : 100, y : 0)
    image.setPos(100, 0)

    # add Image View to UI
    ui.addParts(image)

    display.setLayout(ui.getMatrix())
    display.updateLayout()
    display.refreshDisplay()



receive touch event from mui
-------------------------------

you can receive touch event from mui via InputHandler class
::
    from mui_ui import InputHandler, InputEventListener

    # create input event callback class
    class MyInputEventListener(InputEventListener):
    
        def onInputEvent(self, e):
            # you can receive touch event at this method
            print(e) # print event


    # connect to touch panel and set callback    
    input = InputHandler(MyInputEventListener())
    # start watch touch panel event
    input.startEventLoop()


you can get log like below when touch on mui, after call ``input.startEventLoop``
::
    --- MotionEvent at 1553255200.172396, action 1, x 116, y 17 ---
    --- MotionEvent at 1553255200.256987, action 0, x 116, y 17 ---
    --- MotionEvent at 1553255200.825415, action 1, x 121, y 15 ---
    --- MotionEvent at 1553255200.910052, action 0, x 121, y 15 ---
    --- MotionEvent at 1553255201.056689, action 1, x 121, y 14 ---
    --- MotionEvent at 1553255201.141281, action 0, x 121, y 14 ---

action 1 is down event, action 0 is up and action 2 is move event.


gesture detector
^^^^^^^^^^^^^^^^^

you can also determin simple gestures
::
    from mui_ui import InputHandler, InputEventListener, GestureDetector, GestureListener

    class MyGestureListener(GestureListener):

        def OnFling(self, e1, e2, x, y):
            print('swipe event occured!')

        def onLongPress(self, e):
            # keep press 
            print('long press event occured!')

    gesture_detector = GestureDetector(MyGestureListener())

    # create input event callback class
    class MyInputEventListener(InputEventListener):
    
        def onInputEvent(self, e):
            # you can receive touch event at this method
            print(e) # print event

            # pass to gesture detector
            gesture_detector.onTouchEvent(e, longpress_timeout=1)


    # connect to touch panel and set callback    
    input = InputHandler(MyInputEventListener())
    # start watch touch panel event
    input.startEventLoop()

    


create application
---------------------

single UI appliation
::
    from mui_ui import Display, Text, Widget, AbsApp
    from mui_ui import MotionEvent, InputEventListener, InputHandler, OnTouchEventListener, AppEventListener, OnUpdateRequestListener  
    from mui_ui import GestureListener, GestureDetector

    from threading import Lock
    mutex = Lock()

    class SimpleApplication(AbsApp, InputEventListener, OnTouchEventListener, GestureListener):

        def __init__(self, parameter_list):
            super().__init__(None)

            # connect to mui display
            self.display = Display()

            # you can choice LED brightness(1 - 100)
            self.display.setDuty(100)

            # connect to mui touchpanel(and set InputEventListener)
            self.input = InputHandler(self)

            # create gesture detector for swipe and long press event(and set GestureListener)
            self._gestureDetector = GestureDetector(self)

            # create UI
            text = Text('Hello world')
            text.setSize(0, 0, 100, 32) # set position and size (x, y, width, height)
            self.addView(text) # add view to this application
            self.setView(text, 'text') # set view with reference key. when you'd like to access this view, you can get this view via self.getView('key')
            self.addOnTouchViewListener(self) # set callback method(onTouch()) to catch touch event. 


        def mainLoop(self):
            # start touch event loop
            self.input.startEventLoop()

        def startTask(self):
            pass

        def stopTask(self):
            pass

        def updateUI(self, fade=0):
            """
            update UI.
            """
            with mutex:
                if fade > 0:
                    # fade out(0 - 4 : 0 is do not fade, 4 is very slow)
                    self.display.turnOff(fade)

                # set layout data
                self.display.setLayout(self.getUI())
                # update Display internal data buffer (do not refesh display until call refreshDisplay())
                self.display.updateLayout()
                # refresh Display
                self.display.refreshDisplay()

                if fade > 0:
                    # fade in(0 - 4)
                    self.display.turnOn(fade)

        def onInputEvent(self, e: MotionEvent):
            # dispatch touch event to all views
            self.dispatchTouchEvent(e)

            # determin gesture
            self._gestureDetector.onTouchEvent(e)

        def onTouch(self, view, e: MotionEvent):
            # handling touch events
            pass

        def onFling(self, e1: MotionEvent,  e2: MotionEvent, x, y):
            # handling swipe event
            print('*** swipe ***')


    # create application instance
    app = SimpleApplication()

    # draw UI
    app.updateUI()

    # start capture touch panel event
    app.mainLoop()

