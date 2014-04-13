#! /usr/bin/python

"main.py: Main file for commandline-execution of bugbuster."

import sys
import bugbuster

if len(sys.argv) != 3:
    print "Usage: python main.py BUGPATH LANDSCAPEPATH"
else:
    print bugbuster.count_bugs(*sys.argv[1:])
