#!/bin/sh
# script to start work/home lab.

#echo $@

function display_help () {
    printf "\n"
    printf "\nUsage  : ./labmanage.sh LAB_NAME start|stop"
    printf "\nExample: ./labmanage.sh gns3 start"
    printf "\n\n"
}

function display_labs () {
    printf "\n"
    printf "\nAvailable Labs"
    printf "\ngns3 - GNS3 Network Automation"
    printf "\naap  - Ansible Automation Platform (2.1)"
    printf "\n\n"
}

function display_actions () {
    printf "\n"
    printf "\nInvalid actoion"
    printf "\nstart - Start the virtual machines and services"
    printf "\nstop  - Stop the virtual machines and services"
    printf "\n\n"
}



if [ $# -lt 1 ]; then
    printf "\nLab name and actions required !" >&2
    display_help
    exit 1
fi

if [ "$2" == "" ]; then
    printf "\nstart or stop command is required !" >&2
    display_help
    exit 1
fi

if [ "$1" == "gns3" ];then
    if [ "$2" == "start" ]; then
        VBoxManage startvm "GNS3 VM" --type headless
        VBoxManage startvm "utils-fedora35" --type headless
    elif [ "$2" == "stop" ]; then
        VBoxManage controlvm "GNS3 VM" acpipowerbutton
        VBoxManage controlvm "utils-fedora35" acpipowerbutton
    else
        display_actions
    fi
elif [ "$1" == "aap" ];then
    if [ "$2" == "start" ]; then
        VBoxManage startvm "AnsibleController21-1" --type headless
    elif [ "$2" == "stop" ]; then
        VBoxManage controlvm "AnsibleController21-1" acpipowerbutton
    else
        display_actions
    fi

else
    printf "\nNo such lab configured - $1"
    display_labs
fi

