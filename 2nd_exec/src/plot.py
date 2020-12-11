#!/bin/python3

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from statistics import mean 

if len(sys.argv) < 3:
    print("Usage: plot_metrics.py <input_directory_path> <input_directory_path>")
    exit(-1)

jobs_confs = [1, 2, 4, 8, 16, 32, 64]

array_sizes = [2048, 4096, 6144]

names=[]
outDirs=[]

dir_total_times = {}
dir_comp_times = {}
comp_times = {}
total_times = {}
comp_speedups = {}
total_speedups = {}


for arg in range(1,len(sys.argv)):
    outDir = sys.argv[arg]
    name = outDir.split("/")[1]
    names.append(name)
    outDirs.append(outDir)

# print(outDirs)
# print(names)

for size in array_sizes:
    dir_comp_times[size]={}
    dir_total_times[size]={}

    for name in names:
        dir_total_times[size][name] = {}
        dir_comp_times[size][name] = {}
        for j in jobs_confs:
            dir_total_times[size][name][j] = []
            dir_comp_times[size][name][j] = []

    # print(dir_comp_times)
    # print(dir_total_times)


for x in range(len(outDirs)):
    name = names[x]
    outDir = outDirs[x]
    for filename in os.listdir(outDir):
        if not filename.startswith("Converged"):
            # print(filename)
            with open(os.path.join(outDir, filename), 'r') as fp:
                line = fp.readline()

                while line:
                    if line != "\n":
                        if line.startswith("Iter"):
                            line = fp.readline()
                            continue

                        size_x = int(line.split("X")[1].split(" ")[1])
                        jobs = int(line.split("Jobs")[1].split(" ")[1])
                        comp = float(line.split("ComputationTime")[1].split(" ")[1])
                        total = float(line.split("TotalTime")[1].split(" ")[1])
                        
                        dir_comp_times[size_x][name][jobs].append(comp)
                        dir_total_times[size_x][name][jobs].append(total)

                    line = fp.readline()

# print(dir_comp_times)
# print(dir_total_times)

for size in array_sizes:
    comp_times[size]={}
    total_times[size]={}

    for name in names:
        comp_times[size][name]=[]
        total_times[size][name]=[]
        for jobs in jobs_confs:
            comp_times[size][name].append(round(mean(dir_comp_times[size][name][jobs]), 6))
            total_times[size][name].append(round(mean(dir_total_times[size][name][jobs]), 6))
        
    # print(comp_times)
    # print(total_times,"\n")

    comp_speedups[size] = {}
    total_speedups[size] = {}

    for tuple in comp_times.items():
        for name_key, times in tuple[1].items():
            comp_speedups[size][name_key] = [round(times[0]/x, 6) for x in times]
    
    for tuple in comp_times.items():
        for name_key, times in tuple[1].items():
            total_speedups[size][name_key] = [round(times[0]/x, 6) for x in times]


# print(comp_speedups)
# print(total_speedups)

markers = ['x', 'o', '+', '*']
colors = ["royalblue", "red", "darkgreen", "pink", "orange"]



## PLOT SPEEDUP
x_Axis = np.array(jobs_confs)
y_Axis = comp_speedups
# print("x_Axis: ", x_Axis)
# print("y_Axis: ", y_Axis)
x_ticks = np.arange(0, len(x_Axis), 1)

# print(x_ticks)


for tuple in y_Axis.items():
    # print (tuple)
    i = 0
    fig, ax = plt.subplots()
    print()
    for name, val in tuple[1].items():
        print("size",tuple[0],"name: ", name, ", val:", val)

        ax.grid(True)
        ax.set_facecolor('#f2f5f0')
        ax.set_xlabel("Number of Processes")
        ax.set_ylabel("Speedup (Serial Time / Parallel Time)")
        ax.set_xlim(-0.5, len(x_Axis) - 0.5)
        ax.xaxis.set_ticks(x_ticks)
        ax.set_xticklabels(x_Axis, rotation=0)

        ax.plot(x_ticks, val, label=name, color=colors[i%len(colors)], marker=markers[i%len(markers)])
        i = i + 1

    ax.legend(frameon=True)
    plt.title("Computational Speedup - Array Size: " + str(tuple[0]))
    # plt.show()
    plt.savefig("plot_speedup_comp_" + str(tuple[0]) + ".png",bbox_inches="tight")

y_Axis = total_speedups

for tuple in y_Axis.items():
    # print (tuple)
    i = 0
    fig, ax = plt.subplots()
    print()
    for name, val in tuple[1].items():
        print("size",tuple[0],"name: ", name, ", val:", val)

        ax.grid(True)
        ax.set_facecolor('#f2f5f0')
        ax.set_xlabel("Number of Processes")
        ax.set_ylabel("Speedup (Serial Time / Parallel Time)")
        ax.set_xlim(-0.5, len(x_Axis) - 0.5)
        ax.xaxis.set_ticks(x_ticks)
        ax.set_xticklabels(x_Axis, rotation=0)

        ax.plot(x_ticks, val, label=name, color=colors[i%len(colors)], marker=markers[i%len(markers)])
        i = i + 1

    ax.legend(frameon=True)
    plt.title("Total Speedup - Array Size: " + str(tuple[0]))
    # plt.show()
    plt.savefig("plot_speedup_total_" + str(tuple[0]) + ".png",bbox_inches="tight")
