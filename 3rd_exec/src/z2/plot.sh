#!/bin/bash
DIR_PLOTS="plots"

if [ ! -d "${DIR_PLOTS}" ]; then
	mkdir ${DIR_PLOTS}
fi
sizes=( 16 1024 8192 )

for size in "${sizes[@]}";
do
./plot.py "metrics.txt" ${size}
done
mv plot*.png "${DIR_PLOTS}/"



