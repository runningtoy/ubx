#!/usr/bin/python
# Copyright (C) 2016 Berkeley Applied Analytics <john.kua@berkeleyappliedanalytics.com>
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

import ubx
import struct
import calendar
import os
import gobject
import logging
import sys
import socket
import time
import signal

d = {}
start = time.time()
_TIMEOUT = 10
loop = gobject.MainLoop()
state = 0

def signal_handler(signal, frame):
    loop.quit()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)

def timeout(*args):
    global _TIMEOUT
    if _TIMEOUT<0:
        loop.quit()
    else:
        _TIMEOUT=_TIMEOUT-1
    
def poll_nav_svin(*args):
    #print("poll_nav_status")
    #t.sendraw(("\xff" * 8) + "\xB5\x62\x02\x40\x00\x00\x42\xC8")
    t.send("NAV-SVIN", 0, [])

def callback(ty, *args):
    global state
    global d
    timeout()
    #print("callback %s %s" % (ty, repr(args)))
    d[ty] = args
 
 
    print("meanX:%s meanY:%s meanZ:%s meanAcc:%s active:%s valid:%s" %
              (d["NAV-SVIN"][0][0]["meanX"],
               d["NAV-SVIN"][0][0]["meanY"],
               d["NAV-SVIN"][0][0]["meanZ"],
               d["NAV-SVIN"][0][0]["meanAcc"],
		       d["NAV-SVIN"][0][0]["active"],
               d["NAV-SVIN"][0][0]["valid"]))
               
        #print("done")
        #loop.quit()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', '-d', help='Specify the serial port device to communicate with. e.g. /dev/ttyO5')
    args = parser.parse_args()

    if args.device is not None:
        t = ubx.Parser(callback, device=args.device)
    else:
        t = ubx.Parser(callback)
    poll_nav_svin()
    loop.run()
