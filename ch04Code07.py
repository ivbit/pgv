#!/usr/bin/python3

# Listing 37

import datetime

f = open('eventlog.csv', 'r')

log = dict()

for line in f:
    line = line.strip()
    if len(line) == 0:
        continue
    parts = line.split(';')
    caseid = parts[0]
    task = parts[1]
    user = parts[2]
    timestamp = datetime.datetime.strptime(parts[3], '%Y-%m-%d %H:%M:%S')
    if caseid not in log:
        log[caseid] = []
    event = (task, user, timestamp)
    log[caseid].append(event)

f.close()

import numpy as np
import matplotlib.pyplot as plt

D = dict()

for caseid in log:
    for i in range(0, len(log[caseid])):
        (a, _, t) = log[caseid][i]
        if i > 0:
            (_, _, t0) = log[caseid][i-1]
            d = (t-t0).total_seconds()/(24*3600)
        else:
            d = 0.0
        if a not in D:
            D[a] = []
        D[a].append(d)

nrows = 4
ncols = 2

fig, ax = plt.subplots(nrows, ncols)

i = 0
j = 0
for a in sorted(D.keys()):
    print('%s: mean=%.2f std=%.2f days' % (a, np.mean(D[a]), np.std(D[a])))
    ax[i,j].hist(D[a], bins=[0.1*k for k in range(100)])
    ax[i,j].set_title(a)
    ax[i,j].set_xticks(range(10))
    ax[i,j].grid(True)
    if i == nrows-1:
        ax[i,j].set_xlabel('days')
    j += 1
    if j == ncols:
        i += 1
        j = 0

plt.tight_layout()
plt.show()

# Output of this script:
# a: mean=0.00 std=0.00 days
# b: mean=1.92 std=1.67 days
# c: mean=1.20 std=0.00 days
# d: mean=1.03 std=0.00 days
# e: mean=0.65 std=0.31 days
# f: mean=1.29 std=0.49 days
# g: mean=4.73 std=0.51 days
# h: mean=2.51 std=1.61 days

