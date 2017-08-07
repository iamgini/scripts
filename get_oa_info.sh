#!/bin/bash
#20170807: version 1.0.5 - fixed no blade bug
#Contact : net.gini@gmail.com

if [ -z "$1" ]; then
  echo "Enclosure Name is required"
  exit 1
else
  BladeCenter=$1
fi
#check dns
DNS_NAME=$(nslookup $BladeCenter | grep Name | tail -1 |awk '{print$2}' 2> /dev/null)
if [ -n "$DNS_NAME" ];then
  echo "Checking details of $BladeCenter"
else
  echo "DNS is missing or invalid Enclosure name"
  exit 1
fi
#Generate random name for cmds and output file
RANDOM_commands_for_oa=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
RANDOM_commands_for_oa="/tmp/.$RANDOM_commands_for_oa"
RANDOM_oa_output=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
RANDOM_oa_output="/tmp/.$RANDOM_oa_output"
RANDOM_temp1=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
RANDOM_temp1="/tmp/.$RANDOM_temp1"
RANDOM_temp2=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
RANDOM_temp2="/tmp/.$RANDOM_temp2"
touch $RANDOM_oa_output
touch $RANDOM_temp1
touch $RANDOM_temp2
echo "show enclosure info" >$RANDOM_commands_for_oa
echo "show server info all" >>$RANDOM_commands_for_oa
echo "show interconnect info 1" >>$RANDOM_commands_for_oa
echo "show interconnect info 2" >>$RANDOM_commands_for_oa

ssh -q -l Administrator $BladeCenter < $RANDOM_commands_for_oa > $RANDOM_oa_output
  newcounter=1
  BAYCOUNT=0
  HEADER01="Bay\tBlade Type\tModel\t\t\tBladeName\tSERIALNUM\tBootMode\tILO IP\t\tFirmware :ROM, ILO, PowerMngmt\n"
  printf "\nBay\tCPU, Memory\n">$RANDOM_temp1
  printf "\nBay\tNIC\n">$RANDOM_temp2
  HEADER02="Enclosure (Serial Number) \t: "
  HEADER03="\nBladecenter Switches\n"
  while read line
  do
    BAYNUM=""
    ROMVERSION=""
    SERVERNAME="#"
    BOOTMODE=""
    CPU1=""
    CPU2=""
    MEMORY=""
    ILOROM=""
    ILOIP=""
    PMROM=""

    BAYNUM=$(echo "$line"|grep "Server Blade #" )
    if [ -n "$BAYNUM" ];
    then
      if [ -n "$HEADER01" ]; then
        printf "$HEADER01"
        HEADER01=""
      fi
      BAYCOUNT=$(( $BAYCOUNT + 1 ))
      read line
      BLADETYPE=$(echo "$line"|grep "Type: I/O Expansion Blade" )
      BLADETYPENO=$(echo "$line" | egrep "No Server Blade Installed" )
      if [ -n "$BLADETYPE" ];
      then
        printf "$BAYCOUNT\t$BLADETYPE\n"
        # detect the last line in the expansion blade section and exit
        ENDTHIS=""
        while read line
        do
          ENDTHIS=$(echo "$line" | egrep "ROM Version:")
          if [ -n "$ENDTHIS" ]
          then
            break
          fi
        done
      elif [ -n "$BLADETYPENO" ];
      then
        printf "$BAYCOUNT\tNo Blade Installed\n"
      else
        NICALL=""
        NICCOUNT=0
        for i in PRODUCTNAME1 PRODUCTNAME SERIALNUM1 SERIALNUM SERVERNAME1 SERVERNAME ROMVERSION1 ROMVERSION BOOTMODE1 BOOTMODE CPU11 CPU1 CPU21 CPU2 MEMORY1 MEMORY NICA1 NICA ILOROM1 ILOROM ILOIP1 ILOIP LASTLINE1 LASTLINE
        do
          export $i=""
        done

        #start collecting data from blade
        while read line
        do
        #echo $line
          PRODUCTNAME1=$(echo $line | egrep "Product Name:")
          SERIALNUM1=$(echo $line | egrep "Serial Number:")
          SERVERNAME1=$(echo $line | egrep "Server Name:")
          ROMVERSION1=$(echo $line | egrep "ROM Version:")
          BOOTMODE1=$(echo $line | egrep "Boot Mode:")
          CPU11=$(echo $line | egrep "CPU 1:")
          CPU21=$(echo $line | egrep "CPU 2:")
          MEMORY1=$(echo $line | egrep "Memory:")
          NICA1=$(echo $line | egrep "..:..:..:*" |grep -v "iSCSI"|grep -v "HBA" )
          ILOROM1=$(echo $line | egrep "Firmware Version:")
          ILOIP1=$(echo $line | egrep "IP Address:")
          PMROM1=$(echo $line | egrep "Power Management Controller")

          # find the last line of blade set and exist loop for next blade
          # here your decide which text need to be considered as a the end of a blade section
          LASTLINE1=$(echo $line | egrep "Power Management Controller")

          if [ -n "$PRODUCTNAME1" ]
          then
            PRODUCTNAME=$(echo "$line"|awk '{print$3,$4,$5}')
            #echo $PRODUCTNAME
          elif [ -n "$SERIALNUM1" ]
          then
            SERIALNUM=$(echo "$line"|awk '{print$3}')
            #echo $SERIALNUM
          elif [ -n "$SERVERNAME1" ]
          then
            SERVERNAME=$(echo "$line"|awk '{print$3}')
            #echo $SERVERNAME
                        if [ -z "$SERVERNAME" ]
            then
              SERVERNAME="<No Name>"
            fi

          elif [ -n "$ROMVERSION1" ]
          then
            ROMVERSION=$(echo "$line"|awk '{print$3,$4}' )
            #echo $ROMVERSION
          elif [ -n "$BOOTMODE1" ]
          then
            BOOTMODE=$(echo "$line"|awk '{print$3}')
            #echo $BOOTMODE
          elif [ -n "$CPU11" ]
          then
            CPU1=$(echo "$line")
            CPU1=${CPU1:7}
            #echo $CPU1
          elif [ -n "$CPU21" ]
          then
            CPU2=$(echo "$line")
            CPU2=${CPU2:7}
            #echo $CPU2
          elif [ -n "$MEMORY1" ]
          then
            MEMORY=$(echo "$line"| awk '{print$2,$3}' )
            #echo $MEMORY
          elif [ -n "$NICA1" ]
          then
            NICA=$(echo "$line"| sed "s/ //g"  )
            #echo $NICA
            NICCOUNT=$(( $NICCOUNT + 1 ))
            NICALL=$(echo "$NICALL|$NICA")
          elif [ -n "$ILOROM1" ]
          then
            ILOROM=${line:18}
            #echo $ILOROM
          elif [ -n "$ILOIP1" ]
          then
            ILOIP=$(echo "$line"|awk '{print$3}' )
            #echo $ILOIP
          elif [ -n "$PMROM1" ]
          then
            PMROM=$(echo "$line"|awk '{print$5}' )
            #echo $PMROM
          fi

          if [ -n "$LASTLINE1" ]
          then
            #echo "Break blade - $LASTLINE"
            break
          fi
        done  #end collecting data from blade

        #check if same CPU
        if [ "$CPU1" = "$CPU2" ]
        then
          CPUALL=$(echo "2 x $CPU1")
        else
          CPUALL=$(echo "$CPU1, $CPU2")
        fi

        #Print 1st set of data
        printf "$BAYCOUNT\tServer Blade\t$PRODUCTNAME\t$SERVERNAME\t$SERIALNUM\t$BOOTMODE\t\t$ILOIP\t[$ROMVERSION] [$ILOROM] [$PMROM]\n"
        #Print 2nd set of data to temp
        printf "$BAYCOUNT\t$CPUALL\t$MEMORY\n" >> $RANDOM_temp1
        printf "$BAYCOUNT\t$NICALL\n" >> $RANDOM_temp2
      fi
    fi
    #for enclosure info
    BAYNUM=$(echo "$line"|egrep "Enclosure Information" )
    if [ -n "$BAYNUM" ];
    then
      for i in `seq 1 4`;
      do
        read line
      done
      ENCSERIALNUM=$(echo "$line"|awk '{print$3}' )

      if [ -n "$HEADER02" ]; then
        printf "\n========================================================================="
        printf "\n$HEADER02\t$BladeCenter ($ENCSERIALNUM)\n=========================================================================\n"
        HEADER02=""
      fi
    fi
    #for interconnect switch info
    BAYNUM=$(echo "$line"|grep "1. Ethernet")
    if [ -n "$BAYNUM" ];
    then
            if [ -n "$HEADER03" ]; then
                    printf "$HEADER03"
                    HEADER03=""
            fi
            read line
            SWITCHMODEL="$line"
            for i in `seq 1 7`;
            do
                    read line
            done
            SWITCHSERIAL=$(echo "$line"|awk '{print$3}' )
            printf "$SWITCHMODEL\t$SWITCHSERIAL\n"
    fi
    BAYNUM=$(echo "$line"|grep "2. Ethernet" )
    if [ -n "$BAYNUM" ];
    then
            if [ -n "$HEADER03" ]; then
                    printf "$HEADER03"
                    HEADER03=""
            fi
            read line
            SWITCHMODEL="$line"
            for i in `seq 1 7`;
            do
                    read line
            done
            SWITCHSERIAL=$(echo "$line"|awk '{print$3}' )
            printf "$SWITCHMODEL\t$SWITCHSERIAL\n"
    fi

    newcounter=$(( $newcounter + 1 ))
   done < $RANDOM_oa_output
   cat $RANDOM_temp1
   cat $RANDOM_temp2
rm -rf $RANDOM_oa_output
rm -rf $RANDOM_commands_for_oa
rm -rf $RANDOM_temp1
rm -rf $RANDOM_temp2
