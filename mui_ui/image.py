# -*- coding: utf-8 -*-

# mui ui / image view class

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

        self._offset_x = 0
        self._offset_y = 0

    def setImage(self, img: str):
        if img is None:
            self._src = None
            self._imgData = Matrix(1, 1)
            return

        self._src = img
        self._loadImage()

    def setImageData(self, imgData: Matrix):
        if imgData is None:
            self.deleteImage()
            return

        self._imgData = imgData


    def deleteImage(self):
        self.setImage(None)

    def getMatrix(self):
        self._imgData.startX = self.x - self._offset_x
        self._imgData.startY = self.y - self._offset_y
        return self._imgData

    def _loadImage(self):
        if self._src is None:
            return

        # load target file
        im = ImgLib.open(self._src)
        data = im.load()

        # copy image data to matrix
        self._imgData = Matrix(im.width, im.height)
        imgData = self._imgData
        for y in range(im.height):
            for x in range(im.width):
                color = data[x,y]
                if type(color) is int:
                    if color == 1:
                        imgData.matrix[y][x] = 1
                else:
                    if len(color) == 4:
                        if color[0] == 0 and color[1] == 0 and color[2] == 0 and color[3] == 255:
                            imgData.matrix[y][x] = 1
                    else:
                        if color[0] == 0 and color[1] == 0 and color[2] == 0:
                            imgData.matrix[y][x] = 1

        self.width = im.width
        self.height = im.height

    @property
    def offset_y(self):
        return self._offset_y

    @offset_y.setter
    def offset_y(self, offset):
        self._offset_y = offset

    @property
    def offset_x(self):
        return self._offset_x

    @offset_x.setter
    def offset_x(self, offset):
        self._offset_x = offset