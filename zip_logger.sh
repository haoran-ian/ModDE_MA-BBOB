#!/bin/bash

for i in {0..49}; do
  for n in {0..20}; do
    var=`expr 50 \* $n`
    index=`expr $var + $i`
    zip -r logger-zip/L-SHADE_sat_${i}_${index}.zip logger/L-SHADE_sat_${i}_${index}/
  done
done
