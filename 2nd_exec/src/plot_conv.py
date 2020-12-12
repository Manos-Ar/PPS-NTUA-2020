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

names = []
outDirs = []

comp_times = {}
conv_times = {}
total_times = {}

for arg in range(1,len(sys.argv)):
    outDir = sys.argv[arg]
    name = outDir.split("/")[1].split("_")[0]
    names.append(name)
    outDirs.append(outDir)

# print(outDirs)
# print(names)


for x in range(len(outDirs)):
    name = names[x]
    outDir = outDirs[x]

    comp_times[name] = []
    conv_times[name] = []
    total_times[name] = []

    for filename in os.listdir(outDir):
        if filename.startswith("Converged"):
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
                        conv = float(line.split("ConvergedTime")[1].split(" ")[1])
                        total = float(line.split("TotalTime")[1].split(" ")[1])

                        comp_times[name].append(comp)
                        conv_times[name].append(conv)
                        total_times[name].append(total)

                    line = fp.readline()

# print(comp_times)
# print(conv_times)
# print(total_times)

for name in names:
    comp_times[name] = round(mean(comp_times[name]), 6)
    conv_times[name] = round(mean(conv_times[name]), 6)
    total_times[name] = round(mean(total_times[name]), 6)

print(comp_times)
print(conv_times)
print(total_times,"\n")

markers = ['x', 'o', '+', '*']
colors = ["royalblue", "red", "darkgreen", "pink", "orange"]


## PLOT BAR PLOTS
x_Axis = np.array(names)
total_methods_val = []
comp_methods_val = []
conv_methods_val = []


for tuple_total, tuple_comp, tuple_conv in zip(total_times.items(), comp_times.items(), conv_times.items()):
    print (tuple_total)
    print (tuple_comp)
    print (tuple_conv)
    i = 0
    fig, ax = plt.subplots()
    print()

    total_methods_val.append(tuple_total[1])
    comp_methods_val.append(tuple_comp[1])
    conv_methods_val.append(tuple_conv[1])

# print (total_methods_val)
# print (comp_methods_val)
# print (conv_methods_val)

ax.set_facecolor('#f2f5f0')
ax.grid(True, linewidth=0.2)

br1 = np.arange(len(names))
br2 = [x + 0.3 for x in br1]
br3 = [x + 0.6 for x in br1]

line1 = plt.bar(br1, total_methods_val, label='Total', width=0.25, color = "#5975A4")
line2 = plt.bar(br2, comp_methods_val, label='Computation', width=0.25, color = "#CC8963")
line3 = plt.bar(br3, conv_methods_val, label='Converged', width=0.25, color = "#5F9E6E")

# Add the data value on head of the bar
for value in line1:
	height = value.get_height()
	ax.text(value.get_x() + value.get_width()/2., 1.002*height,'%f' % height, ha='center', va='bottom', fontsize='xx-small', fontweight='300')
for value in line2:
	height = value.get_height()
	ax.text(value.get_x() + value.get_width()/2., 1.002*height,'%f' % height, ha='center', va='bottom', fontsize='xx-small', fontweight='300')
for value in line3:
	height = value.get_height()
	ax.text(value.get_x() + value.get_width()/2., 1.002*height,'%f' % height, ha='center', va='bottom', fontsize='xx-small', fontweight='300')


plt.xlabel("Methods")
plt.ylabel("Time (s)")
plt.xticks([r + 0.15 for r in range(len(names))], names, rotation=0)
plt.title("Times for each Method Converged")
plt.legend()
plt.savefig("plot_conv_times.png",bbox_inches="tight")
