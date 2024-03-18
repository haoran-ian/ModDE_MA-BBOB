#!/bin/bash

for n in {0..20}; do
  python scripts/create_postexp.py $n
done
