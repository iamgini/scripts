#!/bin/bash
# Clean inactive docker containers and images.

HOST=$(uname -n|cut -d. -f1)
DATE=$(date '+%Y%m%d-%H%M%S')
LOGDIR=/var/log/cleanup_docker_logs

tstamp(){
echo -e "\n<<< $(date '+%Y-%m-%d %H:%M:%S') >>> $@"
}

[[ -d ${LOGDIR} ]] || mkdir -p ${LOGDIR}

exec >${LOGDIR}/cleanup_docker-${HOST}-${DATE}.log 2>&1

tstamp Cleaning up old logfiles...
/bin/find ${LOGDIR} -name "cleanup_docker.*log" -mtime +32 -ls -delete
tstamp Done.

tstamp Checking docker pool...
time /usr/sbin/lvs
tstamp Done.

tstamp Deleting 'exited' docker containers...
time docker ps -f status=exited | grep -v "^CONTAINER" | grep -v "\-init." | awk '{ print $1 }' | xargs -r docker rm
tstamp ...done.

tstamp Deleting 'dangling' docker images...
time docker images -q -f dangling=true | xargs -r docker rmi
tstamp ...done.

tstamp Checking docker pool after cleanup...
time /usr/sbin/lvs
tstamp Done.


if [ _$1 = _all ]
then

tstamp Optional action - remove all non-used docker images

tstamp Checking docker info...
time docker info 2>/dev/null|head -2
tstamp Done.

tstamp Deleting all non-used docker images...
time docker images -q | xargs -r docker rmi
tstamp ...done.

tstamp Checking docker info after cleanup...
time docker info 2>/dev/null|head -2
tstamp Done.

fi

### Restart docker if Sunday:
### (( $(date '+%u') == 7 )) &&
###  tstamp Restarting docker... &&
###  time systemctl restart docker &&
###  tstamp ...done.

tstamp Exiting.