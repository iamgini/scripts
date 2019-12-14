# BAU scripts

> These are few bash scripts I use in BAU activities. 
> Thought to share publicly via github.
> 
> Please feel free to clone and use; and feedback if any.
> 
> (Amended)
> 
> Thanks

Any bugs ? Contact net.gini@gmail.com  
Thank you

www.techbeatly.com

-- [Gini](@ginigangadharan)

## `blink.sh`

A small example on `printf` and `sleep` in two nested `for` loops.

## `dns_test.sh`

DNS Test - ver 1.3.0.
- `-p` to get ping result
- `-h` to print help

Note:
add your node names or IP address in a file named "`ping.txt`" in same
directory and run the script.

Sample output:
```
6 total servers to test in: ping.txt
No.  |Hostname           |Ping |#   |STATUS
1    |ams-n-001          |YES  |1   |ams-n-001.labs.colorvibes.in |192.168.94.196 |[Reverse] 196.94.168.192.in-addr.arpa
2    |cbj-a-001          |YES  |1   |cbj-a-001.labs.colorvibes.in |192.168.94.197 |[Reverse] 197.94.168.192.in-addr.arpa
3    |ams-n-011-mgt      |YES  |1   |ams-n-011-mgt.labs.colorvibes.in |192.168.94.4 |[Reverse] 4.94.168.192.in-addr.arpa
4    |apc-a-010-mgt      |YES  |1   |apc-a-010-mgt.labs.colorvibes.in |192.168.94.5 |[Reverse] 5.94.168.192.in-addr.arpa
5    |ams-n-110-403      |YES  |1   |ams-n-110-403.labs.colorvibes.in |192.168.94.132 |[Reverse] 132.94.168.192.in-addr.arpa
6    |ams-a-111-403      |YES  |1   |ams-a-111-403.labs.colorvibes.in |192.168.94.133 |[Reverse] 133.94.168.192.in-addr.arpa

======================== Summary ======================================
6 with DNS and 0 without DNS (out of 6)
6 items alive

Started at    : Wed Aug 16 04:14:37 CEST 2017
Completed at  : Wed Aug 16 04:14:37 CEST 2017
```
Where "#" column shows the number of DNS entries (multi-dns).

## `docker-zombiehunter.sh`

## `get_oa_info.sh`

This is a very basic script to collect blade information from an HP C7000
enclosure.  The script will login to OA and excecute multiple commands,
then process the result to show the details in a tabular format.  
So far tested on ws460 Gen6/Gen8/Gen9 blades.
Please read the script and make sure you understand the working.

Notes:
- Script will exclude iSCSI/HBA interface
- Blade loop are detected by the keywords,
  if you noticed not working, please check the keywords.

Sample output:
```
# ./get_oa_info.sh AMSTERDAM-B001
Checking details of AMSTERDAM-B001
Pseudo-terminal will not be allocated because stdin is not a terminal.

-------------------------------------------------------
Enclosure Serial Number         :       SGHXYZWXYZ
-------------------------------------------------------
Bay     Blade Type      Model                   BladeName       SERIALNUM       BootMode        ILO IP          Firmware :ROM, ILO, PowerMngmt
1       Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00101 STH622XYZ                      156.31.19.97    [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
2       Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00102 STH622XYZ                      156.31.19.98    [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
3       Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00103 STH622XYZ                      156.31.19.99    [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
4       Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00104 STH622XYZ                      156.31.19.100   [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
5       Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00105 STH622XYZ                      156.31.19.101   [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
6       Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00106 STH622XYZ                      156.31.19.102   [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
7       Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00107 STH622XYZ                      156.31.19.103   [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
8       Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00108 STH622XYZ                      156.31.19.104   [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
9       Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00109 STH622XYZ                      156.31.19.105   [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
10      Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00110 STH622XYZ                      156.31.19.106   [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
11      Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00111 STH622XYZ                      156.31.19.107   [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
12      Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00112 STH622XYZ                      156.31.19.108   [I31 06/01/2015] [2.50 Sep 23 2016] [3.3.0]
13      Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00113 STH622XYZ                      156.31.19.109   [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
14      Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00114 STH622XYZ                      156.31.19.110   [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]
15      Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00115 STH622XYZ                      156.31.19.111   [I31 06/01/2015] [2.50 Sep 23 2016] [3.3.0]
16      Server Blade    ProLiant WS460c Gen8    AMSTERDAM-B00116 STH622XYZ                      156.31.19.112   [I31 12/14/2012] [1.51 Jun 16 2014] [3.1]

Bladecenter Switches
Product Name: Cisco Catalyst Blade Switch 3120X for HP  FOC1XX1T0XY
Product Name: Cisco Catalyst Blade Switch 3120X for HP  FOC1XX1T0XY

Bay     CPU, Memory
1       2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
2       2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
3       2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
4       2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
5       2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
6       2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
7       2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
8       2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
9       2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
10      2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
11      2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
12      2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
13      2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
14      2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
15      2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB
16      2 x  Intel(R) Xeon(R) CPU E5-2640 0 @ 2.50GHz (6 cores) 65536 MB

Bay     NIC
1       |NIC1:AC:16:XX:B3:XX:YY|NIC2:AC:XX:2D:B3:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
2       |NIC1:D8:9D:XX:62:XX:YY|NIC2:D8:XX:67:62:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
3       |NIC1:D8:9D:XX:62:XX:YY|NIC2:D8:XX:67:62:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
4       |NIC1:80:C1:XX:7A:XX:YY|NIC2:80:XX:6E:7A:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
5       |NIC1:AC:16:XX:B3:XX:YY|NIC2:AC:XX:2D:B3:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
6       |NIC1:AC:16:XX:B3:XX:YY|NIC2:AC:XX:2D:B3:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
7       |NIC1:AC:16:XX:AC:XX:YY|NIC2:AC:XX:2D:AC:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
8       |NIC1:AC:16:XX:B3:XX:YY|NIC2:AC:XX:2D:B3:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
9       |NIC1:D8:9D:XX:62:XX:YY|NIC2:D8:XX:67:62:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
10      |NIC1:AC:16:XX:B3:XX:YY|NIC2:AC:XX:2D:B3:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
11      |NIC1:AC:16:XX:B3:XX:YY|NIC2:AC:XX:2D:B3:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
12      |NIC1:D8:9D:XX:62:XX:YY|NIC2:D8:XX:67:62:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
13      |NIC1:D8:9D:XX:62:XX:YY|NIC2:D8:XX:67:62:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
14      |NIC1:D8:9D:XX:62:XX:YY|NIC2:D8:XX:67:62:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
15      |NIC1:D8:9D:XX:62:XX:YY|NIC2:D8:XX:67:62:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
16      |NIC1:AC:16:XX:AE:XX:YY|NIC2:AC:XX:2D:AE:XX:YY|MACAddress:D8:9D:67:XX:YY:ZZ
```

## `pydns.py`

Note:
add your node names or IP address in a file named "`ping.txt`" in same
directory and run the script.

## `python-email.py`

...

