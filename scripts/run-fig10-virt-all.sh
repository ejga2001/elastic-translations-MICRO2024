#!/bin/bash

RUNS="baseline et hwk"
for run in ${RUNS}; do
  RUN=${run} run-fig10-virt.sh
done