import os
from sys import argv
import argparse
import time
import csv

# Parse arguments
parser = argparse.ArgumentParser(description='Log time tracking information')
parser.add_argument('-p', '--project', type=str, nargs=1, action='store', dest='project', help='The project name. Defaults to last project opened')
parser.add_argument('-m', '--memo', action='store_false', dest='update', help='Add a memo without changing the tracking status.')
parser.add_argument('-t', '--total', action='store_true', dest='total', help='Total up the hours worked on the project.')
parser.add_argument('-r', '--remove', type=int, nargs='?', const=1, action='store', dest='remove', help='Remove lines from the log starting with the most recent.')
parser.add_argument('-s', '--shift', type=int, nargs='1', action='store', dest='shift', help='Shift time by a number of minutes seconds or hours. Notation is (+|-)n(s|m|h) Examples: Add 10 minutes "+10m". Remove one hour "-1h". Add 40 seconds would be "+40s".')
parser.add_argument('--audit', action='store_true', dest='audit', help='Print all memos and times on the log to the screen with a total.')
parser.add_argument('memo', metavar='m', type=str, nargs='?', default='', help='A memo of what was done')

arguments = parser.parse_args()

# Set basepath for file and create directories
basepath = os.path.expanduser('~/.sourglass/')
if not os.path.exists(basepath+'logs'):
    os.makedirs(basepath+'logs')

# Function to load the name and status of the last project accessed
def getLast():
    store = open(basepath + 'last', 'r')
    last = store.readline().rstrip('\n').partition(' ')
    store.close()
    return last

# Fetch the file for the project. Prompt creation if none exists.
def getPath(project):
    if project == '.sourglass':
        return project
    path = basepath + 'logs/' + project + '.csv'
    try:
        open(path)
    except IOError as e:
        print "Start new project?"
        new = raw_input('y/n > ')
        if new == 'y':
            f = open(path, 'w')
            f.close()
            return path
        else:
            exit()
    else:
        return path

# Invert the status unless flag was set
def getStatus(last):
    if not arguments.update:
        return last[2]
    if last[2]:
        if last[2] == 'a':
            return 's'
        if last[2] == 's':
            return 'a'
    else:
        return 'a'

# Write the entry to the log
def recordLog(project, status, memo):
    path = getPath(project)
    log = open(path, 'a')
    writer = csv.writer(log, lineterminator='\n')
    writer.writerow((time.time(), status, memo))
    log.close()
    if status == 'a':
        print "Tracking your time."
    if status == 's':
        print "Tracking suspended."
    store = open(basepath + 'last', 'w')
    store.write(project+' '+status)
    store.close

# Total the hours on the project
def totalHours(path):
    total = 0
    start = 0
    active = False
    with open(path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            final = row
            if active:
                if row[1] == 's':
                    total += float(row[0]) - start
                    active = False
            else:
                if row[1] == 'a':
                    start = float(row[0])
                    active = True
    if active and final[1] == 'a':
        total += time.time() - float(final[0])
        active = False
    return total / 3600

# Check for a local .sourglass log
try:
    open(os.getcwd() + '/.sourglass')
except IOError as e:
    last = getLast()
else:
    with open(os.getcwd() + '/.sourglass', 'rb') as log:
        reader = csv.reader(log)
        for row in reader:
            line = row
    try: 
        line
    except NameError:
        last = ('.sourglass', ' ', 's')
    else:
        last = ('.sourglass', ' ', line[1])

# Check if a project flag was set
if arguments.project:
    if arguments.project[0] == last[0]:
        pass
    else:
        path = getPath(arguments.project[0])
        log = open(path, 'rb')
        reader = csv.reader(log)
        for row in reader:
            line = row
        last = (arguments.project[0], ' ', line[1])
        log.close()

# If an -t flag was set, total the hours.
if arguments.total:
    print totalHours(getPath(last[0]))
    exit()

if arguments.remove:
    with open(getPath(last[0]), 'r') as log:
        lines = log.readlines()
        lines = lines[:-arguments.remove]
    with open(getPath(last[0]), 'w') as log:
        log.writelines([line for line in lines])
    exit()

if arguments.shift:
    exit() 

if arguments.audit:
    exit()

# As long as no flags would stop an entry from being made, make one.
status = getStatus(last)
recordLog(last[0], status, arguments.memo)
