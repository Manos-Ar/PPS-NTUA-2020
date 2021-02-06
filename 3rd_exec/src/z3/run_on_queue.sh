#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_sync

## Output and error files
#PBS -o run_sync.out
#PBS -e run_sync.err

## How many machines should we get?
#PBS -l nodes=8:ppn=8

##How long should the job run for?
#PBS -l walltime=01:00:00


## Start
##echo "PBS_NODEFILE = $PBS_NODEFILE"
##cat $PBS_NODEFILE

## Start
## Run make in the src folder (modify properly)

cd /home/parallel/parlab07/a3/src/z3

sizes=( 1024 8192 )
operations=( "80 10 10" "20 40 40" )
syncs=( "fine_grain" "optimistic" "lazy" "nonblocking" )

for operation in "${operations[@]}";
do
    for size in "${sizes[@]}";
    do
        for sync in "${syncs[@]}";
        do
            # 1 thread
            MT_CONF=0 ./${sync}.out ${size} ${operation}
            # 2 threads
            MT_CONF=0,1 ./${sync}.out ${size} ${operation}
            # 4 threads
            MT_CONF=0,1,2,3 ./${sync}.out ${size} ${operation}
            # 8 threads
            MT_CONF=0,1,2,3,4,5,6,7 ./${sync}.out ${size} ${operation}
            # 16 threads
            MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15 ./${sync}.out ${size} ${operation}
            # 32 threads
            MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31 ./${sync}.out ${size} ${operation}
            # 64 threads
            MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63 ./${sync}.out ${size} ${operation}
        done
    done
done
