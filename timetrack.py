import argparse
import time
import csv

parser = argparse.ArgumentParser(description='Log time tracking information')
parser.add_argument('-p', '--project', metavar='p', type=str, action='store', dest='project', help='The project name. Defaults to last project opened')
parser.add_argument('memo', metavar='m', type=str, nargs='?', default='', help='A memo of what was done')

arguments = parser.parse_args()

# Get settings
try:
    open('last')
except IOError as e:
    print 'No settings found.', 'Would you like to make a new settings file?'
    exit()
else:
    store = open('last', 'r')
    last = store.readline().partition(' ')
    store.close()

if arguments.project:
    path = arguments.project
    store = open('last', 'w')
    store.write(path + ' a')
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

if last:
    status = last[2].rstrip('\n')
else:
    status = 'a'

writer = csv.writer(log)
writer.writerow((time.time(), status, arguments.memo))
