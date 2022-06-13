#!/bin/sh
# script to start work/home lab.

#echo $@

if [ $# -lt 1 ]; then
    echo "Lab name and actions required !" >&2
    exit 1
fi

if [ "$2" == "" ]; then
    echo "start or stop command is required !" >&2
    exit 1
fi

if [ "$1" == "gns3" ];then
    if [ "$2" == "start" ]; then
        VBoxManage startvm "GNS3 VM" --type headless
        VBoxManage startvm "utils-fedora35" --type headless
    elif [ "$2" == "stop" ]; then
        VBoxManage controlvm "GNS3 VM" acpipowerbutton
        VBoxManage controlvm "utils-fedora35" acpipowerbutton
    fi

fi