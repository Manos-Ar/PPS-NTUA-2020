#!/bin/bash

## Give the Job a descriptive name
# PBS -N make_omp_Game_Of_Life

## Output and error files
# PBS -e make_omp_Game_Of_Life.err
# PBS -o make_omp_Game_Of_Life.out

## How many machines should we get?
# PBS -l nodes=1:ppn=1

##How long should the job run for?
# PBS -l walltime=00:10:00

## Start
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab07/a1/src/Game_Of_Life
make
