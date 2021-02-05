#!/bin/bash

## Give the Job a descriptive name
#PBS -N make_locks

## Output and error files
#PBS -o make_locks.out
#PBS -e make_locks.err

## How many machines should we get?
#PBS -l nodes=1:ppn=1

##How long should the job run for?
#PBS -l walltime=00:01:00

## Start
## Run make in the src folder (modify properly)

cd /home/parallel/parlab07/a3/src/z2
make
