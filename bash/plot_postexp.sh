#!/bin/bash

for n in {0..20}; do
  python scripts/plot_postexp.py $n
done
