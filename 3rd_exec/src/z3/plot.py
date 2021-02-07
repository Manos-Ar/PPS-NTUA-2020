#!/bin/python3

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if len(sys.argv) < 4:
    print("Usage: plot_metrics.py  <metrics> <operation> <size>")
    exit(-1)

threads = [1, 2, 4, 8, 16, 32, 64]
implementations=["fine_grain", "optimistic", "lazy", "nonblocking"]
size=sys.argv[3]
operation=sys.argv[2]

locks={}
for i in implementations:
    locks[i]=[]



skip_sizes={"1024":0, "8192":1}
skip_operations={"80-10-10":0, "20-40-40":1}

skip_s=14*len(implementations)
skip_o=skip_s*len(skip_operations)

skip=skip_sizes[size]*skip_s+skip_o*skip_operations[operation]

with open(sys.argv[1], 'r') as fp:
    # for op,i in skip_operations.items():
    #     for siz,j in skip_sizes.items():
    #         # print(skip_sizes[siz]*skip_s+skip_o*skip_operations[op])
    for i in range(skip):
        line = fp.readline()
    line = fp.readline()
    # exit()
    i=0
    while line:
        if line.startswith("Nthreads: 1 "):
            if i==len(implementations):
                break
            implementation=implementations[i]
            i+=1
        if line.startswith("Nthreads"):
            throughput = float(line.split(":")[4].split("\n")[0])
            locks[implementation].append(throughput)
        line = fp.readline()

print("locks:",locks)


markers = ['x', 'o', '+', '*', "s", "v"]
colors = ["royalblue", "red", "darkgreen", "pink", "orange", "brown"]
x_Axis = np.array(threads)
x_ticks = np.arange(0, len(x_Axis), 1)

fig, ax = plt.subplots()
ax.grid(True)
ax.set_facecolor('#f2f5f0')
ax.set_xlabel("Number of Threads")
ax.set_ylabel("Throughput ($Mops/Sec$)")
ax.set_xlim(-0.5, len(x_Axis) - 0.5)
ax.xaxis.set_ticks(x_ticks)
ax.set_xticklabels(x_Axis, rotation=0)

i=0
for implementation,throughput in locks.items():
    ax.plot(x_ticks, throughput, label=implementation, color=colors[i%len(colors)], marker=markers[i%len(markers)])
    i+=1
ax.legend(frameon=True)
plt.title("Lock Implementations - Ops "+operation+" - Size "+str(size))
plt.savefig("plot_"+operation+"_"+size+".png",bbox_inches="tight")
