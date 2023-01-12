#!/bin/sh

INPUT=port-checker-data.csv
remote_user=devops

function port_check {

  # open the port on target machine as background job
  COMMAND_STRING="sudo nc -l $entry_port &>/dev/null &"
  # COMMAND_STRING="sleep 10 &>/dev/null &"
  # echo "$COMMAND_STRING"
  ssh $remote_user@$entry_destination "hostname -f" < /dev/null
  echo "Listening port >> $entry_destination:$entry_port"
  ssh $remote_user@$entry_destination $COMMAND_STRING < /dev/null
  sleep 2

  # connect from local machine to test port
  # nc -v -z $entry_destination $entry_port > port-checker.log  2>&1 
  nc -v -z $entry_destination $entry_port < /dev/null
  echo "finished" 
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
# [ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
# while read entry_source entry_destination entry_port
# do
while IFS=, read -r entry_source entry_destination entry_port; do 


  entry_destination=$(tr -d ' ' <<< "$entry_destination")
  entry_port=$(tr -d ' ' <<< "$entry_port")
  # echo "Target: $entry_destination"
  printf "\n========= $entry_source -> $entry_destination:$entry_port =========\n"
  # call the function to check
  port_check $entry_source $entry_destination $entry_port

  # COMMAND_STRING="sudo nc -l $entry_port &>/dev/null &"
  # # COMMAND_STRING="sleep 10 &>/dev/null &"
  # # echo "$COMMAND_STRING"
  # ssh $remote_user@$entry_destination "hostname -f" < /dev/null
  # echo "Listening port >> $entry_destination:$entry_port"
  # ssh $remote_user@$entry_destination $COMMAND_STRING < /dev/null
  # sleep 2

  # # connect from local machine to test port
  # # nc -v -z $entry_destination $entry_port > port-checker.log  2>&1 
  # nc -v -z $entry_destination $entry_port < /dev/null
  # echo "finished" 

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

 
