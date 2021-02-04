#!/bin/python3

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print("Usage: plot_metrics.py  <metric>")
    exit(-1)

threads = [1, 2, 4, 8, 16, 32, 64]
implementations=["Run1","Run2"]

time_1=[]
time_2=[]
i=0
with open(sys.argv[1], 'r') as fp:
    line = fp.readline()
    while line:  
        if line.startswith("Nthreads"):
            throughput = float(line.split(":")[3].split("\n")[0])
            if i<len(threads):
                time_1.append(throughput)
            else:
                time_2.append(throughput)
            i+=1
        line = fp.readline()
        
print("time1",time_1)
print("time2",time_2)

markers = ['x', 'o', '+', '*']
colors = ["royalblue", "red", "darkgreen", "pink", "orange"]
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

ax.plot(x_ticks, time_1, label=implementations[0], color=colors[0], marker=markers[0])

ax.plot(x_ticks, time_2, label=implementations[1], color=colors[1], marker=markers[1])

ax.legend(frameon=True)
# plt.title()
i=sys.argv[1].split("_")[1]
plt.savefig("plot_"+i+".png",bbox_inches="tight")