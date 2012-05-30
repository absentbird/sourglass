#!/usr/bin/env python
"""Log time tracking information."""

import os
import argparse
import time
import csv

# Parse arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-p', '--project', type=str, nargs=1, action='store', dest='project', help='The project name. Defaults to last project opened')
parser.add_argument('-m', '--memo', action='store_false', dest='update', help='Add a memo without changing the tracking status.')
parser.add_argument('-t', '--total', action='store_true', dest='total', help='Total up the hours worked on the project.')
parser.add_argument('-r', '--remove', type=int, nargs='?', const=1, action='store', dest='remove', help='Remove lines from the log starting with the most recent.')
parser.add_argument('-s', '--shift', type=str, nargs=1, action='store', dest='shift', help='Shift time by a number of minutes seconds or hours. Ex: Add 10 minutes t+10m remove one hour t-1h add 40 seconds t+40s.')
parser.add_argument('--audit', action='store_true', dest='audit', help='Print all memos and times on the log to the screen with a total.')
parser.add_argument('memo', metavar='m', type=str, nargs='?', default='', help='A memo of what was done')

arguments = parser.parse_args()

# Set basepath for file and create directories
basepath = os.path.expanduser('~')
basepath = os.path.join(basepath, '.sourglass')
print(basepath)
if not os.path.exists(os.path.join(basepath, 'logs')):
    os.makedirs(os.path.join(basepath, 'logs'))


def getLast():
    """Function to load the name and status of the last project accessed."""
    try:
        open(os.path.join(basepath, 'last'))
    except IOError:
        try:
            arguments.project
        except NameError:
            print("No current project. Start one with -p")
            exit()
        else:
            f = open(os.path.join(basepath, 'last'), 'w')
            f.write(arguments.project[0])
            f.close()
    store = open(os.path.join(basepath, 'last'), 'r')
    last = store.readline().rstrip('\n')
    last = [last, 's']
    store.close()
    path = getPath(last[0])
    with open(path, 'r') as log:
        reader = csv.reader(log)
        for row in reader:
            if row[1] == 'a' or row[1] == 's':
                line = row
    try:
        line
    except NameError:
        last[1] = 's'
    else:
        last[1] = line[1]
    return last


def getPath(project):
    """Fetch the file for the project. Prompt creation if none exists."""
    if project == '.sourglass':
        path = project
    else:
        path = os.path.join(basepath, 'logs', project + '.csv')
    try:
        open(path)
    except IOError:
        f = open(path, 'w')
        f.close()
        print("Started new project.")
        return path
    else:
        return path


def getStatus(last):
    """Invert the status unless flag was set."""
    if not arguments.update:
        return last[1]
    if last[1]:
        if last[1] == 'a':
            return 's'
        if last[1] == 's':
            return 'a'
    else:
        return 'a'


def recordLog(project, status, memo):
    """Write the entry to the log."""
    path = getPath(project)
    log = open(path, 'a')
    writer = csv.writer(log, lineterminator='\n')
    writer.writerow((time.time(), status, memo))
    log.close()
    if status == 'a':
        print("Tracking your time on " + project)
    if status == 's':
        print("Tracking suspended on " + project)
    if status == 't':
        print("Time shifted on " + project)
    if not path == '.sourglass':
        store = open(os.path.join(basepath, 'last'), 'w')
        store.write(project)
        store.close


def totalHours(path):
    """Total the hours on the project."""
    total = 0
    start = 0
    active = False
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[1] == 't':
                total += float(row[2])
            else:
                if active:
                    if row[1] == 's':
                        total += float(row[0]) - start
                        active = False
                else:
                    if row[1] == 'a':
                        start = float(row[0])
                        active = True
                        final = row
    if active:
        total += time.time() - float(final[0])
        active = False
    return "%.2f" % (total / 3600)

# Check for a local .sourglass log
try:
    open(os.path.join(os.getcwd(), '.sourglass'))
except IOError as e:
    last = getLast()
else:
    with open(os.getcwd() + '/.sourglass', 'r') as log:
        reader = csv.reader(log)
        for row in reader:
            if row[1] == 'a' or row[1] == 's':
                line = row
    try:
        line
    except NameError:
        last = ('.sourglass', 's')
    else:
        last = ('.sourglass', line[1])

# Check if a project flag was set
if arguments.project:
    if arguments.project[0] == last[0]:
        pass
    else:
        path = getPath(arguments.project[0])
        log = open(path, 'r')
        reader = csv.reader(log)
        for row in reader:
            if row[1] == 'a' or row[1] == 's':
                line = row
        try:
            line
        except NameError:
            last = (arguments.project[0], 's')
        else:
            last = (arguments.project[0], line[1])
        log.close()

# If an -t flag was set, total the hours.
if arguments.total:
    print(totalHours(getPath(last[0])))
    exit()

if arguments.remove:
    with open(getPath(last[0]), 'r') as log:
        lines = log.readlines()
        lines = lines[:-arguments.remove]
    with open(getPath(last[0]), 'w') as log:
        log.writelines([line for line in lines])
    exit()

if arguments.shift:
    shift = arguments.shift[0]
    increment = shift[-1]
    shift = shift[1:-1]
    if increment == 's':
        shift = float(shift)
    elif increment == 'm':
        shift = float(shift) * 60
    elif increment == 'h':
        shift = float(shift) * 3600
    else:
        exit(increment + " is not a supported increment. Please use s (seconds), m (minutes) or h (hours)")
    recordLog(last[0], 't', shift)
    exit()

if arguments.audit:
    print(last[0] + " Audit:\n")
    print("Time \t \t Action \t Memo")
    dashes = ''
    i = 0
    while i < 50:
        dashes += '-'
        i += 1
    print(dashes)
    with open(getPath(last[0]), 'r') as log:
        reader = csv.reader(log)
        for row in reader:
            row[0] = time.strftime("%b %d %H:%M", time.localtime(float(row[0])))
            if row[1] == 't':
                row[1] = 'Time Shifted'
                row[2] = float(row[2]) / 60
                if row[2] > 0:
                    row[2] = '+' + str(row[2]) + ' Minutes'
                else:
                    row[2] = str(row[2]) + ' Minutes'
            if row[1] == 'a':
                row[1] = 'Activated'
            if row[1] == 's':
                row[1] = 'Suspended'
            print(row[0] + '\t' + row[1] + '\t' + row[2])
    print("\nTotal Hours Logged: " + str(totalHours(getPath(last[0]))))
    exit()

# As long as no flags would stop an entry from being made, make one.
status = getStatus(last)
recordLog(last[0], status, arguments.memo)
