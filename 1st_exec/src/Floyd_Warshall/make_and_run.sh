#!/bin/bash

if [ -f make_on_queue.sh.o* ] || [ -f make_on_queue.e* ]; then
  rm make_on_queue.sh.*
fi

eval "qsub -q parlab make_on_queue.sh"
echo "compiling"
while [ ! -f make_on_queue.sh.e* ]
do
  sleep 1
  echo -n "."
done
echo
echo "compiled"

if [ -s make_on_queue.sh.e* ];  then
  echo "error compiling"
  exit 1
else
  rm make_on_queue.sh.*
fi

eval "qsub -q serial -l nodes=sandman:ppn=64 run_on_queue.sh"
