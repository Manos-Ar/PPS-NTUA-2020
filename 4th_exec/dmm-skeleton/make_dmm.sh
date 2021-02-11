#!/bin/bash

## Give the Job a descriptive name
#PBS -N make_dmm_gpu

## Output and error files
#PBS -o make_dmm_gpu.out
#PBS -e make_dmm_gpu.err

## How many machines should we get?
#PBS -l nodes=dungani:ppn=1

##How long should the job run for?
#PBS -l walltime=00:01:00

## Start
## Run make in the src folder (modify properly)

cd /home/parallel/parlab07/a4/dmm-skeleton
make clean
# make DEBUG=0
make DEBUG=0 EPS=1e-5
