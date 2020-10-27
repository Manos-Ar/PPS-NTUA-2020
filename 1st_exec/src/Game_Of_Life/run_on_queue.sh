# !/bin/bash

## Give the Job a descriptive name
PBS -N run_omp_Game_Of_Life

## Output and error files
PBS -o run_omp_Game_Of_Life.out
PBS -e run_omp_Game_Of_Life.err

## How many machines should we get?
PBS -l nodes=1:ppn=8

##How long should the job run for?
PBS -l walltime=00:01:00

## Start
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab07/a1/src/Game_Of_Life
export OMP_NUM_THREADS=8
./Game_Of_Life
