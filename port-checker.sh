#!/bin/sh

INPUT=port-checker-data.csv
remote_user=devops

function port_check {

  # open the port on target machine as background job
  COMMAND_STRING="sudo nc -l $3 &>/dev/null &"
  # COMMAND_STRING="sleep 10 &>/dev/null &"
  # echo "$COMMAND_STRING"
  # ssh $remote_user@$2 "hostname -f"
  echo "Listening port >> $2:$3"
  ssh $remote_user@$2 $COMMAND_STRING
  sleep 2

  # connect from local machine to test port
  nc -v $2 $3 &  
  # LAST_PID=$(echo $!)
  # sleep 5
  # kill $LAST_PID

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
  echo "$entry_source"
  echo "Checking: $entry_source -> $entry_destination : $entry_port"
  # call the function to check
  # port_check $entry_source $entry_destination $entry_port

  COMMAND_STRING="sudo nc -l $entry_port &>/dev/null &"
  # COMMAND_STRING="sleep 10 &>/dev/null &"
  echo "$COMMAND_STRING"
  # ssh $remote_user@$2 "hostname -f"
  echo "Listening port >> $entry_destination:$entry_port"
  ssh $remote_user@$entry_destination $COMMAND_STRING
  sleep 2

  # connect from local machine to test port
  nc -v $entry_destination $entry_port & 
  echo "hhhh" 

  # if [ "$entry_source" == "" ] || [ "$entry_destination" == "" ] || [ "$entry_port" == "" ]
	# then
	# 	echo "Items missing in CSV line! Line skipped"
	# 	# missing=true
  # else
  #   echo "Checking: $entry_source -> $entry_destination : $entry_port"

  #   # call the function to check
  #   port_check $entry_source $entry_destination $entry_port
  # fi
done < $INPUT
IFS=$OLDIFS

 
