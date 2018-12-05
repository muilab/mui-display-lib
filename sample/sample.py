# mui sample app
# -*- coding: utf-8 -*-

from ui import Display, MuiFont, Text, Widget, Border, TextAlignment

class SampleUI():

    def __init__(self):
        self.display = Display()

        self.ui = Widget(200, 32) # max size
        text1 = Text('こんにちは！')
        text1.setTextAlignment(TextAlignment.CENTER)
        text1.x = 0
        text1.y = 0
        text1.width = 200
        text1.height = 32
        self.ui.addParts(text1)

    def showUI(self):
        self.display.setLayout(self.ui.getMatrix())
        self.display.updateLayout()
        self.display.refreshDisplay(2, 100)



if __name__ == "__main__":
    print('OK')
    app = SampleUI()
    app.showUI()