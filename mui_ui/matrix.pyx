#cython: boundscheck=False, wraparound=False, nonecheck=False
from cython.view cimport array
from libc.stdio cimport printf

cdef class Matrix:
    cdef public int startX
    cdef public int startY
    cdef public int width
    cdef public int height
    cdef public int[:,:] matrix

    def __init__(self, int w, int h):
        self.startX = 0
        self.startY = 0
        self.width = w
        self.height = h
        #self.matrix = [[0 for i in range(w)] for j in range(h)]
        self.matrix = array(shape=(h, w), itemsize=sizeof(int), format='i')
        self.matrix[:,:] = 0

    cpdef merge(self, Matrix b):
        if b is None:
            return

        cdef int bottom = self.startY + self.height
        cdef int right = self.startX + self.width

        #m = self.matrix
        cdef int sY = self.startY
        cdef int sX = self.startX

        cdef int bL = b.startX
        cdef int bT = b.startY
        cdef int bR = b.startX + b.width
        cdef int bB = b.startY + b.height

        cdef int bH = b.height
        cdef int bW = b.width

        #bm = b.matrix

        cdef int w = self.width
        cdef int h = self.height
        if w == 200 and h == 32:
            #printf("---- start full merge ---")
            for y in range(bT, bB):
                for x in range(bL, bR):
                    if ((y < h) and (x < w) and (y >= bT) and ((y - bT) < bH) and (x >= bL) and ((x - bL) < bW) and (y >= 0) and (x >= 0)):
                        if (b.matrix[y - bT][x - bL] != 0):
                            self.matrix[y][x] = 1
                        #self.matrix[y][x] |= b.matrix[y - bT][x - bL]
        else:
            #printf("---- start part merge ---")
            for y in range(sY, bottom):
                for x in range(sX, right):
                    if ((y >= bT) and (y < bB) and (x >= bL) and (x < bR) and 
                        ((y - bT) < bH) and ((x - bL) < bW) and ((y - sY) >= 0) and ((x - sX) >= 0) and ((y - sY) < h) and ((x - sX) < w)):
                        if b.matrix[y - bT][x - bL] != 0:
                            self.matrix[y - sY][x - sX] = 1
                        #self.matrix[y - sY][x - sX] |= b.matrix[y - bT][x - bL]
        

    cpdef copy(self, Matrix src):
        if src is None:
            return

        self.startX = src.startX
        self.startY = src.startY
        self.width = src.width
        self.height = src.height
        self.matrix = src.matrix.copy()


cpdef check_diff_range(int[:,:] a, int[:,:] b):
        cdef int minX = 200
        cdef int maxX = -1
        cdef int minY = 32
        cdef int maxY = -1

        for y in range(32):
            for x in range(200):
                if (a[y][x] != b[y][x]):
                    if x <= minX:
                        minX = x

                    if x >= maxX:
                        maxX = x

                    if y <= minY:
                        minY = y

                    if y >= maxY:
                        maxY = y

        return minX, maxX, minY, maxY