#!/bin/bash
DIR_PLOTS="plots"
DIR_METRICS="metrics"

if [ ! -d "${DIR_PLOTS}" ]; then
	mkdir ${DIR_PLOTS}
fi

./plot_1.py ${DIR_METRICS}/metrics_1.txt

# sizes=( 1024 8192 )
# operations=( "80-10-10" "20-40-40" )

# for operation in "${operations[@]}";
# do
#     for size in "${sizes[@]}";
#     do
#         ./plot.py ${METRIC} ${operation} ${size}
#     done
# done
mv plot*.png "${DIR_PLOTS}/"



