#!/bin/bash
dir="metrics"
nthreads=( 1 2 4 8 16 32 64 )
sizes=( 1024 2048 4096 )
block=( 8 16 32 64 128 256 )

if [ ! -d "${dir}" ]; then
	mkdir ${dir}
fi

if [ -d "${dir}/${1}" ]; then
	rm -rf "${dir}/${1}"
	mkdir "${dir}/${1}"
else
	mkdir "${dir}/${1}"
fi


for b in "${block[@]}";
do
	for size in "${sizes[@]}";
	do
		for nthread in "${nthreads[@]}";
		do
			export OMP_NUM_THREADS=${nthread};

			if [ ${1} == "fw" ]; then
				FILE="${dir}/${1}/metrics_${1}.txt"
				echo -n "Threads ${nthread} " >> $FILE
				./${1} ${size} >> $FILE
			else
				FILE="${dir}/${1}/metrics_${1}_${b}.txt"
				echo -n "Threads ${nthread} " >> $FILE
				./${1} ${size} ${b} >> $FILE
			fi
		done
			echo >> $FILE
	done
	if [ ${1} == "fw" ]; then
		break
	fi
done
