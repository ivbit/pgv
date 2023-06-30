#!/usr/bin/python3

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
    timestamp = parts[3]
    if caseid not in log:
        log[caseid] = []
    event = (task, user, timestamp)
    log[caseid].append(event)

f.close()

for caseid in log:
    for (task, user, timestamp) in log[caseid]:
        print(caseid, task, user, timestamp)

print("Sorted:")

for caseid in sorted(log.keys()):
    log[caseid].sort(key = lambda event: event[-1])
    for (task, user, timestamp) in log[caseid]:
        print(caseid, task, user, timestamp)

