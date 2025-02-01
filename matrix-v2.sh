#!/bin/bash
#
# matrix: matrix-ish display for Bash terminal
# Author: Brett Terpstra 2012 <http://brettterpstra.com>
# Contributors: Lauri Ranta and Carl <http://blog.carlsensei.com/>
#
# A morning project. Could have been better, but I'm learning when to stop.
# source: https://gist.github.com/alexfornuto/f2f6ffa423bd5bc21c5e

### Customization:
blue="\033[0;34m"
brightblue="\033[1;34m"
cyan="\033[0;36m"
brightcyan="\033[1;36m"
green="\033[0;32m"
brightgreen="\033[1;32m"
red="\033[0;31m"
brightred="\033[1;31m"
white="\033[1;37m"
black="\033[0;30m"
grey="\033[0;37m"
darkgrey="\033[1;30m"
# Choose the colors that will be used from the above list
# space-separated list
# e.g. `colors=($green $brightgreen $darkgrey $white)`
colors=($green $brightgreen)
### End customization

### Do not edit below this line
spacing=${1:-100} # the likelihood of a character being left in place
scroll=${2:-1} # 0 for static, positive integer determines scroll speed (higher = faster)
screenlines=$(expr `tput lines` - 1 + $scroll)
screencols=$(expr `tput cols` / 2 - 1)

# Updated charset to English letters and numbers
chars=(a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9)

count=${#chars[@]}
colorcount=${#colors[@]}

trap "tput sgr0; clear; exit" SIGTERM SIGINT

if [[ $1 =~ '-h' ]]; then
	echo "Display a Matrix(ish) screen in the terminal"
	echo "Usage:		matrix [SPACING [SCROLL]]"
	echo "Example:	matrix 100 1"
	exit 0
fi

clear
tput cup 0 0

# Array to hold the lines for scrolling
lines=()

# Fill the lines array with initial "empty" content
for ((i=0; i<screenlines; i++)); do
  lines+=("$(printf '%.0s ' {1..$screencols})")  # Create empty lines
done

while :
do
    # Shift lines upwards (scroll effect)
    for ((i=1; i<screenlines; i++)); do
        lines[$i-1]="${lines[$i]}"
    done

    # Create a new line at the bottom with random characters
    new_line=""
    for ((i=0; i<screencols; i++)); do
        rand=$(($RANDOM % $spacing))
        case $rand in
            0)
                new_line="${new_line}${colors[$RANDOM % $colorcount]}${chars[$RANDOM % $count]} "
                ;;
            1)
                new_line="${new_line}  "
                ;;
            *)
                new_line="${new_line}\033[2C"
                ;;
        esac
    done

    lines[$screenlines-1]="$new_line"  # Add new line at the bottom

    # Print all lines with scroll effect
    clear
    for line in "${lines[@]}"; do
        echo -e "$line"
    done

    # Control the scroll speed
    sleep 0.05  # Adjust this value to control the scroll speed (lower is faster)

    tput cup 0 0  # Move cursor to the top after printing all lines
done
