#!/bin/python3

import matplotlib.pyplot as plt
import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')

if len(sys.argv) < 2:
    print("Usage: plot_1.py <metrics>")
    exit(-1)

blocks = [4, 8, 16, 32]
implementations = ["naive", "coalesced_A", "reduced_global"]
dimension = 2048

performances = {}
for i in implementations:
    performances[i] = []

# Read from metrics, dependent of lines in .txt (!)
with open(sys.argv[1], 'r') as fp:
    line = fp.readline()
    i = 0
    while line:
        if line.startswith(">>>> Begin"):
            line = fp.readline()
            block_dims = line.split(":")[1].split("x")[0]

            line = fp.readline()
            line = fp.readline()
            implem = line.split(":")[1].split(" ")[1].split("\n")[0]

            line = fp.readline()
            line = fp.readline()
            perform = float(line.split(":")[1].split(" ")[2])

            performances[implem].append(perform)
        line = fp.readline()

print("performances:", performances)


markers = ['x', 'o', '+', '*', "s", "v"]
colors = ["royalblue", "red", "darkgreen", "pink", "orange", "brown"]
x_Axis = np.array(blocks)
x_ticks = np.arange(0, len(x_Axis), 1)

fig, ax = plt.subplots()
ax.grid(True)
ax.set_facecolor('#f2f5f0')
ax.set_xlabel("Number of Blocks-Tiles")
ax.set_ylabel("Performance ($Gflop/s$)")
ax.set_xlim(-0.5, len(x_Axis) - 0.5)
ax.xaxis.set_ticks(x_ticks)
ax.set_xticklabels(x_Axis, rotation=0)

i = 0
for implem, perform in performances.items():
    ax.plot(x_ticks, perform, label=implem,
            color=colors[i % len(colors)], marker=markers[i % len(markers)])
    i += 1
ax.legend(frameon=True)
# plt.title("Implementation " + implem + " - Size "+str(dimension))
plt.title("Implementations - Size "+str(dimension))
# plt.savefig("plot_1_"+size+"_"+implem+".png", bbox_inches="tight")
plt.savefig("plot_1.png", bbox_inches="tight")
