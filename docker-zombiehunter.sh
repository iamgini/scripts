#!/bin/sh
# Purpose: Matches zombie processes with the parent docker containers if possible.
# Usage: /usr/local/bin/zombiehunter.sh
# v2.0 with pod and project details
# Adapted from: Fekete Zoltán (Z-Fekete@t-systems.com)

ZombiesPID=$( ps axo pid=,stat= | awk '$2~/^Z/ {print $1}' )
[ -z "$ZombiesPID" ] && echo "No Defunct process" && exit
echo "Zombies: $ZombiesPID"
AllContainers="$( docker ps --all --format '{{.ID}} {{.State.Pid}} {{.Config.Lables}}' )"
[ -z "$AllContainers" ] && "No Docker container" && exit
BadContainers="$( echo "$AllContainers" |
  awk -v matches="$( echo "$ZombiesPID" | tr ' ' '|' )" -v OFS="\t" '$2~matches {print}' )"
[ -z "$BadContainers" ] && "No Bad container found" && exit
if [ "$1" != '-KILL' ]; then
    echo "Please, do a \"docker restart \" on the following IDs,"
    echo "or re-run \"$0 -KILL\" to automatically kill related."
    printf "ID\ts.PID\ts.Config.Labels\n%b" "$BadContainers"
else
    echo "$BadContainers" |
    while read B Infos; do
        echo "Restarting $B ### $Infos"
        docker restart $B
    done
fi
