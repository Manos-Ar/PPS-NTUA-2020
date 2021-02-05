#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_locks

## Output and error files
#PBS -o run_locks.out
#PBS -e run_locks.err

## How many machines should we get?
#PBS -l nodes=8:ppn=8

##How long should the job run for?
#PBS -l walltime=01:00:00


## Start
##echo "PBS_NODEFILE = $PBS_NODEFILE"
##cat $PBS_NODEFILE

## Start
## Run make in the src folder (modify properly)

cd /home/parallel/parlab07/a3/src/z2

sizes=( 16 1024 8192 )
locks=( "ttas" "tas" "pthread" "nosync" "array" "clh" )

for lock in "${locks[@]}";
do
    for size in "${sizes[@]}";
    do
        # 1 thread
        MT_CONF=0 ./${lock}.out ${size}
        # 2 threads
        MT_CONF=0,1 ./${lock}.out ${size}
        # 4 threads
        MT_CONF=0,1,2,3 ./${lock}.out ${size}
        # 8 threads
        MT_CONF=0,1,2,3,4,5,6,7 ./${lock}.out ${size}
        # 16 threads
        MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 ./${lock}.out ${size}
        # 32 threads
        MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31 ./${lock}.out ${size}
        # 64 threads
        MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63 ./${lock}.out ${size}
    done
done