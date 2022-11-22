#!/bin/bash
for y in 2017 2018 2019 2020 2021; do
  echo -n "$y	"
  grep "^us " awstats??$y.packages.ros.org.txt | awk {'print $3'} | awk '{s+=$1} END {print s}'
done


