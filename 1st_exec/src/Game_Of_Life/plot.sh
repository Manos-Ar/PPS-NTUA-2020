#!/bin/bash
DIR="./plots"
FILE=metrics.txt

if [ -d $DIR ]
then
 rm -r $DIR
 mkdir $DIR
else
 mkdir $DIR
fi

eval "./plot_metrics.py $FILE"
eval "./plot_metrics_single.py $FILE"
mv plot_speedup*.png "${DIR}"
mv plot_time*.png "${DIR}"
