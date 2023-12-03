#!/bin/bash

for n in {0..20}; do
  for i in {0..49}; do
    python src.py -n=$n -i=$i -b=saturate
  done
done
