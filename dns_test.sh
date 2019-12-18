#!/bin/sh

while getopts "ph" option
do
        case "${option}"
        in
                d) ShowDNS="YES"; shift ;;
                p) ShowPing="YES"; shift ;;
                h) ShowHelp="YES";;
                *) exit 1 ;;
        esac
done

if [ -n "$ShowHelp" ]
then
        echo ""
        echo "-h Print this help"
        #echo "-d Check DNS"
        echo "-p Check PING"
        echo "Any bugs ? Contact net.gini@gmail.com"
        exit 0
fi

File="${1:-ping.txt}"
if [ ! -f "$File" ]
then
        echo "Servers list '$File' Not found." >&2
        exit 1
fi

AllLines="$( grep -cv '^[[:space:]]*#?' "$File" )"
ColorR='\033[0;31m' # red (fail)
ColorB='\033[0;34m' # blue (info)
ColorC='\033[0;36m' # cyan (header)
ColorY='\033[0;33m' # yellow/orange (warning)
ColorG='\033[0;32m' # green (success)
ColorN='\033[0m' # Normal (reset)

printf "${ColorB}DNS test - ver 1.3.0\n${ColorN}"
printf "${ColorC}%-4s |%-18s |%-4s |%-3s |%s${ColorN}\n" "No." "File entry" "Ping" "#" "DNS status (fqdn,ip,reverse-ptr)"
ThisLine=1
YesCount=0
NotCount=0
HasPing=0
TimeStart="$( date )"
while [ $ThisLine -le $AllLines ]
do
        MyHost=$( grep -v '^[[:space:]]*#?' "$File" | awk "NR==$ThisLine {tolower(\$0) ;print \$1}" )
        HostPing="N/A"
        NS_Name=$( nslookup $MyHost | awk '/Name/ {print $2}' | tail -1 )
        NS_Pointer=$( host $MyHost | awk '/domain name pointer/ {print $5}' | tail -1 )

        if [ -n "$NS_Name" ]
        then
                ip=$( nslookup $MyHost | awk '/Address/ {print $2}' | tail -1 )
                MyARPA=$( nslookup $ip | awk '/arpa/ {print $1}' | tail -1 )

                # Find multiple IP
                NS_Alias=$( nslookup $MyHost | grep -cs 'Name' )
                YesCount=$(( YesCount + 1 ))
                if [ -n "$ShowPing" ]
                then
                        MyPing=$( ping -c1 "$NS_Name" | awk '/received/ {print $4}' )
                        if [ $(( MyPing )) -gt 0 ]
                        then
                                HostPing="YES"
                                HasPing=$(( HasPing + 1 ))
                        else
                                HostPing="ERR"
                        fi
                fi
                printf "${ColorG}%-4s |%-18s |%-4s |%-3s |%s\n${ColorN}" $ThisLine $MyHost $HostPing $NS_Alias "$NS_Name,$ip,[Reverse] $MyARPA"
        elif [ -n "$NS_Pointer" ]
        then
                MyARPA=$( host $MyHost | awk '/domain name pointer/ {print $1}' | tail -1 )
                NS_Address=$( host $MyHost | grep -cs "domain name pointer" )
                YesCount=$(( YesCount + 1 ))

                if [ -n "$ShowPing" ]
                then
                        MyPing=$( ping -c1 "$NS_Pointer" | awk '/received/ {print $4}' )
                        if [ $(( MyPing )) -gt 0 ]
                        then
                                HostPing="YES"
                                HasPing=$(( HasPing + 1 ))
                        else
                                HostPing="ERR"
                        fi
                fi
                printf "${ColorG}%-4s |%-18s |%-4s |%-3s |%s\n${ColorN}" $ThisLine $MyHost $HostPing $NS_Address "$NS_Pointer,$MyHost,$MyARPA"
        else
                printf "${ColorR}%-4s |%-18s |%-4s |%-3s |%s\n${ColorN}" $ThisLine $MyHost $HostPing "0" "NO DNS Entry Found"
                NotCount=$(( NotCount + 1 ))

        fi
        ThisLine=$(( ThisLine + 1 ))
done
printf "\n${ColorC}======================== Summary ======================================${ColorN}\n"
printf "$File\t${ColorG} $YesCount with DNS${ColorN}\t${ColorY} $NotCount without DNS${ColorN}"
if [ -n "$ShowPing" ]
then
        printf "\t${ColorG} $HasPing reachable${ColorN}"
fi
printf "\n\nStarted at    : $TimeStart\n"
printf "Completed at  : $(date)\n"
