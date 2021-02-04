#!/bin/bash
DIR_PLOTS="plots"
DIR_METRICS="metrics"

if [ ! -d "${DIR_PLOTS}" ]; then
	mkdir ${DIR_PLOTS}
fi

./plot.py "${DIR_METRICS}/metric_3.txt"
./plot.py "${DIR_METRICS}/metric_4.txt"

mv plot*.png "${DIR_PLOTS}/"






