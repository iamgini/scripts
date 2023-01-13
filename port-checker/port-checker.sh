#!/bin/sh
# version 1.0.0
# gini@iamgini.com

input_file_name=port-checker-data.csv
remote_user=devops
success_string1="Connected to "
failed_string1="No route to host"
failed_string2="Connection refused"

ColorR='\033[0;31m' # red (fail)
ColorB='\033[0;34m' # blue (info)
ColorC='\033[0;36m' # cyan (header)
ColorY='\033[0;33m' # yellow/orange (warning)
ColorG='\033[0;32m' # green (success)
ColorN='\033[0m' # Normal (reset)

function port_check {
  # open the port on target machine as background job
  command_string_listen="sudo nc -l $entry_port &>/dev/null &"
  echo "Step 1: Enable listening port $entry_destination:$entry_port: $command_string_listen"
  ssh $remote_user@$entry_destination $command_string_listen < /dev/null
  sleep 2

  # connect from source machine to test port
  listen_result=""
  output_string=""
  command_string_check="nc -v -z $entry_destination $entry_port 2>&1"
  echo "Step 2: Starting check from $entry_source: $command_string_check"
  listen_result=$(ssh $remote_user@$entry_source $command_string_check < /dev/null)
  echo $listen_result
  
  if grep -q "$success_string1" <<< "$listen_result"; then    
    printf "Result: ${ColorG}Success${ColorN}."
  elif grep -q "$failed_string1" <<< "$listen_result"; then
    printf "Result: ${ColorR}Failed connection (Message: $failed_string1)${ColorN}."    
  elif grep -q "$failed_string2" <<< "$listen_result"; then
    printf "Result: ${ColorR}Failed connection (Message: $failed_string2)${ColorN}."    
  else    
    printf "Result: ${ColorY}Please verify manually${ColorN}."    
  fi
  printf "\n"
}

OLDIFS=$IFS
IFS=','
[ ! -f $input_file_name ] && { echo "$input_file_name file not found"; exit 99; }
while IFS=, read -r entry_source entry_destination entry_port; do 


  entry_destination=$(tr -d ' ' <<< "$entry_destination")
  entry_port=$(tr -d ' ' <<< "$entry_port")
  # echo "Target: $entry_destination"
  printf "\n========= $entry_source -> $entry_destination:$entry_port =========\n"
  # call the function to check
  port_check $entry_source $entry_destination $entry_port

  # if [ "$entry_source" == "" ] || [ "$entry_destination" == "" ] || [ "$entry_port" == "" ]
	# then
	# 	echo "Items missing in CSV line! Line skipped"
	# 	# missing=true
  # else
  #   echo "Checking: $entry_source -> $entry_destination : $entry_port"

  #   # call the function to check
  #   port_check $entry_source $entry_destination $entry_port
  # fi
done < $input_file_name
IFS=$OLDIFS

 
