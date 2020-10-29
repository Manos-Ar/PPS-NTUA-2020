#!/bin/bash

nthreads=( 1 2 4 6 8 )
sizes=( 64 )


for nthread in "${nthreads[@]}";
do
	for size in "${sizes[@]}";
	do
		export OMP_NUM_THREADS=${nthread};
		echo "Number of threads: ${nthread}"
		./Game_Of_Life ${size} 1000
	done
done
