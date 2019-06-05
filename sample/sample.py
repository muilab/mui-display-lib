# -*- coding: utf-8 -*-

# mui sample app


import sys
import asyncio
import time

from datetime import timezone, timedelta

from threading import Lock
mutex = Lock()

from mui_ui import Display, MuiFont, Text, Image, Widget, Border, AbsApp, Message, DigitalClock
from mui_ui import TextAlignment, MotionEvent, InputEventListener, InputHandler, OnTouchEventListener, AppEventListener, OnUpdateRequestListener  
from mui_ui import GestureListener, GestureDetector
from mui_ui import Keyboard, KeyboardListener
from mui_ui import DisplayManager, DisplayEventListener

from app_wifisetting import WiFiSetting

import os
dir = os.path.dirname(os.path.abspath(__file__))

class DummyWeatherApp(AbsApp):

    def __init__(self, appEventListener: AppEventListener, lang='ja-JP'):
        super().__init__(appEventListener)

        self._lang = lang

        # create weather forecast UI
        def createWeatherForecastUI():
            widget = Widget(189, 32)
            widget.visible = False
            self.addView(widget)
            self.setView(widget, 'forecast_view')

            dateText = Text()
            dateText.setSize(9, 3, 80, 8)
            widget.addParts(dateText)
            self.setView(dateText, 'dateText')

            wIcon = Image()
            wIcon.setSize(15, 18, 26, 14)
            widget.addParts(wIcon)
            self.setView(wIcon, 'wIcon')

            highTemp = Text()
            highTemp.setSize(85, 3, 35, 8)
            widget.addParts(highTemp)
            self.setView(highTemp, 'hTemp')

            tempIconName = './assets/weather/icon_f.png' if self._lang == 'en-US' else './assets/weather/icon_c.png'
            tempIconPath = os.path.normpath(os.path.join(dir, tempIconName))

            hTempIcon = Image(tempIconPath)
            hTempIcon.setSize(98, 3, 9, 7)
            widget.addParts(hTempIcon)
            self.setView(hTempIcon, 'hTempIcon')

            lowTemp = Text()
            lowTemp.setSize(85, 21, 35, 8)
            widget.addParts(lowTemp)
            self.setView(lowTemp, 'lTemp')

            lTempIcon = Image(tempIconPath)
            lTempIcon.setSize(98, 21, 9, 7)
            widget.addParts(lTempIcon)
            self.setView(lTempIcon, 'lTempIcon')

            pIcon = Image()
            pIcon.setSize(134, 3, 9, 10)
            widget.addParts(pIcon)
            self.setView(pIcon, 'pIcon')

            pText = Text()
            pText.setSize(148, 3, 32, 8)
            widget.addParts(pText)
            self.setView(pText, 'pText')

            percentIconName = './assets/weather/icon_percent.png'
            percentIconPath = os.path.normpath(os.path.join(dir, percentIconName))

            percentIcon = Image(percentIconPath)
            percentIcon.setSize(160, 3, 3, 7)
            widget.addParts(percentIcon)
            self.setView(percentIcon, 'percentIcon')

            widget.visible = False

        # common area
        def createCommonMenu():
            # add home icon
            iconHome = Image(os.path.normpath(os.path.join(dir, './assets/icon_home.png')))
            iconHome.setSize(190, 0, iconHome.width, iconHome.height)
            iconHome.addOnTouchViewListener(self)
            self.addView(iconHome)
            self.setView(iconHome, 'home')
            
            # add current icon(this icon has no action)
            iconWeather = Image(os.path.normpath(os.path.join(dir, './assets/icon_weather.png')))
            iconWeather.setSize(191, 23, iconWeather.width, iconWeather.height)
            self.addView(iconWeather)

        createWeatherForecastUI()
        createCommonMenu()

        self._next = None
        self._prev = None

    def setRelativeApps(self, next: AbsApp, prev: AbsApp):
        self._next = next
        self._prev = prev

    def _setupDummyData(self):
        """
        set dummy data
        """
        self.getView('dateText').setText('21 July Sun.')
        self.getView('wIcon').setImage(os.path.normpath(os.path.join(dir, './assets/weather/icon_weather_101.png')))
        self.getView('hTemp').setText('28')
        self.getView('lTemp').setText('12')
        self.getView('pIcon').setImage(os.path.normpath(os.path.join(dir, './assets/weather/icon_precip_10.png')))
        self.getView('pText').setText('10')

        self.getView('forecast_view').visible = True
        self.updateRequest(2)

    # ------------------------
    # override AbsApp methods

    def startTask(self):
        self._setupDummyData()

    def stopTask(self):
        self.getView('forecast_view').visible = False

    def dispatchFlingEvent(self, e1, e2, x, y):
        if e1.x > e2.x:
            # next
            self.setNextApp(self._next)

        elif e1.x < e2.x:
            # prev
            self.setNextApp(self._prev)

        return True

    def dispathLongPressEvent(self, e):
        pass    

    def onTurnOffDisplay(self):
        # always allow turn off
        return True

    # ------------------------
    # OnUpdateRequestListener implementation

    def onUpdateView(self, view):
        self.updateRequest(0)

    # ------------------------
    # OnTouchEventListener implementation

    def onTouch(self, view, e):
        iconHome = self.getView('home')

        if view == iconHome:
            # close this application
            self.close()



class DummyThermoApp(AbsApp):

    def __init__(self, appEventListener: AppEventListener, lang='ja-JP'):
        super().__init__(appEventListener)

        dummy = Text('dummy thermostat UI')
        dummy.setSize(0, 11, 189, 8)
        self.addView(dummy)        

        # common area
        def createCommonMenu():
            # add home icon
            iconHome = Image(os.path.normpath(os.path.join(dir, './assets/icon_home.png')))
            iconHome.setSize(190, 0, iconHome.width, iconHome.height)
            iconHome.addOnTouchViewListener(self)
            self.addView(iconHome)
            self.setView(iconHome, 'home')
            
            # add current icon(this icon has no action)
            iconWeather = Image(os.path.normpath(os.path.join(dir, './assets/icon_thermo.png')))
            iconWeather.setSize(191, 23, iconWeather.width, iconWeather.height)
            self.addView(iconWeather)


        createCommonMenu()

        self._next = None
        self._prev = None

    def setRelativeApps(self, next: AbsApp, prev: AbsApp):
        self._next = next
        self._prev = prev
    
    # ------------------------
    # override AbsApp methods

    def startTask(self):
        pass

    def stopTask(self):
        pass

    def dispatchFlingEvent(self, e1, e2, x, y):
        if e1.x > e2.x:
            # next
            self.setNextApp(self._next)

        elif e1.x < e2.x:
            # prev
            self.setNextApp(self._prev)

        return True

    def dispathLongPressEvent(self, e):
        pass    

    def onTurnOffDisplay(self):
        # always allow turn off
        return True

    # ------------------------
    # OnUpdateRequestListener implementation

    def onUpdateView(self, view):
        self.updateRequest(0)

    # ------------------------
    # OnTouchEventListener implementation

    def onTouch(self, view, e):
        iconHome = self.getView('home')

        if view == iconHome:
            # close this application
            self.close()



class HomeApp(AbsApp, OnUpdateRequestListener, OnTouchEventListener):

    def __init__(self, appEventListener: AppEventListener):
        super().__init__(appEventListener)

        # create home UI

        # add clock
        def addClock():
            tz = timezone(timedelta(hours=9)) # this timezone is JST(+9:00). please change to your timezone
            clock = DigitalClock(timezone=tz)
            clock.setPos(173, 0)
            clock.addOnUpdateViewListener(self)
            self.addView(clock)
            self.setView(clock, 'clock')

        # add menu
        def createMenu():
            # create weahter app icon
            iconWeather = Image(os.path.normpath(os.path.join(dir, './assets/icon_weather.png')))
            iconWeather.addOnTouchViewListener(self)
            self.setView(iconWeather, 'icon_weather')

            # create thermostat app icon
            iconThermo = Image(os.path.normpath(os.path.join(dir, './assets/icon_thermo.png')))
            iconThermo.addOnTouchViewListener(self)
            self.setView(iconThermo, 'icon_thermo')

            # create wi-fi setting app icon
            iconWiFi = Image(os.path.normpath(os.path.join(dir, './assets/icon_wifi_enable.png')))
            iconWiFi.addOnTouchViewListener(self)
            self.setView(iconWiFi, 'icon_wifi')

            # create menu widget
            menu = Widget(
                (iconWeather.width + iconThermo.width + 2),
                22)
            menu.setPos(0, 11)
            self.addView(menu)

            # add icons to menu widget
            menu.addParts(iconWeather)

            iconThermo.x = iconWeather.width + 2
            menu.addParts(iconThermo)

            iconWiFi.x = iconWeather.width + 2
            iconWiFi.y = 11
            menu.addParts(iconWiFi)

        # create application
        def createApplication():
            weatherApp = DummyWeatherApp(self.appEventListener)
            thermoApp = DummyThermoApp(self.appEventListener)
            wifiApp = WiFiSetting(self.appEventListener, lang='ja-JP') # if you want to change English, please change to 'en-US'

            weatherApp.setRelativeApps(next=thermoApp, prev=thermoApp)
            thermoApp.setRelativeApps(next=weatherApp, prev=weatherApp)

            self._apps = {}
            self._apps['weather'] = weatherApp
            self._apps['thermo'] = thermoApp
            self._apps['wifi'] = wifiApp


        def addHomeIcon():
            iconHome = Image(os.path.normpath(os.path.join(dir, './assets/icon_home.png')))
            iconHome.setSize(190, 23, iconHome.width, iconHome.height)
            self.addView(iconHome)

        addClock()
        createMenu()
        createApplication()
        addHomeIcon()

    # ------------------------
    # override AbsApp methods

    def startTask(self):
        # start clock update
        self.getView('clock').startTick()

    def stopTask(self):
        # stop clock update
        self.getView('clock').stopTick()

    def dispatchFlingEvent(self, e1, e2, x, y):
        return False

    def dispathLongPressEvent(self, e):
        pass    

    def onTurnOffDisplay(self):
        # always allow turn off
        return True

    # ------------------------
    # OnUpdateRequestListener implementation

    def onUpdateView(self, view):
        self.updateRequest(0)

    # ------------------------
    # OnTouchEventListener implementation

    def onTouch(self, view, e):
        iconWeather = self.getView('icon_weather')
        iconThermo = self.getView('icon_thermo')
        iconWiFi = self.getView('icon_wifi')

        if view == iconWeather:
            next = self._apps['weather']

        elif view == iconThermo:
            next = self._apps['thermo']

        elif view == iconWiFi:
            next = self._apps['wifi']

        if next is not None:
            self.setNextApp(next)



class MuiMain(InputEventListener, GestureListener, AppEventListener, DisplayEventListener):
    """
    Main class
    this class connect to mui's hardware(display and touch panel) and control applications transition.
    """

    def __init__(self):
        # connect to mui touchpanel
        self.input = InputHandler(self)

        # create gesture detector(for swipe)
        self.gesture_detector = GestureDetector(listener=self, longpress_timeout=2)

        # connect to mui display
        self.display = Display()
        # set birghtness level
        self.display.setDuty(100) 
        # clear and turn on display
        self.display.clearDisplay()
        self.display.turnOn(0)

        # create display manager(for auto turn off display)
        # after 15 seconds from last user touch to mui, turn off display.
        self.display_manager = DisplayManager(self, time_to_dismiss=15) 

        # create base application and set it to current application
        self.app = self._baseApp = HomeApp(appEventListener = self)

    def main_loop(self):
        # start display manager check
        self.display_manager.startDismissTimer()
        # start capture touch event
        self.input.startEventLoop()

    def startTask(self):
        self.app.startTask()

    def updateUI(self, fade=0, turn_on=False, turn_off=False):
        with mutex:
            if (fade > 0) and (turn_on is False):
                # fade out (1 - 4 : 4 is very slow)
                self.display.turnOff(fade)

            if (turn_on is False) and (turn_off is False):
                # set layout data
                self.display.setLayout(self.app.getUI())
                # update Display internal data buffer (do not refesh display until call refreshDisplay())
                self.display.updateLayout()
                # refresh Display
                self.display.refreshDisplay()

            if (fade > 0) and (turn_off is False):
                # fade in           
                self.display.turnOn(fade)

    # ------------------------
    # InputEventListener implementation

    def onInputEvent(self, e: MotionEvent):
        if self.display_manager.on is False:
            if e.action == 0:
                self.display_manager.on = True
                self.updateUI(fade=2, turn_on=True)
                self.display_manager.startDismissTimer()
            return

        # pass to gesture detector
        handle = self.gesture_detector.onTouchEvent(e)

        # dispath touch event to current application
        if handle is False:
            self.app.dispatchTouchEvent(e)

        # reset display turn off timer
        self.display_manager.startDismissTimer()


    # ------------------------
    # AppEventListener implementation

    def requestUpdateDisplay(self, app, fade):
        self.updateUI(fade)

    def setNextApp(self, app):
        self.display_manager.startDismissTimer()

        # stop old application task
        self.app.stopTask()

        # change current application
        self.app = app
        # update UI
        self.updateUI(2)
        # start new application task
        self.app.startTask()


    def onCloseApp(self, app):
        self.display_manager.startDismissTimer()

        # close current application, so return to base application
        self.app = self._baseApp
        self.updateUI(2)
        self.app.startTask()

    def onChangeDuty(self, duty):
        # request brightness change to display class
        self.display.setDuty(duty)

    # ------------------------
    # DisplayEventListener implementation

    def onDismissTime(self) -> bool:
        # check app allow turn off
        return self.app.onTurnOffDisplay()

    def onDismiss(self):
        # turn off display with fade effect
        self.updateUI(fade=3, turn_off=True)


    # ------------------------
    # GestureListener implementation

    def onFling(self, e1: MotionEvent, e2: MotionEvent, x, y):
        # swipe event occured, pass to current application
        return self.app.dispatchFlingEvent(e1, e2, x, y)

    def onLongPress(self, e: MotionEvent):
        # long press event occured, pass to current application
        self.app.dispathLongPressEvent(e)




if __name__ == "__main__":
    try:
        app = MuiMain()

        # draw UI
        app.updateUI(fade=3)

        # kick appliction task
        app.startTask()

        # start capture touch panel event
        app.main_loop()

    except (KeyboardInterrupt, EOFError):
        pass

    sys.exit(0)

