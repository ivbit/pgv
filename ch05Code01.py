#!/usr/bin/python3

# Listings 41
# Parsing a XES event log with ElementTree

import datetime
import xml.etree.ElementTree as ET

# The bpic2012Log.xes is 71 MiB, the zipped version is 3.6 MiB.
# ch05Code02.py is modified to use the zipped version instead.
tree = ET.parse('bpic2012Log.xes')
root = tree.getroot()

ns = {'xes': 'http://www.xes-standard.org/'}

for trace in root.findall('xes:trace', ns):
    caseid = ''
    for string in trace.findall('xes:string', ns):
        if string.attrib['key'] == 'concept:name':
            caseid = string.attrib['value']
    for event in trace.findall('xes:event', ns):
        task = ''
        user = ''
        event_type = ''
        for string in event.findall('xes:string', ns):
            if string.attrib['key'] == 'concept:name':
                task = string.attrib['value']
            if string.attrib['key'] == 'org:resource':
                user = string.attrib['value']
            if string.attrib['key'] == 'lifecycle:transition':
                event_type = string.attrib['value']
            timestamp = ''
            for date in event.findall('xes:date', ns):
                if date.attrib['key'] == 'time:timestamp':
                    timestamp = date.attrib['value']
                    timestamp = datetime.datetime.strptime(timestamp[:-10], '%Y-%m-%dT%H:%M:%S')

            print(';'.join([caseid, task, event_type, user, str(timestamp)]))

# Output is 34 MiB of text in CSV format.
# It can be redirected to a file.
# > bpic2012Log.csv ./ch05Code01.py

