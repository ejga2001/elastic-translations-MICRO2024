#!/bin/bash

MY_BENCHMARKS="astar omnetpp streamcluster hashjoin svm canneal xsbench bfs gups btree"

for BENCHMARKS in ${MY_BENCHMARKS}; do
  export BENCHMARKS
  ./scripts/run-fig10-virt.sh
done