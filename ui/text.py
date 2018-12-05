# mui ui text view class
# -*- coding: utf-8 -*-

from enum import Enum

try:
    from parts import AbsParts
    from matrix import Matrix
    from muifont import MuiFont
except ImportError:
    from . import AbsParts
    from . import Matrix
    from . import MuiFont

LINE_OFFSET = (8+3)

class Border(Enum):
    NONE = 0
    BOTTOM = 1
    AROUND = 2

class TextAlignment(Enum):
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class Text(AbsParts):

    def __init__(self, text:str=None, border:Border=Border.NONE, name='textview'):
        super().__init__(name)
        self._text = text
        self._border = border


    def setText(self, text:str, textAlignment:TextAlignment=TextAlignment.LEFT):
        self._text = text
        self._textAlignment = textAlignment


    def setTextAlignment(self, textAlignment:TextAlignment):
        self._textAlignment = textAlignment


    def setBorder(self, border:Border):
        self._border = border


    def getMatrix(self):
        """
        Return Matrix data for display draw
        """
        m = Matrix(self.width, self.height)
        m.startX = self.x
        m.startY = self.y

        if self._text != None:
            font = MuiFont.get_instance()

            maxX = 0
            xOffset = yOffset = 2 if self._border == Border.AROUND else 0

            if self._textAlignment == TextAlignment.CENTER:
                tW = self.getTextWidth(font, self._text)
                dX = self.width - tW
                xOffset = dX // 2
                xOffset += 1 if self._border == Border.AROUND else 0

                tH = self.getTextHeight(font, self._text)
                dY = self.height - tH
                yOffset = dY // 2
            elif self._textAlignment == TextAlignment.RIGHT: 
                tW = self.getTextWidth(font, self._text)
                dX = self.width - tW
                dx -= 1 if self._border == Bordor.AROUND else 0
                xOffset = dx

            xOffsetOrg = xOffset
            isOverArea = False

            # draw text
            for s in self._text:                
                if s == '\n':
                    yOffset += LINE_OFFSET
                    xOffset = xOffsetOrg

                    if ((yOffset + 8) > (self.y + self.height)):
                        isOverArea = True
                else:
                    textM = font.getText(s)
                    textM.startX = self.x + xOffset
                    textM.startY = self.y + yOffset

                    if ((textM.startX + textM.width) > (self.x + self.width)):
                        xOffset = 0
                        yOffset += LINE_OFFSET

                        textM.startX = self.x + xOffset
                        textM.startY = self.y + yOffset

                    # merge char matrix data to area matrix
                    m.merge(textM)

                    xOffset += textM.width
                    if maxX < xOffset:
                        maxX = xOffset

                # check text is out from this view area
                if (isOverArea or (((xOffset + 8) > (self.x + self.width)) and ((yOffset + LINE_OFFSET) > (self.y + self.height)))):
                    # notify text if out from view area
                    pass

                # write border
                if self._border == Border.BOTTOM:
                    yOffset += 8
                    if m.height > 8:
                        for i in range(maxX):
                            m.matrix[yOffset][i] = 1

                elif self._border == Border.AROUND:
                    yOffset += 9
                    maxX = maxX + 2
                    if self._textAlignment == TextAlignment.CENTER:
                        maxX = self.width

                    for i in range(maxX):
                        m.matrix[0][i] = 1
                        m.matrix[yOffset][i] = 1

                    for i in range(yOffset):
                        m.matrix[i][0] = 1
                        m.matrix[i][maxX - 1] = 1

        return m


    def getTextWidth(self, font, text):
        """
        calcurate text width
        """
        textWidth = 0
        for s in text:
            tM = font.getText(s)
            tM.startX = self.x + textWidth

            if (s == '\n') or ((tM.startX + tM.width) > (self.x + self.width)):
                break
            textWidth += tM.width
        
        return textWidth


    def getTextHeight(self, font, text):
        """
        calcurate text height
        """
        textWidth = 0
        textHeight = 8

        for s in text:
            tM = font.getText(s)
            tM.startX = self.x + textWidth

            if (s == '\n') or ((tM.startX + tM.width) > (self.x + self.width)):
                textHeight += LINE_OFFSET
                textWidth = 0

            textWidth += tM.width
        
        return textHeight




# for test
if __name__ == '__main__':
    print('call text.py')