import os
import argparse
import time
import csv

parser = argparse.ArgumentParser(description='Log time tracking information')
parser.add_argument('-p', '--project', type=str, nargs=1, action='store', dest='project', help='The project name. Defaults to last project opened')
parser.add_argument('-a', '--active', action='store_true', dest='status', help='add a memo while keeping the tracking active.')
parser.add_argument('memo', metavar='m', type=str, nargs='?', default='', help='A memo of what was done')

arguments = parser.parse_args()

try:
    open('.last')
except IOError as e:
    print 'No settings found.', 'Would you like to make a new settings file?'
    exit()
else:
    store = open('.last', 'r')
    last = store.readline().rstrip('\n').partition(' ')
    store.close()

if arguments.project:
    path = os.path.join(os.path.dirname(__file__), 'logs/' + arguments.project[0]  + '.csv')
    last = (path, ' ', 's')
    store = open('.last', 'w')
    store.write(last[0] + last[1] + last[2])
    store.close
else:
    if last:
        path = last[0]
    else:
        print "No project specified.", "Run again with -p"
        exit()

try:
    open(path)
except IOError as e:
    print "Project not found.", "Start new project?"
    exit()
else:
    log = open(path, 'a')

if last[2] == 'a':
    status = 's'
else:
    status = 'a'
if arguments.status:
    status = 'a'

writer = csv.writer(log, lineterminator='\n')
writer.writerow((time.time(), status, arguments.memo))
log.close()
if status == 'a':
    print "Tracking your time."
if status == 's':
    print "Tracking suspended."
    
store = open('.last', 'w')
store.write(path+' '+status)
store.close
