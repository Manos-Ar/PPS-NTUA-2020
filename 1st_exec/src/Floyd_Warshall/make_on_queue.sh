#!/bin/bash

## Give the Job a descriptive name
# PBS -N make_omp_Floyd_Warshall

## Output and error files
# PBS -e make_omp_Floyd_Warshall.err
# PBS -o make_omp_Floyd_Warshall.out

## How many machines should we get?
# PBS -l nodes=1:ppn=1

##How long should the job run for?
# PBS -l walltime=00:00:01

## Start
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab07/a1/src/Floyd_Warshall
make
