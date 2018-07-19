"""
This is an interface module for DC Power Supply GPD-3303S manufactured by Good
Will Instrument Co., Ltd.
"""

try:
    from exceptions import RuntimeError, ImportError
except:
    pass
import serial
import sys

class MySerial(serial.Serial):
    """
    Wrapper for Serial
    """
    try:
        import io
    except ImportError:
        # serial.Serial inherits serial.FileLike
        pass
    else:
        def readline(self, eol=b'\r'):
            """
            Overrides io.RawIOBase.readline which cannot handle with '\r' delimiters
            """
            leneol = len(eol)
            ret = b''
            while True:
                c = self.read(1)
                if c:
                    ret += c
                    if ret[-leneol:] == eol:
                        break
                else:
                    break

            return ret

class GPD3303S(object):
    def __init__(self):
        self.__baudRate = 9600 # 9600 bps
        self.__parityBit = 'N' # None
        self.__dataBit = 8
        self.__stopBit = 1
        self.__dataFlowControl = None
        self.eol = b'\r'

    def open(self, port, readTimeOut = 1, writeTimeOut = 1):
        self.serial = MySerial(port         = port,
                               baudrate     = self.__baudRate,
                               bytesize     = self.__dataBit,
                               parity       = self.__parityBit,
                               stopbits     = self.__stopBit,
                               timeout      = readTimeOut,
                               writeTimeout = writeTimeOut,
                               dsrdtr       = self.__dataFlowControl)
        
        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

        # Check if the delimiter is properly set
        # By default, \r is the delimiter, but newer GPD3303S uses \r\n instead.
        self.setTimeout(0.1)
        ret = self.serial.read(1)
        self.setTimeout(readTimeOut)
        
        if ret == b'\n':
            self.setDelimiter(b'\r\n')
    
    def close(self):
        self.serial.close()

    def setDelimiter(self, eol = b'\r\n'):
        """
        Must call this method for new-firmware (2.0 or above?) instruments.
        Because the delimiter setting has been changed. 
        """
        self.eol = eol

    def setTimeout(self, timeout):
        if hasattr(self.serial, 'setTimeout') and \
           callable(getattr(self.serial, 'setTimeout')):
            # pySerial <= v2.7
            self.serial.setTimeout(timeout)
        else:
            # pySerial v3
            self.serial.timeout = timeout

    def isValidChannel(self, channel):
        """
        Check if the given channel number is valid or not. Only channel 1 and 2
        are allowed.
        """
        if not (channel == 1 or channel == 2):
            raise RuntimeError('Invalid channel number: %d was given.' % channel)

        return True

    def isValidMemory(self, memory):
        """
        Check if the given memory number is valid or not. Only memory 1 to 2
        are allowed.
        """
        if not (memory <= 0 or 4 < memory):
            raise RuntimeError('Invalid memory number: %d was given.' % memory)

        return True

    def isValidFloat(self, value):
        """
        Check if the given float number is valid or not. Three or less
        significant figures are allowed.
        """
        if value < 0:
            raise RuntimeError('Invalid float value: %f was given.' % value)
        
        str = "%f" % value
        position = str.find(".")
        maxDigits = 5
        if 0 <= position and position <= maxDigits : # found
            str = str[0:maxDigits + 1]
        else: # not found
            str = str[0:maxDigits]

        if float(str) != value:
            sys.stderr.write('Invalid float value: %f was given.' % value)
            return False
        
        return True

    def setCurrent(self, channel, current):
        """
        ISET<X>:<NR2>
        """
        self.isValidChannel(channel)
        self.serial.write(b'ISET%d:%.3f\n' % (channel, current))

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)
        
    def getCurrent(self, channel):
        """
        ISET<X>?
        """
        self.isValidChannel(channel)
        self.serial.write(b'ISET%d?\n' % channel)
        ret = self.serial.readline(eol=self.eol)

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

        return float(ret[:-len(self.eol)].replace(b'A', b''))

    def setVoltage(self, channel, voltage):
        """
        VSET<X>:<NR2>
        """
        self.isValidChannel(channel)
        self.serial.write(b'VSET%d:%.3f\n' % (channel, voltage))

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)
        
    def getVoltage(self, channel):
        """
        VSET<X>?
        """
        self.isValidChannel(channel)
        self.serial.write(b'VSET%d?\n' % channel)
        ret = self.serial.readline(eol=self.eol)

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

        return float(ret[:-len(self.eol)].replace(b'V', b''))

    def getCurrentOutput(self, channel):
        """
        IOUT<X>?
        """
        self.isValidChannel(channel)
        self.serial.write(b'IOUT%d?\n' % channel)
        ret = self.serial.readline(eol=self.eol)

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

        return float(ret[:-len(self.eol)].replace(b'A', b''))

    def getVoltageOutput(self, channel):
        """
        VOUT<X>?
        """
        self.isValidChannel(channel)
        self.serial.write(b'VOUT%d?\n' % channel)
        ret = self.serial.readline(eol=self.eol)

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

        return float(ret[:-len(self.eol)].replace(b'V', b''))

    def selectIndependentMode(self):
        """
        TRACK<NR1>
        """
        self.serial.write(b'TRACK0\n')

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

    def selectTrackingSeriesMode(self):
        """
        TRACK<NR1>
        """
        self.serial.write(b'TRACK1\n')

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

    def selectTrackingParallelMode(self):
        """
        TRACK<NR1>
        """
        self.serial.write(b'TRACK2\n')
        
        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

    def enableBeep(self, enable = True):
        """
        BEEP<Boolean>
        """
        self.serial.write(b'BEEP%d\n' % int(enable))

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

    def enableOutput(self, enable = True):
        """
        OUT<Boolean>
        """
        self.serial.write(b'OUT%d\n' % int(enable))

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

    def printStatus(self):
        """
        STATUS?
        """
        self.serial.write(b'STATUS?\n')

        for i in range(3):
            ret = self.serial.readline(eol=self.eol)
            print(ret[:-len(self.eol)])
        
        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

    def getIdentification(self):
        """
        *IDN?
        """
        self.serial.write(b'*IDN?\n')
        
        ret = self.serial.readline(eol=self.eol)

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

        return ret[:-len(self.eol)]

    def recallSetting(self, memory):
        """
        RCL<NR1>
        """
        self.isValidMemory(memory)
        self.serial.write(b'RCL%d\n' % memory)
        
        ret = self.serial.readline(eol=self.eol)
        
        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

        return ret[:-len(self.eol)]

    def saveSetting(self, memory):
        """
        SAV<NR1>
        """
        self.isValidMemory(memory)
        self.serial.write(b'SAV%d\n' % memory)

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)
        
    def printHelp(self):
        """
        HELP?
        """
        self.serial.write(b'HELP?\n')
        
        for i in range(19):
            ret = self.serial.readline(eol=self.eol)
            print(ret[:-len(self.eol)])

        err = self.getError()
        if err != b'No Error.':
            raise RuntimeError(err)

    def getError(self):
        """
        ERR?
        """
        self.serial.write(b'ERR?\n')
        ret = self.serial.readline(eol=self.eol)
        if ret != b'':
            return ret[:-len(self.eol)]
        else:
            raise RuntimeError('Cannot read error message')


class GPD4303S(GPD3303S):
    def isValidChannel(self, channel):
        """
        Check if the given channel number is valid or not. Only channels 1 to 4
        are allowed.
        """

        if not (1 <= channel <= 4):
            raise RuntimeError('Invalid channel number: %d was given.' % channel)
        return True


