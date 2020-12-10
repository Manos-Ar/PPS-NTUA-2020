#!/usr/bin/python3
import sys
import os
from os import path
import subprocess
import shutil

size = [2048, 4096, 6144]

tuples = [(1,1), (1,2), (2,2), (4,2), (4,4), (8,4), (8,8)]

if not path.isdir("metrics/"):
    os.mkdir("metrics")

dir = "metrics/"+sys.argv[1]

if not path.isdir(dir)
    os.mkdir(dir)
else:
    shutil.rmtree(dir)
    os.mkdir(dir)


for s in size:
    for t in tuples:
        threads = t[0]*t[1]
        file = f"{dir}/t_{threads}_{t[0]}_{t[1]}.txt"
        subprocess.run(f"mpirun -np {threads} --map-by node --mca btl self,tcp ./{sys.argv[1]}_mpi.out {s} {s} {t[0]} {t[1]} > {file}",shell=True)
