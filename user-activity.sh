#!/bin/bash

# Define output file
output_file="user_activity_$(date +%Y-%m-%d-%H-%M-%S).csv"

# Print header row
echo "Username,Login Time,Source IP,TTY,sudo,su"  >> $output_file

# Track last boot time for filtering relevant entries
last_boot=$(who -b | awk '{print $3,$4}')

# Analyze last, wtmp, and sudo logs
for logfile in /var/log/last /var/log/wtmp /var/log/auth.log; do
  # Filter entries since last boot for relevant logs
  if [[ $logfile == "/var/log/last" ]]; then
    awk -v boot_time="$last_boot" '$1 > boot_time {print $1,$3,$4,$5}' $logfile
  else
    awk -v boot_time="$last_boot" '$4 > boot_time {print $1,$3,$6,$7}' $logfile
  fi | grep -E '(su | sudo)' | awk '
    {
      username=$1;
      login_time=$2;
      source_ip=$3;
      tty=$4;
      sudo_used="";
      su_used="";
      if ($0 ~ /sudo/) {
        sudo_used="YES";
      } else if ($0 ~ /su/) {
        su_used="YES";
      }
      printf("%s,%s,%s,%s,%s,%s\n", username, login_time, source_ip, tty, sudo_used, su_used);
    }
  ' >> $output_file
done

# Print success message
echo "User activity report saved to: $output_file"
