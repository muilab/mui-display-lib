
# matrix class

import numpy as np

class Matrix:
    """
    LED Matrix information holder class
    """
    def __init__(self, w, h):
        self._startX = 0
        self._startY = 0
        self._width = w
        self._height = h
        self.matrix = np.asarray([[0] * w for i in range(h)], dtype='int8')

    @property
    def startX(self):
        return self._startX

    @property
    def startY(self):
        return self._startY

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @startX.setter
    def startX(self, startX):
        self._startX = startX

    @startY.setter
    def startY(self, startY):
        self._startY = startY
    
    @width.setter
    def width(self, width):
        self._width = width

    @height.setter
    def height(self, height):
        self._height = height

    def __str__(self):
        np.set_printoptions(linewidth=np.inf)
        for h in range(self._height):
            print(self.matrix[h,0:min(self._width, 100)])

        return ''


    def merge(self, b: 'Matrix'):
        if b is None:
            return

        bottom = self.startY + self.height
        right = self.startX + self.width

        bL = b.startX
        bT = b.startY
        bR = b.startX + b.width
        bB = b.startY + b.height

        for y in range(self.startY, bottom):
            for x in range(self.startX, right):
                if ((y >= bT) and (y < bB) and (x >= bL) and (x < bR)):
                    self.matrix[y - self.startY][x - self.startX] |= b.matrix[y - bT][x - bL]
        

    def copy(self, src: 'Matrix'):
        if src is None:
            return
        # copy matrix
        self.startX = src.startX
        self.startY = src.startY
        self.width = src.width
        self.height = src.height
        self.matrix = np.copy(src.matrix)


    def setStartX(self, x):
        self._startX = x

    def toString(self):
        for h in range(self._height):
            print(self.matrix[h,:])
