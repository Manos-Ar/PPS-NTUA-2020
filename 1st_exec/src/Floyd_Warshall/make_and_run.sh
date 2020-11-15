#!/bin/bash

eval "qsub -q serial -l nodes=sandman:ppn=64 make_on_queue.sh"
echo "compiling"
while [ ! -f make_on_queue.sh.* ]
do
  sleep 1
  echo -n "."
done
echo
echo "compiled"

if [ -s make_on_queue.sh.e* ];  then
  echo "error compiling"
  exit 1
fi

eval "qsub -q serial -l nodes=sandman:ppn=64 run_on_queue.sh"
