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

BASE="/home/enrique/CLionProjects/elastic-translations-MICRO2024"

for type in ["host", "vm"]:
    cycles = {}
    pcycles = {}

    for bench in ["astar", "omnetpp", "streamcluster", "canneal", "svm", "hashjoin"]:
        pcycles[bench] = {}
        for t in ["4KiB", "64KiB", "2MiB", "32MiB"]:
            pcycles[bench][t] = 0

    pdc={}
    for bench in ["astar", "omnetpp", "streamcluster", "canneal", "svm", "hashjoin"]:
        cycles[bench] = []

        #base
        if os.path.exists(BASE + "/results/" + type + "/fig2/%s.4KB.base.tcmalloc-norelease/1"%(bench)):
            file = open(BASE + "/results/" + type + "/fig2/%s.4KB.base.tcmalloc-norelease/1"%( bench),"r+")
            for line in file.readlines():
                if bench in ["omnetpp", "astar"]:
                    if "cycles" in line and "numactl" not in line:
                        cycles[bench].append(int(line.split()[0]))
                else:
                    if "cycles:" in line:
                        cycles[bench].append(int(line.split(":")[1]))
            pcycles[bench]["4KiB"] = cycles[bench][-1]


        #hptec
        if os.path.exists(BASE + "/results/" + type + "/fig2/%s.4KB.hptec.tcmalloc-norelease/1"%(bench)):
            file = open(BASE + "/results/" + type + "/fig2/%s.4KB.hptec.tcmalloc-norelease/1"%( bench),"r+")
            for line in file.readlines():
                if bench in ["omnetpp", "astar"]:
                    if "cycles" in line and "numactl" not in line:
                        cycles[bench].append(int(line.split()[0]))
                else:
                    if "cycles:" in line:
                        cycles[bench].append(int(line.split(":")[1]))
            pcycles[bench]["64KiB"] = cycles[bench][-1]


        #hpmd
        if os.path.exists(BASE + "/results/" + type + "/fig2/%s.4KB.hpmd.tcmalloc-norelease/1"%(bench)):
            file = open(BASE + "/results/" + type + "/fig2/%s.4KB.hpmd.tcmalloc-norelease/1"%( bench),"r+")
            for line in file.readlines():
                if bench in ["omnetpp", "astar"]:
                    if "cycles" in line and "numactl" not in line:
                        cycles[bench].append(int(line.split()[0]))
                else:
                    if "cycles:" in line:
                        cycles[bench].append(int(line.split(":")[1]))
            pcycles[bench]["2MiB"] = cycles[bench][-1]

        #hpmdc
        if os.path.exists(BASE + "/results/" + type + "/fig2/%s.4KB.hpmdc.tcmalloc-norelease/1"%(bench)):
            file = open(BASE + "/results/" + type + "/fig2/%s.4KB.hpmdc.tcmalloc-norelease/1"%( bench),"r+")
            for line in file.readlines():
                if bench in ["omnetpp", "astar"]:
                    if "cycles" in line and "numactl" not in line:
                        cycles[bench].append(int(line.split()[0]))
                else:
                    if "cycles:" in line:
                        cycles[bench].append(int(line.split(":")[1]))
            pcycles[bench]["32MiB"] = cycles[bench][-1]

    pdc=pd.DataFrame.from_dict(pcycles).T

    pdc.index=['Astar', 'Omnetpp', 'Streamcluster', 'Canneal', 'SVM', 'Hashjoin']
    pdc.to_csv('./cycles.' + type + '.csv')
