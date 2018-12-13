# -*- coding: utf-8 -*-

# mui ui text view class

from PIL import Image as ImgLib

try:
    from parts import AbsParts
    from matrix import Matrix
except ImportError:
    from . import AbsParts, Matrix

class Image(AbsParts):

    def __init__(self, img:str=None, name='imageview'):
        super().__init__(name)        
        self._src = img
        self._imgData = Matrix(1, 1)
        # load image data
        self._loadImage()

    def setImage(self, img:str):
        if img == None:
            self._src = None
            self._imgData = Matrix(1, 1)
            return

        self._src = img
        self._loadImage()

    def deleteImage(self):
        self.setImage(None)

    def getMatrix(self):
        self._imgData.startX = self.x
        self._imgData.startY = self.y
        return self._imgData

    def _loadImage(self):
        if self._src == None:
            return

        # load target file
        im = ImgLib.open(self._src)
        data = im.load()

        # copy image data to matrix
        self._imgData = Matrix(im.width, im.height)
        for y in range(im.height):
            for x in range(im.width):
                color = data[x,y]
                if color[0] == 0 and color[1] == 0 and color[2] == 0:
                    self._imgData.matrix[y][x] = 1

        self.width = im.width
        self.height = im.height

