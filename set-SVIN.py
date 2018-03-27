#!/usr/bin/python
# Copyright (C) 2010 Timo Juhani Lindfors <timo.lindfors@iki.fi>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Set logging rate (in ms)

import ubx
import struct
import calendar
import os
import gobject
import logging
import sys
import socket
import time
from ubx import clearMaskShiftDict, buildMask

loop = gobject.MainLoop()
assert len(sys.argv) == 3
TIME = int(sys.argv[1])
ACC = int(sys.argv[2])



def callbackSAVEexit(ty, packet):
    print("callback %s" % repr([ty, packet]))
    #if ty == "ACK-ACK":
    if packet[0]['MsgID'] == 9:
        loop.quit()

t = ubx.Parser(callbackSAVEexit)
#t.sendraw("\xb5\x62\x06\x71\x28\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x38\x00\x00\xf4\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0d\x7c")
#FLAG: 0 Disable
#: 1:SVIN
#: 2:FIXED

t.send("CFG-TMODE3",40,{'version':0,'reserved1':1,'flags':1,'ecefXOrLat':0,'ecefYOrLon':0,'ecefZOrAlt':0,'ecefXOrLatHP':1,'ecefYOrLonHP':1,'ecefZOrAlHP':1,'reserved2':1,'fixedPosAcc':0,'svinMinDur':TIME,'svinAccLimit':ACC,'reserved3_1':1,"reserved3_2":1,"reserved3_3":1,"reserved3_4":1})
saveMask = buildMask('all', clearMaskShiftDict)
t.send("CFG-CFG", 12, {'clearMask': 0, 'saveMask': saveMask, 'loadMask': 0})
loop.run()
