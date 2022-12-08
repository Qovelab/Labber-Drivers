#!/usr/bin/env python

from VISA_Driver import VISA_Driver
import numpy as np

class Driver(VISA_Driver):
    """ This class implements the Keysight scope driver"""


    def performGetValue(self, quant, options={}):
        """Perform the Get Value instrument operation"""
        # check type of quantity
        self.write('WAV:FORMat BYTE', bCheckError=False)    # Added
        self.write('WAV:UNS 0', bCheckError=False)          # Added
        if quant.name in ('Ch1 - Data', 'Ch2 - Data','Ch3 - Data', 'Ch4 - Data') : #, 'Ch3 - Data', 'Ch4 - Data'):
            # traces, get channel
            channel = int(quant.name[2])
            # check if channel is on
            if self.getValue('Ch%d - Enabled' % channel):
                self.write("WAV:SOUR CHAN%d" %channel)      # Added
                # query range and offset
                # self.write('WAV:FORMat BYTE', bCheckError=False)
                sRange = self.askAndLog('WAV:PRE?', bCheckError=False)
                lRange = sRange.split(',')
                #<format 16-bit NR1>, <type 16-bit NR1>, <points 32-bit NR1>, <count 32-bit NR1>,
                #<xincrement 64-bit floating point NR3>, <xorigin 64-bit floating point NR3>,
                #<xreference 32-bit NR1>,
                #<yincrement 32-bit floating point NR3>, <yorigin 32-bit floating point NR3>,
                #<yreference 32-bit NR1>
                iStep = 256 if int(lRange[0])==0 else 65536
                pts = int(lRange[2])
                dt = float(lRange[4])
                gain = float(lRange[7])
                # self.log(gain)
                y_offs = float(lRange[8])
                y_offs_byte = int(lRange[9])
                # get data as i16, convert to numpy array
                self.write('WAV:DATA?', bCheckError=False)
                sHead0 = self.read(n_bytes=10)
                # strip header to find # of points
                i0 = sHead0.find(b'#')
                nDig = int(sHead0[i0+1])#[i0+1:i0+2])
                nByte = int(sHead0[i0+2:i0+2+nDig])
                # read data, including final line feed
                sData = self.read(n_bytes=(1+nByte))
                # get data to numpy array
                vData = np.frombuffer(sData[:-1], dtype='byte')       # '>f'
                # self.log(len(sData))
                # self.log(len(vData))
                value = quant.getTraceDict(gain*(vData - y_offs_byte) + y_offs, dt=dt)
                # value = quant.getTraceDict(0.001*(vData - y_offs_byte) + y_offs, dt=dt)
            else:
                # not enabled, return empty array
                value = quant.getTraceDict([])
        else:
            # for all other cases, call VISA driver
            value = VISA_Driver.performGetValue(self, quant, options)
        return value

if __name__ == '__main__':
    pass


