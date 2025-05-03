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
    cycles = {}
    tlbmisses = {}

    pcycles = {}
    ptlbmisses = {}

    BASE = "/home/enrique/CLionProjects/elastic-translations-MICRO2024"

    for bench in ["streamcluster","astar", "omnetpp", "bfs", "canneal", "xsbench", "btree", "svm", "hashjoin"]:
        pcycles[bench] = {}
        ptlbmisses[bench] = {}
        for t in ["4KiB", "THP", "mTHP", "Hawkeye", "ET", "ET-offline"]:
            pcycles[bench][t] = 0
            ptlbmisses[bench][t] = 0

    pages = {}

    for bench in ["streamcluster","astar", "omnetpp", "bfs", "canneal", "xsbench", "btree", "svm", "hashjoin", "gups"]:
        pages = {}

        # base
        pages["4KiB"] = {}
        if os.path.exists(BASE + "/results/host/eval/frag0/%s.4KB.base.tcmalloc-norelease.nokcompactd.1000ms/1" % (bench)):
            file = open(BASE + "/results/host/eval/frag0/%s.4KB.base.tcmalloc-norelease.nokcompactd.1000ms/1" % (bench), "r+")
            for line in file.readlines():
                if "Anon 4K:" in line:
                    pages["4KiB"]["4KiB"] = int(line.split()[2])
                    pages["4KiB"]["64KiB"] = int(line.split()[5])
                    pages["4KiB"]["2MiB"] = int(line.split()[8])
                    pages["4KiB"]["32MiB"] = int(line.split()[11])
                    break

        # THP
        pages["THP"] = {}
        if os.path.exists(BASE + "/results/host/eval/frag0/%s.4KB.thp.tcmalloc-norelease.nokcompactd.1000ms/1" % (bench)):
            file = open(BASE + "/results/host/eval/frag0/%s.4KB.thp.tcmalloc-norelease.nokcompactd.1000ms/1" % (bench), "r+")
            for line in file.readlines():
                if "Anon 4K:" in line:
                    pages["THP"]["4KiB"] = int(line.split()[2])
                    pages["THP"]["64KiB"] = int(line.split()[5])
                    pages["THP"]["2MiB"] = int(line.split()[8])
                    pages["THP"]["32MiB"] = int(line.split()[11])
                    break

        # mTHP
        pages["mTHP"] = {}
        if os.path.exists(BASE + "/results/host/eval/frag0/%s.4KB.thp-mthp.tcmalloc-norelease.nokcompactd.1000ms/1" % (bench)):
            file = open(BASE + "/results/host/eval/frag0/%s.4KB.thp-mthp.tcmalloc-norelease.nokcompactd.1000ms/1" % (bench), "r+")
            for line in file.readlines():
                if "Anon 4K:" in line:
                    pages["mTHP"]["4KiB"] = int(line.split()[2])
                    pages["mTHP"]["64KiB"] = int(line.split()[5])
                    pages["mTHP"]["2MiB"] = int(line.split()[8])
                    pages["mTHP"]["32MiB"] = int(line.split()[11])
                    break

        # Hawkeye
        pages["Hawkeye"] = {}
        if os.path.exists(BASE + "/results/host/eval/frag0/%s.4KB.thp.tcmalloc-norelease.1s.hwk.nokcompactd.1000ms/1" % (bench)):
            file = open(BASE + "/results/host/eval/frag0/%s.4KB.thp.tcmalloc-norelease.1s.hwk.nokcompactd.1000ms/1" % (bench), "r+")
            for line in file.readlines():
                if "Anon 4K:" in line:
                    pages["Hawkeye"]["4KiB"] = int(line.split()[2])
                    pages["Hawkeye"]["64KiB"] = int(line.split()[5])
                    pages["Hawkeye"]["2MiB"] = int(line.split()[8])
                    pages["Hawkeye"]["32MiB"] = int(line.split()[11])
                    break

        # ET greedy
        pages["ET"] = {}
        if os.path.exists(BASE + "/results/host/eval/frag0/%s.4KB.thp.tcmalloc-norelease.etheap.nokcompactd.1000ms.async-32m/1" % (bench)):
            file = open(BASE + "/results/host/eval/frag0/%s.4KB.thp.tcmalloc-norelease.etheap.nokcompactd.1000ms.async-32m/1" % (bench), "r+")
            for line in file.readlines():
                if "Anon 4K:" in line:
                    pages["ET"]["4KiB"] = int(line.split()[2])
                    pages["ET"]["64KiB"] = int(line.split()[5])
                    pages["ET"]["2MiB"] = int(line.split()[8])
                    pages["ET"]["32MiB"] = int(line.split()[11])
                    break

        # ET offline
        pages["ET-Offline"] = {}
        if os.path.exists(BASE + "/results/host/eval/frag0/%s.4KB.thp.tcmalloc-norelease.leshy.nokcompactd.1000ms/1" % (bench)):
            file = open(BASE + "/results/host/eval/frag0/%s.4KB.thp.tcmalloc-norelease.leshy.nokcompactd.1000ms/1" % (bench), "r+")
            for line in file.readlines():
                if "Anon 4K:" in line:
                    pages["ET-Offline"]["4KiB"] = int(line.split()[2])
                    pages["ET-Offline"]["64KiB"] = int(line.split()[5])
                    pages["ET-Offline"]["2MiB"] = int(line.split()[8])
                    pages["ET-Offline"]["32MiB"] = int(line.split()[11])
                    break

        paged = pd.DataFrame.from_dict(pages).T
        paged.to_csv('./%s.csv' % bench)

if __name__ == "__main__":
    main()
