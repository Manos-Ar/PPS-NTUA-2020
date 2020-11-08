#!/bin/bash

FILE=metrics_${1}.txt
nthreads=( 1 2 4 8 16 32 64 )
sizes=( 1024 2048 4096 )

if [ -f "$FILE" ]; then
	rm $FILE
fi
for size in "${sizes[@]}";
do
	for nthread in "${nthreads[@]}";
	do
		export OMP_NUM_THREADS=${nthread};
		echo -n "Threads ${nthread} " >> $FILE
		./${1} ${size} >> $FILE
	done
		echo >> $FILE
done