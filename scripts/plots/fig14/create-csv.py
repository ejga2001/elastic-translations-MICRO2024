#!/usr/bin/env python

import itertools
import os
import sys
import subprocess
import shlex

import numpy as np
import pandas as pd
import seaborn as sns

import statistics
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from collections import Counter, OrderedDict
from ctypes import *

def main():
    cycles = {}
    tlbmisses = {}

    pcycles = {}
    ptlbmisses = {}

    BASE = "/home/enrique/CLionProjects/elastic-translations-MICRO2024"

    mixes = [['xsbench', 'hashjoin'],
             ['astar', 'btree', 'gups'],
             ['omnetpp', 'svm', 'bfs', 'gups']]

    pdc = {}
    pdt = {}
    for idx, mix in enumerate(mixes):
        for bench in mix:
            pcycles[(idx, bench)] = {}
            ptlbmisses[(idx, bench)] = {}
            for t in ["4KiB", "THP", "ET"]:
                pcycles[(idx, bench)][t] = 0
                ptlbmisses[(idx, bench)][t] = 0

        for bench in mix:
            cycles[bench] = []
            tlbmisses[bench] = []

            # base
            if os.path.exists(BASE + f"/results/host/multi/{bench}.4KB.base.tcmalloc-norelease.nokcompactd.1000ms/1"):
                with open(BASE + f"/results/host/multi/{bench}.4KB.base.tcmalloc-norelease.nokcompactd.1000ms/1", "r") as file:
                    for line in file.readlines():
                        if bench in ["omnetpp", "astar"]:
                            if "cycles" in line and "numactl" not in line:
                                cycles[bench].append(int(line.split()[0]))
                            if "dtlb_walk" in line and "numactl" not in line:
                                tlbmisses[bench].append(int(line.split()[0]))
                        else:
                            if "cycles:" in line:
                                cycles[bench].append(int(line.split(":")[1]))
                            if "dtlb_walk:" in line:
                                tlbmisses[bench].append(int(line.split(":")[1]))
                pcycles[(idx, bench)]["4KiB"] = cycles[bench][-1]
                ptlbmisses[(idx, bench)]["4KiB"] = tlbmisses[bench][-1]

            # THP
            if os.path.exists(BASE + f"/results/host/multi/{bench}.4KB.thp.tcmalloc-norelease.nokcompactd.1000ms/1"):
                with open(BASE + f"/results/host/multi/{bench}.4KB.thp.tcmalloc-norelease.nokcompactd.1000ms/1", "r") as file:
                    for line in file.readlines():
                        if bench in ["omnetpp", "astar"]:
                            if "cycles" in line and "numactl" not in line:
                                cycles[bench].append(int(line.split()[0]))
                            if "dtlb_walk" in line and "numactl" not in line:
                                tlbmisses[bench].append(int(line.split()[0]))
                        else:
                            if "cycles:" in line:
                                cycles[bench].append(int(line.split(":")[1]))
                            if "dtlb_walk:" in line:
                                tlbmisses[bench].append(int(line.split(":")[1]))
                    pcycles[(idx, bench)]["THP"] = cycles[bench][-1]
                    ptlbmisses[(idx, bench)]["THP"] = tlbmisses[bench][-1]

            # ET greedy
            if os.path.exists(BASE + f"/results/host/multi/{bench}.4KB.thp.tcmalloc-norelease.etheap.nokcompactd.1000ms.async-32m/1"):
                with open(BASE + f"/results/host/multi/{bench}.4KB.thp.tcmalloc-norelease.etheap.nokcompactd.1000ms.async-32m/1", "r") as file:
                    for line in file.readlines():
                        if bench in ["omnetpp", "astar"]:
                            if "cycles" in line and "numactl" not in line:
                                cycles[bench].append(int(line.split()[0]))
                            if "dtlb_walk" in line and "numactl" not in line:
                                tlbmisses[bench].append(int(line.split()[0]))
                        else:
                            if "cycles:" in line:
                                cycles[bench].append(int(line.split(":")[1]))
                            if "dtlb_walk:" in line:
                                tlbmisses[bench].append(int(line.split(":")[1]))
                pcycles[(idx, bench)]["ET"] = cycles[bench][-1]
                ptlbmisses[(idx, bench)]["ET"] = tlbmisses[bench][-1]

    pdc = pd.DataFrame.from_dict(pcycles).T
    pdt = pd.DataFrame.from_dict(ptlbmisses).T

    pdc.index = [(1, 'XSBench'), (1, 'Hashjoin'),
                 (2, 'Astar'), (2, 'BTree'), (2, 'Gups'),
                 (3, 'Omnetpp'), (3, 'SVM'), (3, 'BFS'), (3, 'Gups')]
    pdt.index = [(1, 'XSBench'), (1, 'Hashjoin'),
                 (2, 'Astar'), (2, 'BTree'), (2, 'Gups'),
                 (3, 'Omnetpp'), (3, 'SVM'), (3, 'BFS'), (3, 'Gups')]

    pdc.to_csv('./cycles.csv')
    pdt.to_csv('./tlbmisses.csv')

if __name__ == "__main__":
    main()
