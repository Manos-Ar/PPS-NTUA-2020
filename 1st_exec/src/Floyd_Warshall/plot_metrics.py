#!/bin/python3

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print("Usage: plot_metrics.py <input_directory_path>")
    exit(-1)

outDir = sys.argv[1]
threads_confs = [1, 2, 4, 8, 16, 32, 64]
array_sizes = [1024, 2048, 4096]
block_size = [16, 32, 64, 128, 256]
implementations = {"fw": "", "fw_sr": "Recursive", "fw_tiled": "Tiled", "fw_tiled_opt": "Tiled Optimal"}
name = implementations[outDir.split("/")[1]]

times = {}
speedups = {}
for n in array_sizes:
    times[n] = {}
    speedups[n] = {}
    for b in block_size:
        times[n][b] = []
        speedups[n][b] = []



for filename in os.listdir(outDir):
    with open(os.path.join(outDir, filename), 'r') as fp:
        line = fp.readline()

        while line:
            if line != "\n":
                tokens = line.split(",")
                threads = int(tokens[0].split(" ")[1])
                array_size = int(tokens[1])
                time = float(tokens[len(tokens)-1])
                block = int(tokens[2])
                # print (threads, array_size, block, time)
                times[array_size][block].append(time)

            line = fp.readline()

for arr_size, b_size in times.items():
    for key, val in b_size.items():
        speedups[arr_size][key] = [val[0]/x for x in val]
# print ("times: ", times)
# print ("speedups: ", speedups)


markers = ['x', 'o', '+', '*']
colors = ["royalblue", "red", "darkgreen", "pink", "orange"]

## PLOT TIMES
x_Axis = np.array(threads_confs)
y_Axis = times
# print("x_Axis: ", x_Axis)
# print("y_Axis: ", y_Axis)
x_ticks = np.arange(0, len(x_Axis), 1)

for tuple in y_Axis.items():
    # print ("tuple[1] = ", tuple[1])
    i = 0
    fig, ax = plt.subplots()

    for b_size, val in tuple[1].items():
        # print("b_size: ", b_size, ", val:", val)

        ax.grid(True)
        ax.set_facecolor('#f2f5f0')
        ax.set_xlabel("Number of Threads")
        ax.set_ylabel("Time ($sec$)")
        ax.set_xlim(-0.5, len(x_Axis) - 0.5)
        ax.xaxis.set_ticks(x_ticks)
        ax.set_xticklabels(x_Axis, rotation=0)

        ax.plot(x_ticks, val, label="B = " + str(b_size), color=colors[i%len(colors)], marker=markers[i%len(markers)])
        i = i + 1

    ax.legend(frameon=True)
    plt.title("Floyd-Warshall " + name + "- Time - Array Size: " + str(tuple[0]))
    plt.savefig("plot_time_" + str(tuple[0]) + ".png",bbox_inches="tight")


## PLOT SPEEDUP
x_Axis = np.array(threads_confs)
y_Axis = speedups
# print("x_Axis: ", x_Axis)
# print("y_Axis: ", y_Axis)
x_ticks = np.arange(0, len(x_Axis), 1)

for tuple in y_Axis.items():
    # print ("tuple[1] = ", tuple[1])
    i = 0
    fig, ax = plt.subplots()

    for b_size, val in tuple[1].items():
        # print("b_size: ", b_size, ", val:", val)

        ax.grid(True)
        ax.set_facecolor('#f2f5f0')
        ax.set_xlabel("Number of Threads")
        ax.set_ylabel("Speedup (Serial Time / Parallel Time)")
        ax.set_xlim(-0.5, len(x_Axis) - 0.5)
        ax.xaxis.set_ticks(x_ticks)
        ax.set_xticklabels(x_Axis, rotation=0)

        ax.plot(x_ticks, val, label="B = " + str(b_size), color=colors[i%len(colors)], marker=markers[i%len(markers)])
        i = i + 1

    ax.legend(frameon=True)
    plt.title("Floyd-Warshall " + name + " - Speedup - Array Size: " + str(tuple[0]))
    plt.savefig("plot_speedup_" + str(tuple[0]) + ".png",bbox_inches="tight")
