#!/bin/bash
DIR_PLOTS="plots"
DIR_METRICS=metrics
implementations=( "fw" "fw_sr" "fw_tiled" )

if [ ! -d "${DIR_PLOTS}" ]; then
	mkdir ${DIR_PLOTS}
fi

for implementation in "${implementations[@]}";
do
  # Check if plots dirs exists, and delete them
  if [ -d "${DIR_PLOTS}/${implementation}" ]; then
  	rm -rf "${DIR_PLOTS}/${implementation}"
  	mkdir "${DIR_PLOTS}/${implementation}"
  else
  	mkdir "${DIR_PLOTS}/${implementation}"
  fi

  # Make plots
  if [ ${implementation} == "fw" ]; then
    eval "./plot_metrics_fw.py ${DIR_METRICS}/${implementation}/metrics_fw.txt"
  else
    eval "./plot_metrics.py ${DIR_METRICS}/${implementation}"
  fi
  mv plot_speedup*.png "${DIR_PLOTS}/${implementation}"
  mv plot_time*.png "${DIR_PLOTS}/${implementation}"

done
