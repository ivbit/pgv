#!/usr/bin/python3

# Listing 36

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

import matplotlib.pyplot as plt

X = dict()
Y = dict()
caseids = sorted(log.keys(), key=lambda caseid: log[caseid][-1][-1]-log[caseid][0][-1])

for (y, caseid) in enumerate(caseids):
    x0 = log[caseid][0][-1]
    for i in range(0, len(log[caseid])):
        (a, _, x) = log[caseid][i]
        if a not in X:
            X[a] = []
            Y[a] = []
            X[a].append((x-x0).total_seconds()/(24*3600))
            Y[a].append(y)

for a in sorted(X.keys()):
    plt.plot(X[a], Y[a], 'o', label=a, markersize=20, markeredgewidth=0.0, alpha=0.5)

axes = plt.gca()

axes.set_yticks(range(len(caseids)))
axes.set_ylim(-1, len(caseids))
axes.set_yticklabels(caseids)
axes.set_ylabel('case id')
axes.invert_yaxis()

axes.set_xlabel('days')
axes.xaxis.tick_top()
axes.xaxis.set_label_position('top')

plt.grid(True)
plt.legend(numpoints=1)
plt.tight_layout()
plt.show()

