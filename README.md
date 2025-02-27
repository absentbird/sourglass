Sourglass
=========

The Simple Hour Glass. A simple, fast, CLI program to track time on projects.

The basic structure of sourglass is to be as simple and easy as possible. The first time you start sourglass it will create a `.sourglass` folder in your home directory. In there you will find a `logs` folder which will contain the time logs of any projects you start and a 'last' file which just holds the name and state of the last project you altered.

The log files are stored as `.csv` files.

Usage
---------

Every statement that will leave a log entry (except for time shifts) can be followed by a memo.

Any oporation can have use the -p (--project) flag to set the project

If a project does not exist it will be made.

If a .sourglass file is in your current working directory and you did not set the -p flag the .sourglass file will be used as a log.

### Commands

`-h` Print a help file

`-p` Set the project for the command to be run on

`-m` Leave a memo without changing the status of the log (Eg. if it was currently tracking after you leave the memo it will still be tracking)

`-t` Total up the hours on the project

`-s` Shift time by the amount specified (Ex: t-40m would remove 40 minutes from the log)

`-r` Remove the last x entries from the log.

`--audit` Print an audit of the log with human readible times and memos and a total.

### Examples

To start a new project type: `python sourglass.py -p '<project name>' [optional memo]`

To stop/start time tracking type `python sourglass.py -p '<project name>'`

To toggle the tracking status on the last project used type `python sourglass.py`

To print the hours logged on the current project type `python sourglass.py -t`

### Tips

Typing `python sourglass.py -p '.sourglass'` will create the log in your current working directory.
