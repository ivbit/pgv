#!/usr/bin/python3

# Listing 32

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

D = dict()
for caseid in log:
    for i in range(0, len(log[caseid])-1):
        (ai, _, ti) = log[caseid][i]
        (aj, _, tj) = log[caseid][i+1]
        if ai not in D:
            D[ai] = dict()
        if aj not in D[ai]:
            D[ai][aj] = []
        D[ai][aj].append(tj-ti)

for ai in sorted(D.keys()):
    for aj in sorted(D[ai].keys()):
        sum_td = sum(D[ai][aj], datetime.timedelta(0))
        count_td = len(D[ai][aj])
        avg_td = sum_td/count_td
        avg_td -= datetime.timedelta(microseconds=avg_td.microseconds)
        D[ai][aj] = avg_td

import pygraphviz as pgv

G = pgv.AGraph(strict=False, directed=True)

G.graph_attr['rankdir'] = 'TB'
G.node_attr['shape'] = 'box'

values = [D[ai][aj].total_seconds() for ai in D for aj in D[ai]]
x_min = min(values)
x_max = max(values)

y_min = 1.0
y_max = 5.0

for ai in D:
    for aj in D[ai]:
        x = D[ai][aj].total_seconds()
        y = y_min + (y_max-y_min) * float(x-x_min) / float(x_max-x_min)
        G.add_edge(ai, aj, label=D[ai][aj], penwidth=y)

print(G.string())

G.draw('graph.png', prog='dot')

