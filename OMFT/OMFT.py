import InstrumentDriver
import numpy as np
import socket

OMFT_port = 2000
OMFT_host = '169.254.82.1'

class OMFT:
    def __init__(self, host):
        self.host = host
        self.port = OMFT_port
        self.socket = socket.socket(socket.AF_INET)
        self.socket.connect((self.host, self.port))

    def sendScpi(self, command):
        self.socket.sendall(bytearray(command + "\n", 'utf-8'))
        reply = ""
        while reply.find('\n') < 0:
            reply = reply + self.socket.recv(1024).decode("utf-8")
        return reply

    def close():
        self.socket.close()

class Driver(InstrumentDriver.InstrumentWorker):
    """ This class implements a simple signal generator driver"""

    def performOpen(self, options={}):
        """Perform the operation of opening the instrument connection"""
        self.host_add = self.getAddress()    #gets the address of the OMFT that the user defines
        self.omft = OMFT(self.host_add)
        pass


    def performClose(self, bError=False, options={}):
        """Perform the close instrument connection operation"""
        lambda x: self.omft.close()
        pass


    def performSetValue(self, quant, value, sweepRate=0.0, options={}):
        """Perform the Set Value instrument operation. This function should
        return the actual value set by the instrument"""
        if quant.name == 'Frequency':
            self.omft.sendScpi('freq '+str(value))
        if quant.name == 'Wavelength':
            self.omft.sendScpi('wav '+str(value))
        if quant.name == 'Offset':
            self.omft.sendScpi('off '+str(value))
        if quant.name == 'Power':
            self.omft.sendScpi('pow '+str(value))
        if quant.name == 'Laser On/Off':
            self.omft.sendScpi('stat '+str(int(value)))
        # just return the value
        return value


    def performGetValue(self, quant, options={}):
        """Perform the Get Value instrument operation"""
        # proceed depending on quantity
        if quant.name == 'Frequency':
            gotvalue = float(self.omft.sendScpi('freq?'))
        if quant.name == 'Frequency':
            gotvalue = float(self.omft.sendScpi('freq?'))
        if quant.name == 'Offset':
            gotvalue = float(self.omft.sendScpi('off?'))
        if quant.name == 'Power':
            gotvalue = float(self.omft.sendScpi('pow?'))
        if quant.name == 'Laser On/Off':
            gotvalue = bool(self.omft.sendScpi('stat?'))
        # just return the value
        return gotvalue
