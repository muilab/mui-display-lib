# mui font class
# -*- coding: utf-8 -*-

from PIL import Image
import csv

import os
name = os.path.dirname(os.path.abspath(__name__))

pJ = os.path.join(name, './mui_ui/assets/mui_gothic_01.png')
fontFile = os.path.normpath(pJ)
print(fontFile)

pJ = os.path.join(name, './mui_ui/assets/sjis_unicode_convert_table.csv')
fontInfoFile = os.path.normpath(pJ)
print(fontInfoFile)

try:
    from display import Display
    from matrix import Matrix
except ImportError:
    from . import Display
    from . import Matrix


class MuiFont:
    """
    font class for mui
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()

        return cls._instance


    def __init__(self):
        # load font data file
        im = Image.open(fontFile)
        self.fontData = im.load()

        # load font information file
        self.fontMap = {}
        f = open(fontInfoFile)
        reader = csv.reader(f)
        for row in reader:
            w = ""
            if len(row) >= 3:
                w = row[2]

            h = ""
            if len(row) == 4:
                h = row[3]

            p = FontPos(row[0], w, h)
            self.fontMap[row[1]] = p            
        f.close

    def getText(self, s):
        # print("getText : " + s)

        if s == " ":
            return Matrix(2, 8)

        if s == "！":
            s = "!"

        mt = Matrix(8, 8)

        b = s.encode(encoding='utf-16')
        hexStr = b.hex()[4:8]
        hexStr = hexStr[2:4] + hexStr[0:2]
        hexStr = hexStr.upper()
        # print(hexStr)

        fi = self._getFontPos(hexStr)
        if fi is None:
            print("missing font pos")
            return mt

        mt = self._readFontData(fi)
        return mt

    def _getFontPos(self, str):
        if str in self.fontMap:
            # return font information
            return self.fontMap[str]

        # if not exist target font...
        return None

    def _readFontData(self, fontPos):
        #print(fontPos)
        fW = fontPos.width
        fH = fontPos.height
        mt = Matrix(fW, fH)

        if fW > 8:
            fW = 8

        if fH > 8:
            fH = 8

        for y in range(fontPos.row, fontPos.row + fH):
            for x in range(fontPos.col, fontPos.col + fW):
                color = self.fontData[x,y]
                if color == 0:
                    mt.matrix[y - fontPos.row][x - fontPos.col] = 1

        return mt



class FontPos:
    """
    font position class
    """

    def __init__(self, s1, s2, s3):
        self._row = 0
        self._col = 0
        self._width = 8
        self._height = 8

        ku = s1[0:2]
        kuNum = int(ku, 16)
        self._row = (kuNum - 33) * 8

        ten = s1[2:4]
        tenNum = int(ten, 16)
        self._col = (tenNum - 33) * 8

        if len(s2) > 0:
            self._width = int(s2)

        if len(s3) > 0:
            self._height = int(s3)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def col(self):
        return self._col

    @property
    def row(self):
        return self._row

    def __str__(self):
        msg = 'row {:d}, col {:d}, w {:d}, h {:d}'
        return msg.format(self._row, self._col, self._width, self._height)


# for test
if __name__ == '__main__':
    font = MuiFont.get_instance() # mui font
    d = Display()    # mui display

    text = 'Hello World'

    offsetX = 0
    for t in text:
        tM = font.getText(t)
        tM.setStartX(offsetX)
        offsetX += tM.width
        d.setLayout(tM)

    d.updateLayout()
    d.refreshDisplay(0, 100)

    





