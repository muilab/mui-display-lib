# display class

import crc8
import serial
import time

try:
    from matrix import Matrix
except ImportError:
    from . import Matrix

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
        print('<', 1, ack)
        rdly = self.port.read(17)
        print('<', len(rdly), rdly)
        self.port.write([ACK])
        print('>', 1, ACK)


    def turnOff(self, fade):
        packet = self._createDisplayReqCommand(2, fade, 100)
        n = self.port.write(packet) # off
        #print('>', n, packet)
        ack = self.port.read()
        if ack[0] == NACK:
            print('<', 1, ack)
            raise Exception('NACK', packet)
        print('<', 1, ack)
        rdly = self.port.read(17)
        print('<', len(rdly), rdly)
        self.port.write([ACK])
        print('>', 1, ACK)

    def setLayout(self, matrixInfo):
        for y in range(matrixInfo.height):
            for x in range(matrixInfo.width):
                self.ledMatrix.matrix[y + matrixInfo.startY][x + matrixInfo.startX] = matrixInfo.matrix[y][x]

    def updateLayout(self):
        packet = self._createLayoutCommand()
        n = self.port.write(packet)
        #print('>', n, packet)
        rsly = self.port.read(1024)
        #print('<', len(rsly), rsly)
        self.port.write([ACK])

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
        
    def clearDisplay(self):
        pass

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

        index = 0
        for y in range(32):
            for x in range(0, 200, 8):
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

        buf[822] = 0x03
        hash = crc8.crc8()
        hash.update(buf[14:822])
        buf[823] = hash.digest()[0]
        return buf

    def toString(self):
        self.ledMatrix.toString()


# for TEST
if __name__ == '__main__':
    d=Display()
    d.turnOff(2)
    time.sleep(2)
    d.turnOn(2)
