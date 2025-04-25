#!/bin/bash

MY_BENCHMARKS="astar omnetpp streamcluster hashjoin svm canneal"

for BENCHMARKS in ${MY_BENCHMARKS}; do
  export BENCHMARKS
  ./scripts/run-fig2-hugetlb.sh
done