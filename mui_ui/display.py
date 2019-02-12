# display class

import crc8
import serial
import time
import itertools

import RPi.GPIO as GPIO 

from threading import Lock

try:
   from matrix import Matrix, check_diff_range
except ImportError:
   from . import Matrix, check_diff_range

ACK = 0x06
NACK = 0x15


def reset_display():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.OUT)
    GPIO.output(26, GPIO.LOW)
    time.sleep(0.02)
    GPIO.output(26, GPIO.HIGH)
    time.sleep(0.5)

class Display(object):
    """
    mui Display API class
    """
    def __init__(self, device_name='/dev/ttyS0', debug=False):
        print("create display class")

        self.buf5 = bytearray(5)
        self.buf8 = bytearray(8)          

        self.mutex = Lock()

        # create led matrix
        self.ledMatrix = Matrix(200, 32)
        self.ledMatrixBuf = Matrix(200, 32) # buffer for old data

        # open UART port
        self.port = serial.Serial(device_name,
                     460800,
                     parity=serial.PARITY_NONE,
                     bytesize=serial.EIGHTBITS,
                     stopbits=1,
                     timeout=1)
        
        self.debug = debug
        self._reset()
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()


    def _reset(self):
        reset_display()

    def turnOn(self, fade):
        return self._createDisplayReqCommand(0, fade, 100)

    def turnOff(self, fade):
        return self._createDisplayReqCommand(2, fade, 0)

    def setLayout(self, matrixInfo):
        self.ledMatrix.matrix = matrixInfo.matrix

    def updateLayout(self):
        self._createLayoutCommandForDiff()
         # store current layout info
        self.ledMatrixBuf.copy(self.ledMatrix)

    def refreshDisplay(self, fade, duty):
        rdly = self.port.read(self.port.in_waiting)
        return self._createDisplayReqCommand(1, fade, duty)

    def _writePacket(self, packet):
        self.mutex.acquire()
        self.port.write(packet)
        if self.debug is True:
            print('>', packet)
        self.mutex.release()

    def _recivePacket(self, rdlen):
        self.mutex.acquire()
        self._waitRcvData()
        rdly = self.port.read(rdlen)
        if self.debug is True:
            print('<', len(rdly), rdly)
        self.mutex.release()
        return rdly

    def _waitRcvData(self):
        while self.port.in_waiting == 0:
                time.sleep(0)

        
    def _updateLayoutForce(self, fade, duty):
        packet = self._createLayoutCommand()
        if packet == None:
            return

        self._writePacket(packet)
        rcvpacket = self._recivePacket(6)
        if ( self._checkPacket(rcvpacket) == False):
            print('rcv fail.')

        # store current layout info
        self.ledMatrixBuf.copy(self.ledMatrix)
        

    def clearDisplay(self):
        self.ledMatrix = Matrix(200, 32) # clear
        self._updateLayoutForce(0, 100)
        self.refreshDisplay(0, 100)

    def getVersion(self):
        version = 0
        packet = self._createGetVersionCommand()
        if packet == None:
            return version
        
        self._writePacket(packet)
        rcvpckt = self._recivePacket(7)
        if ( self._checkPacket(rcvpckt) == False ):
            return version

        version = rcvpckt[4] * 256 + rcvpckt[5]
        print(version)
        return version

    def getMuiID(self):
        packet = self._createGetMuiIDCommand()
        if packet == None:
            return
        
        self._writePacket(packet)
        rcvpckt = self._recivePacket(29)
        if ( self._checkPacket(rcvpckt) == False ):
            return ""

        #print(rcvpckt)
        muiId = rcvpckt[4:28].decode('utf-8')
        print(muiId)
        return muiId

    def getPanelStatus(self):
        packet = self._createGetPanelStatus()
        if packet == None:
            return

        self._writePacket(packet)
        rcvpacket = self._recivePacket(15)
        if ( self._checkPacket(rcvpacket) == False):
            return

        print(rcvpacket)
        return


    def _checkPacket(self, packet):
        size = len(packet)
        if (size < 5):
            return False
        checksum = 0
        for i in range(2, size-1):
            checksum = checksum + packet[i]

        checksum = checksum & 0xFF

        if ( checksum == packet[size-1] ):
            return True
        return False


    def _createGetVersionCommand(self):
        buf = bytearray(5)
        buf[0] = 0x00
        buf[1] = 0x03
        buf[2] = 0x80
        buf[3] = 0x00
        buf[4] = 0x80
        return buf

    def _createGetMuiIDCommand(self):
        buf = bytearray(5)
        buf[0] = 0x00
        buf[1] = 0x03
        buf[2] = 0x80
        buf[3] = 0x01
        buf[4] = 0x81
        return buf

    def _createGetPanelStatus(self):
        buf = bytearray(5)
        buf[0] = 0x00
        buf[1] = 0x03
        buf[2] = 0x80
        buf[3] = 0x02
        buf[4] = 0x82
        return buf

    def _createDisplayReqCommand(self, mode, fade, duty):
        sum = 0
        self.buf8[0] = 0x00
        self.buf8[1] = 0x06
        self.buf8[2] = 0x00
        self.buf8[3] = 0x03
        self.buf8[4] = fade
        self.buf8[5] = duty
        self.buf8[6] = mode
        for i in range(2,7):
                sum = sum + self.buf8[i]
        self.buf8[7] = (sum & 0xFF)
        if self.debug is True:
            print('Sum:', self.buf8[7])

        self._writePacket(self.buf8)
        rcvpacket = self._recivePacket(6)
        return self._checkPacket(rcvpacket)

    def _createLayoutCommand(self):
        buf = bytearray(813)
        buf[0] = 0x03
        buf[1] = 0x2B
        buf[2] = 0x00
        buf[3] = 0x02
        buf[4] = 0      # x-pos
        buf[5] = 0
        buf[6] = 0      # y-pos
        buf[7] = 0
        buf[8] = 0      # width
        buf[9] = 200
        buf[10] = 0     # height
        buf[11] = 32        

        m = self.ledMatrix.matrix

        index = 0
        for y in range(32):
            for x in range(0, 200, 8):
                tmp = ( m[y][x + 0] << 7 )
                tmp |= ( m[y][x + 1] << 6 )
                tmp |= ( m[y][x + 2] << 5 )
                tmp |= ( m[y][x + 3] << 4 )
                tmp |= ( m[y][x + 4] << 3 )
                tmp |= ( m[y][x + 5] << 2 )
                tmp |= ( m[y][x + 6] << 1 )
                tmp |= ( m[y][x + 7] << 0 )

                buf[12+index] = tmp
                index += 1

        sum = 0
        for i in range(2,812):
                sum = sum + buf[i]

        buf[812] = sum & 0xFF
        if self.debug is True:
            print('checksum' , buf[812] )
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
        if self.debug is True:
            print("minX {0}, maxX {1}, minY {2}, maxY {3}".format(minX, maxX, minY, maxY))


        # check change data is exist?
        if (maxX == -1) or (maxY == -1):
            # no data has changed
            if self.debug is True:
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
        if self.debug is True:
            print("data length {0}".format(dataLen))

        buf = bytearray(dataLen + 5)
        buf[0] = (( dataLen + 3) >> 8) & 0xFF
        buf[1] = (( dataLen + 3) & 0xFF )
        buf[2] = 0x00
        buf[3] = 0x02
        buf[4] = 0x00
        buf[5] = minX
        buf[6] = 0x00
        buf[7] = minY
        buf[8] = 0x00
        buf[9] = w
        buf[10] = 0x00
        buf[11] = h

        index = 0
        for y, x in itertools.product(range(minY, maxY, 1),range(minX, maxX, 8)):
            tmp = ( self.ledMatrix.matrix[y][x + 0] << 7 )
            tmp |= ( self.ledMatrix.matrix[y][x + 1] << 6 )
            tmp |= ( self.ledMatrix.matrix[y][x + 2] << 5 )
            tmp |= ( self.ledMatrix.matrix[y][x + 3] << 4 )
            tmp |= ( self.ledMatrix.matrix[y][x + 4] << 3 )
            tmp |= ( self.ledMatrix.matrix[y][x + 5] << 2 )
            tmp |= ( self.ledMatrix.matrix[y][x + 6] << 1 )
            tmp |= ( self.ledMatrix.matrix[y][x + 7] << 0 )
            buf[12 + index] = tmp
            index += 1

        sum = 0
        for i in range(2, dataLen + 5):
                sum = sum + buf[i]
        buf[dataLen + 4] = (sum & 0xFF)
        self._writePacket(buf)
#        rcvpacket = self._recivePacket(6)
#        return self._checkPacket(rcvpacket)
        return True

    def toString(self):
        self.ledMatrix.toStrin


# for TEST
if __name__ == '__main__':
    d=Display()
    d.turnOff(2)
    time.sleep(2)
    d.turnOn(2)
