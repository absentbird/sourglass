import os
import argparse
import time
import csv

parser = argparse.ArgumentParser(description='Log time tracking information')
parser.add_argument('-p', '--project', type=str, nargs=1, action='store', dest='project', help='The project name. Defaults to last project opened')
parser.add_argument('-a', '--active', action='store_true', dest='status', help='Add a memo without changing the tracking status.')
parser.add_argument('-t', '--total', action='store_true', dest='total', help='Total up the time worked on the project.')
parser.add_argument('memo', metavar='m', type=str, nargs='?', default='', help='A memo of what was done')

arguments = parser.parse_args()

def getLast():
    store = open('~/.sourglass/last', 'r')
    last = store.readline().rstrip('\n').partition(' ')
    store.close()
    return last

def getProject(project):
    path = '~/.sourglass/logs/' + project + '.csv')
    try:
        open(path)
    except IOError as e:
        print "Project not found.", "Start new project?"
        exit()
    else:
        return path

def getStatus(last):
    if arguments.status:
        return 'a'
    if last[2]:
        if last[2] == 'a':
            return 's'
        if last[2] == 's':
            return 'a'

def recordLog(path, status, memo):
    log = open(path, 'a')
    writer = csv.writer(log, lineterminator='\n')
    writer.writerow((time.time(), status, memo))
    log.close()
    if status == 'a':
        print "Tracking your time."
    if status == 's':
        print "Tracking suspended."
    store = open('~/.sourglass/last', 'w')
    store.write(path+' '+status)
    store.close

last = getLast()

if arguments.project:
    if arguments.project[0] == last[0]:
        pass
    else:
        path = getProject(arguments.project[0])
        log = open(path, 'rb')
        reader = csv.reader(log)
        for row in reader:
            line = row
        last = (path, ' ', line[1])
        log.close()

if arguments.total:
    exit()

status = getStatus(last)
recordLog(last[0], status, arguments.memo)

