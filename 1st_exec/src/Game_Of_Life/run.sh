#!/bin/bash

FILE=metrics.txt
nthreads=( 1 2 4 6 8 )
sizes=( 64 1024 4096)

if [ -f "$FILE" ]; then
	rm $FILE
fi
for size in "${sizes[@]}";
do
	for nthread in "${nthreads[@]}";
	do
		export OMP_NUM_THREADS=${nthread};
		echo -n "Threads ${nthread} " >> $FILE
		./Game_Of_Life ${size} 1000 >> $FILE
	done
		echo >> $FILE
done
