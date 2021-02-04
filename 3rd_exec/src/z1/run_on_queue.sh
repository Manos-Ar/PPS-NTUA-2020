#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_accounts

## Output and error files
#PBS -o run_accounts.out
#PBS -e run_accounts.err

## How many machines should we get?
#PBS -l nodes=8:ppn=8

##How long should the job run for?
#PBS -l walltime=01:00:00


## Start
##echo "PBS_NODEFILE = $PBS_NODEFILE"
##cat $PBS_NODEFILE

## Start
## Run make in the src folder (modify properly)

cd /home/parallel/parlab07/a3/src/z1

# First Run
# 1 thread
MT_CONF=0 ./accounts
# 2 threads
MT_CONF=0,1 ./accounts
# 4 threads
MT_CONF=0,1,2,3 ./accounts
# 8 threads
MT_CONF=0,1,2,3,4,5,6,7 ./accounts
# 16 threads
MT_CONF=0,1,2,3,4,5,6,7,32,33,34,35,36,37,38,39 ./accounts
# 32 threads
MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47 ./accounts
# 64 threads
MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63 ./accounts


# Second Run
# 1 thread
MT_CONF=1 ./accounts
# 2 threads
MT_CONF=0,8 ./accounts
# 4 threads
MT_CONF=0,8,16,24 ./accounts
# 8 threads
MT_CONF=0,1,8,9,16,17,24,25 ./accounts
# 16 threads
MT_CONF=0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27 ./accounts
# 32 threads
MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31 ./accounts
# 64 threads
MT_CONF=0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63 ./accounts
