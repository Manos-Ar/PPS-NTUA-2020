#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_mpi

## Output and error files
#PBS -o run_mpi.out
#PBS -e run_mpi.err

## How many machines should we get?
#PBS -l nodes=8:ppn=8

##How long should the job run for?
#PBS -l walltime=01:00:00


## Start 
##echo "PBS_NODEFILE = $PBS_NODEFILE"
##cat $PBS_NODEFILE

## Start
## Run make in the src folder (modify properly)

mkdir -p ${HOME}/tmp
export TMPDIR=${HOME}/tmp

module load openmpi/1.8.3
cd /home/parallel/parlab07/a2/src

# implementations=( "jacobi" "gauss_seidel" "red_black_sor" )
implementations=( "jacobi" )

# seidelsor_mpi.out redblacksor_mpi.out

dir="metrics"

if [ ! -d "${dir}" ]; then
	mkdir ${dir}
fi



for execfile in jacobi_mpi
do

    if [ -d "${dir}/${execfile}" ]; then
	    rm -rf "${dir}/${execfile}"
	    mkdir "${dir}/${execfile}"
    else
	    mkdir "${dir}/${execfile}"
    fi

	for size in 2048 4096 6144
	do
		mpirun  -np 1 --map-by node  ${execfile}.out ${size} ${size} 1 1 >>"${dir}/${execfile}/ScalabilityResultsMPI_${size}.txt"
		mpirun  -np 2 --map-by node  ${execfile}.out ${size} ${size} 2 1 >>"${dir}/${execfile}/ScalabilityResultsMPI_${size}.txt"
		mpirun  -np 4 --map-by node   ${execfile}.out ${size} ${size} 2 2 >>"${dir}/${execfile}/ScalabilityResultsMPI_${size}.txt"
		mpirun  -np 8 --map-by node  ${execfile}.out ${size} ${size} 4 2 >>"${dir}/${execfile}/ScalabilityResultsMPI_${size}.txt"
		mpirun  -np 16 --map-by node   ${execfile}.out ${size} ${size} 4 4 >>"${dir}/${execfile}/ScalabilityResultsMPI_${size}.txt"
		mpirun  -np 32 --map-by node   ${execfile}.out ${size} ${size} 8 4 >>"${dir}/${execfile}/ScalabilityResultsMPI_${size}.txt"
		mpirun  -np 64 --map-by node   ${execfile}.out ${size} ${size} 8 8 >>"${dir}/${execfile}/ScalabilityResultsMPI_${size}.txt"
	done
done
rm -r ${HOME}/tmp