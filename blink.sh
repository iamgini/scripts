#!/bin/bash
# blink.sh


printf 'Working'
for ((i = 0; i < 5; ++i)); do
    for ((j = 0; j < 4; ++j)); do
        printf .
        sleep 5
    done

    printf '\b\b\b\b    \b\b\b\b'
done
printf '....done\n'