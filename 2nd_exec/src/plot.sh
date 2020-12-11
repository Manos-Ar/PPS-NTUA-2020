#!/bin/bash
DIR_PLOTS="plots"
DIR_METRICS=metrics
# "redblacksor_mpi"
implementations=( "jacobi_mpi" "seidelsor_mpi"  )

if [ ! -d "${DIR_PLOTS}" ]; then
	mkdir ${DIR_PLOTS}
fi

./plot.py "${DIR_METRICS}/jacobi_mpi" "${DIR_METRICS}/seidelsor_mpi"


if [ ! -d "${DIR_PLOTS}/total_speedup" ]; then
	mkdir "${DIR_PLOTS}/total_speedup"
fi

if [ ! -d "${DIR_PLOTS}/computational_speedup" ]; then
	mkdir "${DIR_PLOTS}/computational_speedup"
fi

mv plot_speedup_total*.png "${DIR_PLOTS}/total_speedup"
mv plot_speedup_comp*.png "${DIR_PLOTS}/computational_speedup"

