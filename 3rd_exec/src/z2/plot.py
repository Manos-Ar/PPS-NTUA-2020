#!/bin/python3

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if len(sys.argv) < 3:
    print("Usage: plot_metrics.py  <metrics> <size>")
    exit(-1)

threads = [1, 2, 4, 8, 16, 32, 64]
implementations=["ttas", "tas", "pthread", "nosync", "array", "clh"]
size=sys.argv[2]

locks={}
for i in implementations:
    locks[i]=[]

skiplines={"16":0, "1024":1, "8192":2}

with open(sys.argv[1], 'r') as fp:
    for i in range(skiplines[size]*84):
        line = fp.readline()
    line = fp.readline()
    i=0
    while line:  
        if line.startswith("Nthreads: 1 "):
            if i==len(implementations):
                break
            implementation=implementations[i]
            i+=1
        if line.startswith("Nthreads"):
            throughput = float(line.split(":")[3].split("\n")[0])
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
plt.title("Lock Implementations-Size "+str(size))
plt.savefig("plot_all_"+size+".png",bbox_inches="tight")

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
    if implementation!="nosync":
        ax.plot(x_ticks, throughput, label=implementation, color=colors[i%len(colors)], marker=markers[i%len(markers)])
    i+=1
ax.legend(frameon=True)
plt.title("Lock Implementations-Size "+str(size))
plt.savefig("plot_"+size+".png",bbox_inches="tight")

