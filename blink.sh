#!/bin/sh

printf 'Working'
for i in 0 1 2 3 4; do
    for j in 0 1 2 3; do
        printf .
        sleep 5
    done
    printf '\b\b\b\b    \b\b\b\b'
done
echo '....done'
