#!/bin/python3

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from statistics import mean

if len(sys.argv) < 4:
    print("Usage: plot_metrics.py <input_directory_path> <input_directory_path>  <input_directory_path>")
    exit(-1)

jobs_confs = [1, 2, 4, 8, 16, 32, 64]

plot_confs = [8, 16, 32, 64]

array_sizes = [2048, 4096, 6144]

names=[]
outDirs=[]

dir_total_times = {}
dir_comp_times = {}
total_times = {}
comp_times = {}
comp_speedups = {}
total_speedups = {}


for arg in range(1,len(sys.argv)):
    outDir = sys.argv[arg]
    name = outDir.split("/")[1].split("_")[0]
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
    # print()
    for name, val in tuple[1].items():
        # print("size",tuple[0],"name: ", name, ", val:", val)

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
    # print()
    for name, val in tuple[1].items():
        # print("size",tuple[0],"name: ", name, ", val:", val)

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



## PLOT BAR PLOTS

x_Axis = np.array(names)

print(total_times)
print(comp_times)
print()

for tuple_total, tuple_comp in zip(total_times.items(), comp_times.items()):
    print (tuple_total)
    print (tuple_comp)
    i = 0
    fig, ax = plt.subplots()
    print()

    total_methods_val = []
    comp_methods_val = []
    names_per_job = []

    for plot_conf in np.arange(3, len(jobs_confs)):
        # print(plot_conf)
        for name in names:
            names_per_job.append(name+"_"+str(2**plot_conf))

        for (name_total, val_total), (name_comp, val_comp) in zip(tuple_total[1].items(), tuple_comp[1].items()):
            # print()
            # print("size",tuple_total[0],"name: ", name_total, ", val:", val_total)
            # print("size",tuple_comp[0],"name: ", name_comp, ", val:", val_comp)
            total_methods_val.append(val_total[plot_conf])
            comp_methods_val.append(val_comp[plot_conf])

    ax.set_facecolor('#f2f5f0')
    ax.grid(True, linewidth=0.2)

    br1 = np.arange(len(names)*len(jobs_confs[3:]))
    br2 = [x + 0.3 for x in br1]

    line1 = plt.bar(br1, total_methods_val, label='Total', width=0.25, color = "#5975A4")
    line2 = plt.bar(br2, comp_methods_val, label='Computation', width=0.25, color = "#CC8963")

    # Add the data value on head of the bar
    for value in line1:
    	height = value.get_height()
    	ax.text(value.get_x() + value.get_width()/2., 1.002*height,'%f' % height, ha='center', va='bottom', fontsize='xx-small', fontweight='300')
    for value in line2:
    	height = value.get_height()
    	ax.text(value.get_x() + value.get_width()/2., 1.002*height,'%f' % height, ha='center', va='bottom', fontsize='xx-small', fontweight='300')

    plt.xlabel("Methods")
    plt.ylabel("Time (s)")
    plt.xticks([r + 0.15 for r in range(len(names)*len(jobs_confs[3:]))], names_per_job, rotation=45)
    plt.title("Times for each 'Method_Process' - Array Size: " + str(tuple_total[0]))
    plt.legend()
    plt.savefig("plot_times_" + str(tuple_total[0]) + ".png",bbox_inches="tight")
