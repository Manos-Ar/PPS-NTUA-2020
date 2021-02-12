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

implementations = ["naive", "coalesced_A", "reduced_global", "cublas"]
dimensions = [256, 512, 1024, 2048]
blocks = {}
performances = {}

for i in implementations:
    blocks[i] = 0
    performances[i] = {}
    for m in dimensions:
        performances[i][m] = {}
        for n in dimensions:
            performances[i][m][n] = {}
            for k in dimensions:
                performances[i][m][n][k] = 0.0

# print("blocks:", blocks)
# print("performances:", performances)

########## Read Metrics ##########

with open(sys.argv[1], 'r') as fp:
    line = fp.readline()
    i = 0
    while line:
        if line.startswith("Adjusted dimension M:"):
            M_dim = int(line.split(":")[1])
            line = fp.readline()
            while not line.startswith(">>>> End"):
                if line.startswith("Adjusted dimension N:"):
                    N_dim = int(line.split(":")[1])

                if line.startswith("Adjusted dimension K:"):
                    K_dim = int(line.split(":")[1])

                if line.startswith("Block dimensions:"):
                    # print(line)
                    block_dims = int(line.split(":")[1].split("x")[0])

                if line.startswith("GPU kernel version:"):
                    # print(line)
                    implem = line.split(":")[1].split(" ")[1].split("\n")[0]
                    blocks[implem] = block_dims

                if line.startswith("Performance:"):
                    # print(line)
                    perform = float(line.split(":")[1].split(" ")[2])
                    # performances[implem][M_dim].append(perform)
                    performances[implem][M_dim][N_dim][K_dim] = perform

                line = fp.readline()
        line = fp.readline()

# print("blocks:", blocks)
# print("performances:", performances)

# Print performances Dictionary
# for implem, m_n_k_perform in performances.items():
#     print("------------------------------------------------------------")
#     print("Kernel Implem.:", implem)
#     for m, n_k_perform in m_n_k_perform.items():
#         print("\tM =", m)
#         for n, k_perform in n_k_perform.items():
#             print("\t\tN =", n)
#             for k, perform in k_perform.items():
#                 print("\t\t\tK =", k)
#                 print("\t\t\t\tPerformance:", perform)


########## 1st Plot ##########

# Create list with all dimension compinations
dimensions_M = {}

for m in dimensions:
    dimensions_M[m] = []
    for n in dimensions:
        for k in dimensions:
            dimensions_M[m].append(str(m)+"-"+str(n)+"-"+str(k))
print()
print("dimensions_M:", dimensions_M)

# Save performance results for plotting per implementation, M size
performances_implem_M = {}

for i in implementations:
    performances_implem_M[i] = {}
    for m in dimensions:
        performances_implem_M[i][m] = []

for implem, m_n_k_perform in performances.items():
    for m, n_k_perform in m_n_k_perform.items():
        for n, k_perform in n_k_perform.items():
            for k, perform in k_perform.items():
                performances_implem_M[implem][m].append(perform)
print()
print("performances_implem_M:", performances_implem_M)


markers = ['x', 'o', '+', '*', "s", "v"]
colors = ["royalblue", "red", "darkgreen", "pink", "orange", "brown"]

# Plot different plots per implementation, M size
i = 0
for implem in implementations:
    for m in dimensions:
        x_Axis = np.array(dimensions_M[m])
        x_ticks = np.arange(0, len(x_Axis), 1)

        fig, ax = plt.subplots()
        ax.grid(True)
        ax.set_facecolor('#f2f5f0')
        ax.set_xlabel("M-N-K")
        ax.set_ylabel("Performance ($Gflop/s$)")
        ax.set_xlim(-0.5, len(x_Axis) - 0.5)
        ax.xaxis.set_ticks(x_ticks)
        ax.set_xticklabels(x_Axis, rotation=40)

        ax.plot(x_ticks, performances_implem_M[implem][m], label=implem,
                color=colors[i % len(colors)], marker=markers[i % len(markers)])
        ax.legend(frameon=True)
        plt.title(implem + " Kernel - M=" + str(m) +
                  " - Block Size=" + str(blocks[implem]) + "x" + str(blocks[implem]))
        plt.savefig("plot_2_"+implem+"_"+str(m)+".png", bbox_inches="tight")
    i += 1


########## 2nd Plot ##########

# Save performance results for plotting per M size
performances_M = {}

for m in dimensions:
    performances_M[m] = {}
    for implem in implementations:
        performances_M[m][implem] = []
# print()
# print("performances_M:", performances_M)

for implem, m_n_k_perform in performances.items():
    for m, n_k_perform in m_n_k_perform.items():
        for n, k_perform in n_k_perform.items():
            for k, perform in k_perform.items():
                performances_M[m][implem].append(perform)
print()
print("performances_M:", performances_M)


# Plot different plots per M size (for all implementations)
for m in dimensions:
    x_Axis = np.array(dimensions_M[m])
    x_ticks = np.arange(0, len(x_Axis), 1)

    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_facecolor('#f2f5f0')
    ax.set_xlabel("M-N-K")
    ax.set_ylabel("Performance ($Gflop/s$)")
    ax.set_xlim(-0.5, len(x_Axis) - 0.5)
    ax.xaxis.set_ticks(x_ticks)
    ax.set_xticklabels(x_Axis, rotation=40)

    i = 0
    for implem in implementations:
        ax.plot(x_ticks, performances_M[m][implem], label=implem,
                color=colors[i % len(colors)], marker=markers[i % len(markers)])
        i += 1

    ax.legend(frameon=True)
    plt.title("Kernel Implementations - M=" + str(m))
    plt.savefig("plot_2_"+str(m)+".png", bbox_inches="tight")
