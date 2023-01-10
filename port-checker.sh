#!/bin/sh

INPUT=port-checker-data.csv
remote_user=devops

function port_check {
  ssh $remote_user@$2 "hostname -f"
  ssh $remote_user@$2 "sudo nc -l $entry_port"
	# if nc -zv -w30 $1 $2 <<< '' &> /dev/null
	# then
	# 	echo "[+] Port $1/$2 is open"
	# else
	# 	echo "[-] Port $1/$2 is closed"
	# fi
}

OLDIFS=$IFS
IFS=','
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read entry_source entry_destination entry_port
do
  if [ "$entry_source" == "" ] || [ "$entry_destination" == "" ] || [ "$entry_port" == "" ]
	then
		echo "Items missing in CSV line! Line skipped"
		missing=true
  else
    echo "Source : $entry_source"
    echo "Destination : $entry_destination"
    echo "Port : $entry_port"

    # call the function to check
    port_check $entry_source $entry_destination $entry_port
  fi
done < $INPUT
IFS=$OLDIFS

 
