#! /bin/sh
# Version 1.3.0 - net.gini@gmail.com
LINE="$(wc -l ping.txt | awk '{print$1}')"

RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[0;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

printf "${CYAN}DNS Test - ver 1.3.0.\n-p to get ping result\n-h to print help\n\"Single\" column shows the number of DNS entries (multi-dns).${NC}\n"

SHOWPING="NO"
while getopts "ph" option
do
        case "${option}"
        in
                d) SHOWDNS="YES";;
                p) SHOWPING="YES";;
                h) SHOWHELP="YES";;
                *)
                        usage
                   ;;

        esac
done
#==check help only or not==
if [ -n "$SHOWHELP" ]
then
        echo ""
        echo "-h Print this help"
        #echo "-d Check DNS"
        echo "-p Check PING"
        echo "Any bugs ? Contact net.gini@gmail.com"
        exit 1
fi

printf "\nTotal servers to test DNS/Ping : $LINE\n"
printf "${CYAN}%-4s |%-18s |%-6s |%-7s |%s${NC}" "No." "Hostname" "Ping" "Single?" "STATUS"
printf "\n"
counter=1
yescount=0
nocount=0
PING=0
RED='\033[0;31m'
NC='\033[0m' # No Color
TIMESTART="$(date)"
while [ $counter -le $LINE ]
do
        MYHOST=$(awk NR==$counter ping.txt|tr '[:upper:]' '[:lower:]')
        HOSTPING="-"
        #nslookup $(awk NR==$counter ping.txt) | grep Name | awk '{print$2}'
        #echo $(awk NR==$counter ping.txt)
        DNS_NAME=$(nslookup $MYHOST | grep Name | tail -1 |awk '{print$2}' 2> /dev/null)
        DNS_NAME_IP=$(host $MYHOST | egrep "domain name pointer" | tail -1 |awk '{print$5}' 2> /dev/null)

        if [ -n "$DNS_NAME" ];then
                #echo "$(awk NR==$counter ping.txt) : DNS FOUND - $DNS_NAME"
                #"$(awk NR==$counter ping.txt) : DNS FOUND - $DNS_NAME"
                ip=$(nslookup $(awk NR==$counter ping.txt) |grep Address|grep -v "#"| tail -1 |awk '{print$2}')
                #echo "$ip"
                myarpa=$(nslookup $ip | grep arpa | tail -1 | awk '{print$1}')

                #find multiple IP
                DNS_NAMES=$(nslookup $(awk NR==$counter ping.txt) | grep Name | wc -l 2> /dev/null)
                yescount=$(( $yescount + 1 ))
                #echo "$(awk NR==$counter ping.txt) : DNS FOUND $DNS_NAME       $MYIP   $MYARPA"
                if [ "$SHOWPING" == "YES" ];then
                        TOTAL=$(ping -c3 "$DNS_NAME" | grep received | awk '{print$4}' 2> /dev/null)
                        if [ $TOTAL -gt 0 ];then
                                HOSTPING="P-YES"
                                PING=$((PING + 1))
                        fi
                fi
                #printf "$DNS_NAME\t$ip\t$myarpa\n"
                printf "%-4s |%-18s |%-6s |%-7s |%s" $counter $MYHOST $HOSTPING $DNS_NAMES "$DNS_NAME |$ip |[Reverse] $myarpa"
                printf "\n"
                #TOTAL=$(ping -c3 "$DNS_NAME" | grep received | awk '{print$4}' 2> /dev/null)
        elif [ -n "$DNS_NAME_IP" ];then
                #printf "\n$DNS_NAME_IP"
                myarpa=$(host $MYHOST | egrep "domain name pointer" | tail -1 |awk '{print$1}' 2> /dev/null)
                DNS_NAMES_IP=$(host $MYHOST | egrep "domain name pointer" | wc -l 2> /dev/null)
                yescount=$(( $yescount + 1 ))

                if [ "$SHOWPING" == "YES" ];then
                        TOTAL=$(ping -c3 "$DNS_NAME_IP" | grep received | awk '{print$4}' 2> /dev/null)
                        if [ $TOTAL -gt 0 ];then
                                HOSTPING="P-YES"
                                PING=$((PING + 1))
                        fi
                fi
                printf "%-4s |%-18s |%-6s |%-7s |%s" $counter $MYHOST $HOSTPING $DNS_NAMES_IP "$DNS_NAME_IP |$MYHOST |$myarpa"
                printf "\n"
        else
                #printf "$(awk NR==$counter ping.txt) : ${RED}NO DNS Entry Found${NC}\n"
                printf "%-4s |%-18s |%-6s |%-7s |%s" $counter $MYHOST $HOSTPING "0" "NO DNS Entry Found"
                printf "\n"
                nocount=$(( $nocount + 1 ))

        fi

        #nslookup $(awk NR==$counter ping.txt) |egrep "Name|SERVFAIL"
        #nslookup $(awk NR==$counter ping.txt) |grep Address|grep -v "#"|awk '{print$2}'
                #ip=$(nslookup $(awk NR==$counter ping.txt) |grep Address|grep -v "#"|awk '{print$2}')
                #echo "$ip"
                #nslookup $ip | grep arpa

        counter=$(( $counter + 1 ))
done
printf "\n======================== Summary ======================================\n"
printf "${GREEN}$yescount ${NC}with DNS and ${YELLOW}$nocount ${NC}without DNS (out of $LINE)\n"
if [ "$SHOWPING" == "YES" ];then
        printf "$PING items alive\n"
fi
printf "\nStarted at    : $TIMESTART\n"
printf "Completed at  : $(date)\n"