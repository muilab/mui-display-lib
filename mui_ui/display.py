# display class

import crc8
import serial
import time

try:
   from matrix import Matrix, check_diff_range
except ImportError:
   from . import Matrix, check_diff_range

ACK = 0x06
NACK = 0x15

class Display:
    """
    mui Display API class
    """
    def __init__(self):
        print("create display class")
        # create led matrix
        self.ledMatrix = Matrix(200, 32)
        self.ledMatrixBuf = Matrix(200, 32) # buffer for old data

        # open UART port
        self.port = serial.Serial('/dev/ttyS0',
                     115200,
                     parity=serial.PARITY_NONE,
                     bytesize=serial.EIGHTBITS,
                     stopbits=1,
                     timeout=1)


    def turnOn(self, fade):
        packet = self._createDisplayReqCommand(0, fade, 100)
        n = self.port.write(packet) # on
        #print('>', n, packet)
        ack = self.port.read()
        if ack[0] == NACK:
            print('<', 1, ack)
            raise Exception('NACK', packet)
        # print('<', 1, ack)
        rdly = self.port.read(17)
        # print('<', len(rdly), rdly)
        self.port.write([ACK])
        # print('>', 1, ACK)


    def turnOff(self, fade):
        packet = self._createDisplayReqCommand(2, fade, 100)
        n = self.port.write(packet) # off
        #print('>', n, packet)
        ack = self.port.read()
        if ack[0] == NACK:
            print('<', 1, ack)
            raise Exception('NACK', packet)
        # print('<', 1, ack)
        rdly = self.port.read(17)
        # print('<', len(rdly), rdly)
        self.port.write([ACK])
        # print('>', 1, ACK)


    def setLayout(self, matrixInfo):
        # s = time.time()
        # for y in range(matrixInfo.height):
        #     for x in range(matrixInfo.width):
        #         self.ledMatrix.matrix[y + matrixInfo.startY][x + matrixInfo.startX] = matrixInfo.matrix[y][x]
        self.ledMatrix.matrix = matrixInfo.matrix

        # e = time.time()
        # print('??? setLayout ', (e - s))

    def updateLayout(self):
        #sT = time.time()
        packet = self._createLayoutCommandForDiff()
        if packet == None:
            return
        #cT = time.time()
        n = self.port.write(packet)
        #rT = time.time()
        #print('>', n, packet)
        #rsly = self.port.read(1)
        #print('<', len(rsly), rsly)
        #self.port.write([ACK])

        # store current layout info
        self.ledMatrixBuf.copy(self.ledMatrix)
        #eT = time.time()
        # print("create comannd time {0}".format(cT - sT))
        # print("send comannd time {0}".format(rT - sT))

    def refreshDisplay(self, fade, duty):
        packet = self._createDisplayReqCommand(1, fade, duty)
        n = self.port.write(packet)
        #print('>', n, packet)
        ack = []
        while True:
            ack = self.port.read()
            if len(ack) != 0:
                break;
        if ack[0] == NACK:
            print('<', 1, ack)
            raise Exception('NACK', packet)
        #print('<', 1, ack)
        rdly = self.port.read(17)
        #print('<', len(rdly), rdly)
        self.port.write([ACK])
        #print('>', 1, ACK)
        
    def _updateLayoutForce(self, fade, duty):
        packet = self._createLayoutCommand()
        if packet == None:
            return

        n = self.port.write(packet)
        rsly = self.port.read(1)

        # store current layout info
        self.ledMatrixBuf.copy(self.ledMatrix)
        

    def clearDisplay(self):
        self.ledMatrix = Matrix(200, 32) # clear
        self._updateLayoutForce(0, 100)
        self.refreshDisplay(0, 100)

    def getMuiID(self):
        pass

    def _createDisplayReqCommand(self, mode, fade, duty):
        buf = bytearray(19)
        buf[0] = 0x16       # SYN
        buf[1] = 0x16       # SYN
        buf[2] = 0x01       # SOH
        buf[3:7] = b'QDLY'
        buf[7] = 0x00
        buf[8] = 0x03
        buf[9] = 0x00
        buf[10] = 0x03
        buf[11] = 0x17      # ETB
        hash = crc8.crc8()
        hash.update(buf[3:11])
        buf[12] = hash.digest()[0]
        buf[13] = 0x02      # STX
        buf[14] = mode      # mode
        buf[15] = fade      # fade
        buf[16] = duty      # fade
        buf[17] = 0x03      # ETX
        hash = crc8.crc8()
        hash.update(buf[14:17])
        buf[18] = hash.digest()[0]
        return buf

    def _createLayoutCommand(self):
        buf = bytearray(824)
        buf[0] = 0x16       # SYN
        buf[1] = 0x16       # SYN
        buf[2] = 0x01       # SOH
        buf[3:7] = b'QSLY'
        buf[7] = 0x03
        buf[8] = 0x28
        buf[9] = 0x03
        buf[10] = 0x28
        buf[11] = 0x17      # ETB
        hash = crc8.crc8()
        hash.update(buf[3:11])
        buf[12] = hash.digest()[0]
        buf[13] = 0x02      # STX
        buf[14] = 0x00      # x-pos
        buf[15] = 0x00      # x-pos
        buf[16] = 0x00      # y-pos
        buf[17] = 0x00      # y-pos
        buf[18] = 0x00
        buf[19] = 200       # display-width
        buf[20] = 0x00
        buf[21] = 32        # display-height

        m = self.ledMatrix.matrix

        index = 0
        for y in range(32):
            for x in range(0, 200, 8):
                tmp = 0
                if m[y][x + 0] == 1:
                    tmp |= 0x80
                if m[y][x + 1] == 1:
                    tmp |= 0x40
                if m[y][x + 2] == 1:
                    tmp |= 0x20
                if m[y][x + 3] == 1:
                    tmp |= 0x10
                if m[y][x + 4] == 1:
                    tmp |= 0x08
                if m[y][x + 5] == 1:
                    tmp |= 0x04
                if m[y][x + 6] == 1:
                    tmp |= 0x02
                if m[y][x + 7] == 1:
                    tmp |= 0x01

                buf[22 + index] = tmp
                index += 1

        buf[822] = 0x03
        hash = crc8.crc8()
        hash.update(buf[14:822])
        buf[823] = hash.digest()[0]
        return buf

    def _createLayoutCommandForDiff(self):

        posX = 0
        posY = 0
        w = 0
        h = 0
        dataLen = 0

        minX = 200
        maxX = -1
        minY = 32
        maxY = -1

        # mOld = self.ledMatrixBuf.matrix
        # mNew = self.ledMatrix.matrix

        #search data changed area
        # for y in range(32):
        #     for x in range(200):
        #         if (mOld[y][x] != mNew[y][x]):
        #             if x <= minX:
        #                 minX = x

        #             if x >= maxX:
        #                 maxX = x

        #             if y <= minY:
        #                 minY = y

        #             if y >= maxY:
        #                 maxY = y

        diffRange = check_diff_range(self.ledMatrixBuf.matrix, self.ledMatrix.matrix)
        minX = diffRange[0]
        maxX = diffRange[1]
        minY = diffRange[2]
        maxY = diffRange[3]
        # print("minX {0}, maxX {1}, minY {2}, maxY {3}".format(minX, maxX, minY, maxY))


        # check change data is exist?
        if (maxX == -1) or (maxY == -1):
            # no data has changed
            print('-- no data has changed --')
            return

        # calc diff data area size and data size
        minX = (minX // 8) * 8
        maxX = ((maxX // 8) * 8) + 8
        if maxX > 200:
            maxX = 200

        maxY = maxY + 1
        if maxY > 32:
            maxY = 32

        posX = minX
        posY = minY
        w = maxX - minX
        h = maxY - minY
        dataLen = ((w // 8) * h) + 8
        #print("data length {0}".format(dataLen))

        buf = bytearray(dataLen + 16)
        buf[0] = 0x16       # SYN
        buf[1] = 0x16       # SYN
        buf[2] = 0x01       # SOH
        buf[3:7] = b'QSLY'
        buf[7] = ((dataLen >> 8) & 0xFF)
        buf[8] = (dataLen & 0xFF)
        buf[9] = ((dataLen >> 8) & 0xFF)
        buf[10] = (dataLen & 0xFF)
        buf[11] = 0x17      # ETB
        hash = crc8.crc8()
        hash.update(buf[3:11])
        buf[12] = hash.digest()[0]
        buf[13] = 0x02      # STX
        buf[14] = 0x00      # x-pos
        buf[15] = minX      # x-pos
        buf[16] = 0x00      # y-pos
        buf[17] = minY      # y-pos
        buf[18] = 0x00
        buf[19] = w         # diff area width
        buf[20] = 0x00
        buf[21] = h         # diff area height

        index = 0
        for y in range(minY, maxY, 1):
            for x in range(minX, maxX, 8):
                tmp = 0
                if self.ledMatrix.matrix[y][x + 0] == 1:
                    tmp |= 0x80
                if self.ledMatrix.matrix[y][x + 1] == 1:
                    tmp |= 0x40
                if self.ledMatrix.matrix[y][x + 2] == 1:
                    tmp |= 0x20
                if self.ledMatrix.matrix[y][x + 3] == 1:
                    tmp |= 0x10
                if self.ledMatrix.matrix[y][x + 4] == 1:
                    tmp |= 0x08
                if self.ledMatrix.matrix[y][x + 5] == 1:
                    tmp |= 0x04
                if self.ledMatrix.matrix[y][x + 6] == 1:
                    tmp |= 0x02
                if self.ledMatrix.matrix[y][x + 7] == 1:
                    tmp |= 0x01

                buf[22 + index] = tmp
                index += 1

        buf[index + 22] = 0x03
        hash = crc8.crc8()
        hash.update(buf[14:(index + 22)])
        buf[index + 23] = hash.digest()[0]
        return buf

    def toString(self):
        self.ledMatrix.toString()


# for TEST
if __name__ == '__main__':
    d=Display()
    d.turnOff(2)
    time.sleep(2)
    d.turnOn(2)
