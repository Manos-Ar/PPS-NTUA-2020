#!/bin/bash


# jacobi_mpi seidelsor_mpi redblacksor_mpi
for execfile in redblacksor_mpi
do

    if [ -d "${1}/${execfile}" ]; then
	    rm -rf "${1}/${execfile}"
	    mkdir "${1}/${execfile}"
    else
	    mkdir "${1}/${execfile}"
    fi

	for i in 1 2 3
	do
    	for size in 2048 4096 6144
		do
			echo "Iteration ${i}" >> "${1}/${execfile}/ScalabilityResultsMPI_${size}.txt"
			mpirun -np 1 --map-by node --mca btl self,tcp ${execfile}.out ${size} ${size} 1 1 >>"${1}/${execfile}/ScalabilityResultsMPI_${size}.txt"
			mpirun -np 2 --map-by node --mca btl self,tcp ${execfile}.out ${size} ${size} 2 1 >>"${1}/${execfile}/ScalabilityResultsMPI_${size}.txt"
			mpirun -np 4 --map-by node --mca btl self,tcp ${execfile}.out ${size} ${size} 2 2 >>"${1}/${execfile}/ScalabilityResultsMPI_${size}.txt"
			mpirun -np 8 --map-by node --mca btl self,tcp ${execfile}.out ${size} ${size} 4 2 >>"${1}/${execfile}/ScalabilityResultsMPI_${size}.txt"
			mpirun -np 16 --map-by node --mca btl self,tcp ${execfile}.out ${size} ${size} 4 4 >>"${1}/${execfile}/ScalabilityResultsMPI_${size}.txt"
			mpirun -np 32 --map-by node --mca btl self,tcp ${execfile}.out ${size} ${size} 8 4 >>"${1}/${execfile}/ScalabilityResultsMPI_${size}.txt"
			mpirun -np 64 --map-by node --mca btl self,tcp ${execfile}.out ${size} ${size} 8 8 >>"${1}/${execfile}/ScalabilityResultsMPI_${size}.txt"
  		done
		echo "Iteration ${i}" >> "${1}/${execfile}/ConvergedResultsMPI_1024.txt"
      	mpirun -np 64 --map-by node --mca btl self,tcp ${execfile}_conv.out 1024 1024 8 8 >>"${1}/${execfile}/ConvergedResultsMPI_1024.txt"
  	done
done
