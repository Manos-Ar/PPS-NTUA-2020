# !/bin/bash

## Give the Job a descriptive name
# PBS -N run_omp_Floyd_Warshall

## Output and error files
# PBS -o run_omp_Floyd_Warshall.out
# PBS -e run_omp_Floyd_Warshall.err

## How many machines should we get?
# PBS -l nodes=8:ppn=8

##How long should the job run for?
# PBS -l walltime=00:01:00

## Start
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab07/a1/src/Floyd_Warshall

implementations=( "fw" "fw_sr" "fw_tiled" )
B=16


for implementation in "${implementations[@]}";
do
  ./run.sh ${implementation} ${B}
done
