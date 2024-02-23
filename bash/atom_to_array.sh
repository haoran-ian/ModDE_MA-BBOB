#!/bin/bash

for i in {0..7}; do
  for j in {1..25}; do
    python scripts/atom_to_array.py $i $j
  done
done
