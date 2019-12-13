#!/bin/sh
#20191210: version 1.2.0 - Updated details
#Contact : net.gini@gmail.com

if [ $# -lt 1 ]; then
  echo "Enclosure Name is required" >&2
fi
BladeCenter="$1"

# Check DNS
DNS_NAME=$( nslookup $BladeCenter 2>/dev/null | awk '/^Name:/ {print $2}' )
if [ -z "$DNS_NAME" ]; then
  echo "DNS is missing or invalid Enclosure name" >&2
  # From Bind 9.7 there's a separate DNS library to be used by C apps
  # That later is configured via /etc/dns.conf
  # /etc/dns.conf.sec is used as /etc/named.conf on a slave server that
  # does not save zone files locally (this type of slave only works when
  # the master server is up and running)
  # /etc/dns.conf.sec.save is used as /etc/named.conf on a slave server
  # that saves zone files locally (ths type of slave does not requiere the
  # presene of the master server)
  # /etc/dns.conf.chacheonly is used as /etc/named.conf on a caching-only
  # server
  # All those boot files has the same syntax as /etc/named.conf
  DHCP_IP=$( grep -his "$BladeCenter " /etc/dhcpd.conf* /etc/named.conf /usr/local/etc/dhcp.conf* /usr/local/etc/named.conf )
  if [ -n "$DHCP_IP" ]
  then
    BladeCenter=$( echo "$DHCP_IP" | awk '{gsub($5,";",""); print $5}' )
  else
    BladeCenter=$( awk -v pattern="$BladeCenter" 'tolower($0) ~ tolover(pattern) {print $1}' /etc/hosts )
  fi
  if [ -z "$BladeCenter" ]
  then 
    echo "No record found to access the enclosure; exiting." >&2
    exit 1
#  else
#    echo "Found IP: $BladeCenter Trying to access ..." >&2
  fi
  unset DHCP_IP
fi
echo "Checking details of $BladeCenter" >&2

temp_files="commands_for_oa oa_output temp1 temp2"
# Generate random name for cmds and output file
for i in $temp_files; do
  if command -v mktemp >/dev/null; then
    eval "RANDOM_$i=$( mktemp -p '/tmp' '.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX' )"
  elif command -v fold >/dev/null; then
    random=$( cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1 )
    eval "RANDOM_$i='/tmp/.$random'"
    eval "touch \$RANDOM_$i"
  else
    echo "Unable to create temporary files" >&2
    exit 2
  fi
done

{
  echo "show enclosure info"
  #echo "show oa network all"
  echo "show server info all"
  echo "show interconnect info 1"
  echo "show interconnect info 2"
  echo "show oa network 1"
  echo "show oa info 1"
  echo "show oa status 1"
  echo "show oa network 2"
  echo "show oa info 2"
  echo "show oa status 2"
} >"$RANDOM_commands_for_oa"

ssh -q -l "${2:-Administrator}" $BladeCenter <"$RANDOM_commands_for_oa" >"$RANDOM_oa_output"

newcounter=1
BAYCOUNT=0
line1="\n---------------------------------------------\n"
line2="\n=========================================================================\n"
HEADER01="Bay\tBlade Type\tModel\t\t\tBladeName\tSERIALNUM\tBootMode\tILO IP\t\tFirmware :ROM, ILO, PowerMngmt\n"
printf "\nBay\tCPU, Memory$line1" >"$RANDOM_temp1"
printf "\nBay\tNIC (NIC1, NIC2, iLO NIC)$line1" >"$RANDOM_temp2"
HEADER02="Enclosure (Serial Number) \t: "
HEADER03="\nBladecenter Switches$line1"
HEADER04="\nOnboard Administrators (Name, Network, MAC, Serial, Role, FW)$line1"
while read line; do
  SERVERNAME="#"
  for i in 'ROMVERSION' 'BOOTMODE' 'CPU1' 'CPU2' 'MEMORY' 'ILOROM' 'ILOIP' 'PMROM'; do
    eval "$i=''"
  done
  if echo "$line" | grep -qs "Server Blade #"; then
    if [ -n "$HEADER01" ]; then
      printf "$HEADER01"
      HEADER01=""
    fi
    BAYCOUNT=$(( BAYCOUNT + 1 ))
    read line
    BLADETYPE=$( echo "$line" | grep "Type: I/O Expansion Blade" )
    if [ -n "$BLADETYPE" ]; then
      printf "$BAYCOUNT\t$BLADETYPE\n"
      # Detect the last line in the expansion blade section and exit
      while read line; do
        echo "$line" | grep -qs "ROM Version:" && break
      done
    elif echo "$line" | grep -qs "No Server Blade Installed"; then
      printf "$BAYCOUNT\tNo Blade Installed\n"
    else
      # Clean up variable to be used
      NICCOUNT=0
      for i in 'PRODUCTNAME' 'SERIALNUM' 'SERVERNAME' 'ROMVERSION' 'BOOTMODE' 'CPU1' 'CPU2' 'NICA' 'ILOROM' 'ILOIP' 'PMROM' 'NICA' 'NICALL' 'CPUALL' ; do
        eval "$i=''"
      done
      # Start collecting data from blade
      while read line; do
        if echo "$line" | grep -qs 'Product Name:'; then
          PRODUCTNAME=$( echo "$line" | awk '{print $3,$4,$5}' )
        elif echo "$line" | grep -qs 'Serial Number:'; then
          SERIALNUM=$( echo "$line" | awk '{print $3}' )
        elif echo "$line" | grep -qs "Server Name:"; then
          SERVERNAME=$( echo "$line" | awk '{print $3}' )
          if [ -z "$SERVERNAME" ]; then
            SERVERNAME="<No Name>"
          fi
        elif echo "$line" | grep -qs 'ROM Version:'; then
          ROMVERSION=$( echo "$line" | awk '{print $3,$4}' )
        elif echo "$line" | grep -qs 'Boot Mode:'; then
          BOOTMODE=$( echo "$line" | awk '{print $3}' )
        elif echo "$line" | grep -qs "CPU 1:"; then
          CPU1=$( echo "$line" | cut -c 8- )
          #CPU1=$( echo "$line" | awk -F ': ' '{print $2}' )
        elif echo "$line" | grep -qs "CPU 2:"; then
          CPU2=$( echo "$line" | cut -c 8- )
          #CPU2=$( echo "$line" | awk -F ': ' '{print $2}' )
        elif echo "$line" | grep -qs 'Memory:'; then
          MEMORY=$( echo "$line" | awk '{print $2,$3}' )
        elif echo "$line" | grep "..:..:..:*" | grep -qvs "iSCSI\|HBA"; then
          NICA=$( echo "$line" | sed "s/ //g" )
          NICCOUNT=$(( NICCOUNT + 1 ))
          NICALL="$NICALL|$NICA"
        elif echo "$line" | grep -qs 'Firmware Version:'; then
          ILOROM=$( echo "$line" | cut -c 19- )
          #ILOROM=$( echo "$line" | awk -F ': ' '{print $2}' )
        elif echo "$line" | grep -qs 'IP Address:'; then
          ILOIP=$( echo "$line" | awk '{print $3}' )
        elif echo "$line" | grep -qs 'Power Management Controller'; then
          PMROM=$( echo "$line" | awk '{print $5}' )
        fi
        # Find the last line of blade set and exist loop for next blade
        # Here your decide which text need to be considered as a the end
        # of a blade section
        echo "$line" | grep -qs "Power Management Controller" && break
      done  # End collecting data from blade
      # Check if same CPU
      if [ "$CPU1" = "$CPU2" ]; then
        CPUALL="2 x $CPU1"
      else
        CPUALL="$CPU1, $CPU2"
      fi
      # Print 1st set of data
      printf "$BAYCOUNT\tServer Blade\t$PRODUCTNAME\t$SERVERNAME\t$SERIALNUM\t$BOOTMODE\t\t$ILOIP\t[$ROMVERSION] [$ILOROM] [$PMROM]\n"
      # Print 2nd set of data to temp
      printf "$BAYCOUNT\t$CPUALL\t$MEMORY\n" >>"$RANDOM_temp1"
      printf "$BAYCOUNT\t$NICALL\n" >>"$RANDOM_temp2"
    fi
  fi
  if echo "$line" | grep -qs "Enclosure Information"; then
    for i in 1 2 3 4; do
      read line
    done
    ENCSERIALNUM="$( echo "$line" | awk '{print $3}' )"
    if [ -n "$HEADER02" ]; then
      printf "$line2$HEADER02\t$BladeCenter ($ENCSERIALNUM)$line2"
      HEADER02=""
    fi
  fi
  for i in 1 2; do
    if echo "$line" | grep -qs "$i\. Ethernet"; then
      if [ -n "$HEADER03" ]; then
        printf "$HEADER03"
        HEADER03=""
      fi
      read line
      SWITCHMODEL="$line"
      for i in 1 2 3 4 5 6 7; do
        read line
      done
      printf "$SWITCHMODEL\t%s\n" "$( echo "$line" | awk '{print $3}' )"
    fi
  done
  if echo "$line" | grep -qs "Onboard Administrator #. Network Information"; then
    if [ -n "$HEADER04" ]; then
      printf "$HEADER04"
      HEADER04=""
    fi
    for i in 'NAME' 'IPADDR' 'IPMASK' 'IPGW' 'OAMAC' 'OAFW' 'OASER' 'OAROLE'; do
      eval "$i=''"
    done
    OA_C=0
    read line
    NAME="$line"
    while [ $OA_C -lt 100 ]; do
      read line
      if echo "$line" | grep -qs 'IPv4 Address:'; then
        IPADDR=$( echo "$line" | awk '{print $3}' )
      elif echo "$line" | grep -qs 'Netmask:'; then
        IPMASK=$( echo "$line" | awk '{print $2}' )
      elif echo "$line" | grep -qs 'Gateway Address:'; then
        IPGW=$( echo "$line" | awk '{print $3}' )
      elif echo "$line" | grep -qs 'MAC Address:'; then
        OAMAC=$( echo "$line" | awk '{print $3}' )
      elif echo "$line" | grep -qs 'Serial Number :'; then
        OASER=$( echo "$line" | awk '{print $4}' )
      elif echo "$line" | grep -qs "Firmware Ver. :"; then
        OAFW="$line"
        #OAFW=$( echo "$line" | awk '{print $4}' )
      elif echo "$line" | grep -qs 'Role:'; then
        OAROLE=$( echo "$line" | awk '{print $2}' )
      fi
      # Find the last line of OA set and exit loop
      # Here your decide which text need to be considered as a the end
      # of a OA section 
      if echo "$line" | grep -qs "Diagnostic Status:"; then
        printf "$NAME\t$IPADDR\t$IPMASK\t$IPGW\t$OAMAC\t$OASER\t$OAROLE\t$OAFW\n"
        break
      fi
      OA_C=$(( OA_C + 1 ))
    done
  fi
  newcounter=$(( newcounter + 1 ))
done <"$RANDOM_oa_output"

# Display details only if OA login success
if grep -qs "Enclosure Information" "$RANDOM_oa_output"; then
  cat "$RANDOM_temp1"
  cat "$RANDOM_temp2"
else
  echo "Enclosure not Accessible or Reachable" >&2
fi
# Clean temp files up
for i in $temp_files; do
  rm -rf "$i"
done
