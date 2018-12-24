#!/bin/bash
# Purpose: Matches zombie processes with the parent docker containers if possible.
# Usage: /usr/local/bin/zombiehunter.sh
# v2.0 with pod and project details
# Author: Fekete Zoltán (Z-Fekete@t-systems.com)

echo -e "\nZombies:"
ZOMBIES="$(ps -ef | grep '<defunct>' | grep -v grep | tee >(cat 1>&2))"
ZOMBIEPPIDS="$(echo "$ZOMBIES" | while read _ _ A _; do ((A>1)) && echo $A; done)"
CONTAINERS="$(for f in $(docker ps -q); do echo -n "$f "; docker inspect -f '### {{.State.Pid}} {{.Config.Labels}}' $f; done)"

[[ -n "$ZOMBIEPPIDS" ]] && [[ -n "$CONTAINERS" ]] &&
BADCONTAINERS="$(for P in $ZOMBIEPPIDS; do grep "### $P " <<<"$CONTAINERS"; done|sort|uniq)"

[[ -z "$BADCONTAINERS" ]] && echo -e "\n(found no container to restart)\n" && exit 1

echo -e "\nRestart Commands ### Details:"

[[ "-KILL" != "$1" ]] &&
echo "$BADCONTAINERS"|while read B; do echo docker restart $B; done &&
echo -e "\nPlease copy and run the restart commands manually or re-run with -KILL to kill the related zombies.\n" && exit 0

[[ "$1" == "-KILL" ]] && echo Killing... &&
echo "$BADCONTAINERS" | while read B EXTRA; do echo Running: docker restart $B $EXTRA; docker restart $B; done
