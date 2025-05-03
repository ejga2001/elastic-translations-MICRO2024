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

from collections import Counter
from collections import OrderedDict

from ctypes import *


def main():
    
    BENCHMARKS = ["astar", "omnetpp", "streamcluster", "bfs", "canneal", "xsbench", "btree", "svm", "hashjoin", "gups"]
    BASE = "/home/enrique/CLionProjects/elastic-translations-MICRO2024"
    
    cycles = {}
    tlbmisses = {}

    pcycles = {}
    ptlbmisses = {}

    for bench in BENCHMARKS:
        pcycles[bench] = {}
        ptlbmisses[bench] = {}
        for t in ["4KiB", "THP", "mTHP", "Hawkeye", "ET", "ET-offline"]:
            pcycles[bench][t] = 0
            ptlbmisses[bench][t] = 0

    pdc = {}
    pdt = {}
    for frag in [50, 99]:
        for bench in BENCHMARKS:
            cycles[bench] = []
            tlbmisses[bench] = []

            # base
            if os.path.exists(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.base.tcmalloc-norelease.nokcompactd.1000ms/1"):
                file = open(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.base.tcmalloc-norelease.nokcompactd.1000ms/1", "r+")
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
                pcycles[bench]["4KiB"] = cycles[bench][-1]
                ptlbmisses[bench]["4KiB"] = tlbmisses[bench][-1]

            # THP
            if os.path.exists(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.thp.tcmalloc-norelease.nokcompactd.1000ms/1"):
                file = open(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.thp.tcmalloc-norelease.nokcompactd.1000ms/1", "r+")
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
                pcycles[bench]["THP"] = cycles[bench][-1]
                ptlbmisses[bench]["THP"] = tlbmisses[bench][-1]

            # mTHP
            if os.path.exists(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.thp-mthp.tcmalloc-norelease.nokcompactd.1000ms/1"):
                file = open(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.thp-mthp.tcmalloc-norelease.nokcompactd.1000ms/1", "r+")
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
                pcycles[bench]["mTHP"] = cycles[bench][-1]
                ptlbmisses[bench]["mTHP"] = tlbmisses[bench][-1]

            # Hawkeye
            if os.path.exists(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.thp.tcmalloc-norelease.1s.hwk.nokcompactd.1000ms/1"):
                file = open(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.thp.tcmalloc-norelease.1s.hwk.nokcompactd.1000ms/1", "r+")
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
                pcycles[bench]["Hawkeye"] = cycles[bench][-1]
                ptlbmisses[bench]["Hawkeye"] = tlbmisses[bench][-1]

            # ET greedy
            if os.path.exists(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.thp.tcmalloc-norelease.etheap.nokcompactd.1000ms.async-32m/1"):
                file = open(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.thp.tcmalloc-norelease.etheap.nokcompactd.1000ms.async-32m/1", "r+")
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
                pcycles[bench]["ET"] = cycles[bench][-1]
                ptlbmisses[bench]["ET"] = tlbmisses[bench][-1]

            # offline
            if os.path.exists(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.thp.tcmalloc-norelease.leshy.nokcompactd.1000ms/1"):
                file = open(f"{BASE}/results/host/eval/frag{frag}/{bench}.4KB.thp.tcmalloc-norelease.leshy.nokcompactd.1000ms/1", "r+")
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
                pcycles[bench]["ET-offline"] = cycles[bench][-1]
                ptlbmisses[bench]["ET-offline"] = tlbmisses[bench][-1]

        pdc[frag] = pd.DataFrame.from_dict(pcycles).T
        pdt[frag] = pd.DataFrame.from_dict(ptlbmisses).T

        pdc[frag].index = ['Astar', 'Omnetpp', 'Streamcluster', 'BFS', 'Canneal', 'XSBench', 'BTree', 'SVM', 'Hashjoin', 'Gups']
        pdt[frag].index = ['Astar', 'Omnetpp', 'Streamcluster', 'BFS', 'Canneal', 'XSBench', 'BTree', 'SVM', 'Hashjoin', 'Gups']

        pdc[frag].to_csv(f'./cycles-{frag}.csv')
        pdt[frag].to_csv(f'./tlbmisses-{frag}.csv')


if __name__ == "__main__":
    main()
