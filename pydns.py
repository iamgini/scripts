#!/usr/bin/python
# Version 2.0.0 - net.gini@gmail.com

import os
import sys
import socket
import subprocess, shlex
from datetime import datetime

class Color:
    B = '\033[94m' # blue (info)
    G = '\033[92m' # green (success)
    Y = '\033[93m' # yellow/orange (warning)
    R = '\033[91m' # red (fail)
    N = '\033[0m' # normal (reset)
    C = '\033[0;36m' # cyan (header)

# instead of reinventing the wheel, one may considere:
# Alexandro Maggio: https://www.ictshore.com/python/python-ping-tutorial/
# Scapy project: https://dev.to/ankitdobhal/let-s-ping-the-network-with-python
# Matthew Dixon Cowles, then Jens Diemer: https://pypy.org/project/python-ping
def pinghost(hostname):
    command_line = "/bin/ping -c1 " + hostname
    args = shlex.split(command_line)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pingStatus = 'ok'
    for line in p.stdout:
        output = line.rstrip().decode('UTF-8')
        if (output.endswith('unreachable.')) :
            # No route from the local system, Packets sent were never put on the wire.
            pingStatus = 'nr'
            break
        elif (output.startswith('Ping request could not find host')) :
            pingStatus = 'nf'
            break
        elif ('unknown' in output ) :
            pingStatus = 'nf'
            break
        elif (output.startswith('1 packets transmitted, 0 received')) :
            pingStatus = 'no'
            break
        elif (output.startswith('Request timed out.')) :
            # No Echo Reply message were received within the second.
            pingStatus = 'to'
            break
        # end if
    # endFor
    return pingStatus
# endDef

if len(sys.argv)>1:
    File = sys.argv[1]
else:
    File = 'ping.txt'
try:
  with open(File, mode='r') as AllLines:
    print (Color.B + 'DNS Test - ver 2.0.0.\n' + Color.N)
    TimeStart = datetime.now()
    ThisLine = 0
    HasPing = 0
    YesCount = 0
    NotCount = 0
    print  (Color.C + '%-4s |%-18s |%-4s |%s' % ('No.',"Hostname","Ping","DNS status (fqdn,ip)") + Color.N)
    for MyHost in AllLines:
        ThisLine = ThisLine + 1
        MyHost = MyHost.replace('\n','')
        try:
          startcolor = Color.G
          statusText2 = ''
          addr = socket.gethostbyname(MyHost)
          MyPing = pinghost(addr)
          if addr:
            fqdn = socket.getfqdn(MyHost)
            YesCount = YesCount + 1
            if MyPing == 'ok':
              HasPing = HasPing + 1
            else:
              startcolor = Color.Y
              statusText2 = Color.R + '[host not reachable]'
          HostPing = MyPing
          statusText = fqdn + ',' + addr + statusText2
        except IOError:
          NotCount = NotCount + 1
          statusText = 'NO DNS Entry Found'
          HostPing = 'na'
          startcolor = Color.R
        #else:
          #print 'Done'
        finally:
          print (startcolor + '%-4s |%-18s |%-4s |%s' % (ThisLine,MyHost,HostPing,statusText) + Color.N)
    TimeStop = datetime.now()
    print (Color.C + "\n======================== Summary ======================================" + Color.N)
    print (Color.G + " %s with DNS\t" % (YesCount) + Color.Y + " %s without DNS\t" % (NotCount) + Color.G + " %s reachable" %(HasPing) + Color.N)
    # %c = %a %b %d %H:%M:%S %Y
    print ("\nStarted at    : " + TimeStart.strftime("%c") + "\nCompleted at  : " + TimeStop.strftime("%c") )
except IOError:
    print("Servers list '" + File + "' Not found.")
