# -*- coding: utf-8 -*-

# matrix class

import copy

import time

class Matrix:
    """
    LED Matrix information holder class
    """
    def __init__(self, w, h):
        self._startX = 0
        self._startY = 0
        self._width = w
        self._height = h
        self.matrix = [[0 for i in range(w)] for j in range(h)]

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


    def merge(self, b: 'Matrix', t=False):
        if b is None:
            return

        s = time.time()

        bottom = self.startY + self.height
        right = self.startX + self.width

        m = self.matrix
        sY = self.startY
        sX = self.startX

        bL = b.startX
        bT = b.startY
        bR = b.startX + b.width
        bB = b.startY + b.height

        bm = b.matrix

        w = self.width
        h = self.height
        if w == 200 and h == 32:
            for y in range(bT, bB):
                for x in range(bL, bR):
                    if (y < h) and (x < w):
                        m[y][x] |= bm[y - bT][x - bL]
        else:
            for y in range(sY, bottom):
                for x in range(sX, right):
                    if ((y >= bT) and (y < bB) and (x >= bL) and (x < bR)):
                        m[y - sY][x - sX] |= bm[y - bT][x - bL]



        e = time.time()
        if t is True:
            print('... merge time ', (e - s))

    def copy(self, src: 'Matrix'):
        if src is None:
            return
        # copy matrix
        self.startX = src.startX
        self.startY = src.startY
        self.width = src.width
        self.height = src.height

#        self.matrix = np.copy(src.matrix)
        self.matrix = copy.deepcopy(src.matrix)


    def setStartX(self, x):
        self._startX = x

    def toString(self):
        for h in range(self._height):
            print(self.matrix[h,:])
