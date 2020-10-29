#!/bin/bash
DIR="./plots"
FILE=metrics.txt

if [ -d $DIR ]
then
 rm -r $DIR
 mkdir $DIR
 mkdir "${DIR}/Speedup"
 mkdir "${DIR}/Time"
else
 mkdir $DIR
 mkdir "${DIR}/Speedup"
 mkdir "${DIR}/Time"
fi

eval "./plot.py $FILE"
mv stats-speedup* "${DIR}/Speedup"
mv stats-time* "${DIR}/Time"
