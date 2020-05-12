#!/bin/sh

for i in `ls -l |awk '{print $9}'|grep -v ^$`
do 
  echo $i;
  for j in `ls -l $i/ |awk '{print $9}'|grep -v ^$`
  do 
    echo "Deleteting $i-$j"
    isi worm files delete $i/$j
    rm $i/$j
  done
done