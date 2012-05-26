import argparse
import time
import csv

parser = argparse.ArgumentParser(description='Log time tracking information')
parser.add_argument('-p', '--project', metavar='p', type=str, action='store', dest='project', help='The project name. Defaults to last project opened')
parser.add_argument('memo', metavar='m', type=str, nargs='?', help='A memo of what was done')

arguments = parser.parse_args()

# Get settings
try:
    open('last')
except IOError as e:
    print 'No settings found.', 'Would you like to make a new settings file?'
    exit()
else:
    last = open('last', 'r')
    last = last.read().partition(' ')

if arguments.project:
    path = arguments.project
else:
    if state.last:
        path = last[0]
    else:
        print "No project specified"
        exit()

def loadlog(path):
    try:
        open()
    except IOError as e:
        print "Project not found.", "Start new project?"
        exit()

def logtime(path, memo):
    pass
