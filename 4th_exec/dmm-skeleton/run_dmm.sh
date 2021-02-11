#!/bin/bash
#
## run_dmm.sh -- Run DMM in GPU systems.
##
## This is an example script for submitting to the Torque system your
## experiments. You can freely change the script as you like. Please respect the
## `walltime' attribute.
##
## Please remember to compile your code with `make DEBUG=0' before
## submitting. If you plan to use this script, we recommend you to enable only
## the GPU kernels to avoid unnecessary executions of the serial and OpenMP
## version of the code wasting your time. Use similar scripts with just the
## required executions for these versions.
##
## Copyright (C) 2020, Computing Systems Laboratory (CSLab)
##

#PBS -o run_dmm_gpu.out
#PBS -e run_dmm_gpu.err
#PBS -l walltime=06:00:00
#PBS -l nodes=dungani:ppn=24:cuda

export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_VISIBLE_DEVICES=2

# gpu_kernels="0 1 2"	# Our kernels
gpu_kernels="2"

# gpu_kernels_all="0 1 2 3"	# All kernels
gpu_kernels_all="1"

problem_sizes="256 512 1024 2048"

block_sizes="4 8 16 32"

gpu_prog="./dmm_main"

## Change this to the directory of your executable!
cd /home/parallel/parlab07/a4/dmm-skeleton/cuda
echo "Benchmark started on $(date) in $(hostname)"

## Scenario: All possible configurations
# for i in $gpu_kernels; do
# 	for m in $problem_sizes; do
# 		for n in $problem_sizes; do
# 			for k in $problem_sizes; do
# 				for b in $block_sizes; do
# 					GPU_KERNEL=$i GPU_BLOCK_SIZE=$b $gpu_prog $m $n $k
# 				done
# 			done
# 		done
# 	done
# done

## Scenario 1: For (naive, coalesced, shmem) kernels, for block-tile sizes, M = N = K = 2048
for i in $gpu_kernels; do
	for b in $block_sizes; do
		make -s clean
		make -s THREAD_BLOCK_X=$b THREAD_BLOCK_Y=$b TILE_X=$b TILE_Y=$b DEBUG=0
		GPU_KERNEL=$i $gpu_prog 256 256 256
	done
done


# GPU_KERNEL=3 $gpu_prog 2048 2048 2048
# GPU_KERNEL=0 $gpu_prog 256 256 256
# GPU_KERNEL=1 $gpu_prog 256 256 256
# GPU_KERNEL=3 $gpu_prog 256 256 256

## Scenario 2: For all kernels, for M, N, K ∈ [256, 512, 1024, 2048], for best blocks dims
# for i in $gpu_kernels_all; do
# 	for m in $problem_sizes; do
# 		for n in $problem_sizes; do
# 			for k in $problem_sizes; do
# 				# make -s clean
# 				# make -s THREAD_BLOCK_X="??" THREAD_BLOCK_Y="??" DEBUG=0
# 				GPU_KERNEL=$i $gpu_prog $m $n $k
# 			done
# 		done
# 	done
# done


echo "Benchmark ended on $(date) in $(hostname)"
