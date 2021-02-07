#!/bin/python3
from itertools import islice
import sys

implementations=[]
for i in range(1,len(sys.argv)):
    implementations.append(sys.argv[i])

print(implementations)
N=14
# fine_grain=sys.argv[1]
# optimistic=sys.argv[2]
# lazy=sys.argv[3]
# no_blocking=sys.argv[4]
# implementations=[fine_grain, optimistic, lazy, no_blocking]

metric=open("metrics.txt","w")


for i in range(1,5):
    for filename in implementations:
        with open(filename, 'r') as infile:
            lines_gen = islice(infile, (i-1)*N,i*N)
            for line in lines_gen:
                metric.write(line)