#!/usr/bin/python
from sys import argv # argv[0] gives main.py
import os  # print os.popen("echo Hello, World!").read()
from multiprocessing import cpu_count
# Dependencies: Make, gcc, Linux.

#sys.argv[1] is the location of the makefile.
if len(argv) < 2:
    print("Usage:\nCall: python3 main.py [PATH TO DIRECTORY CONTAINING MAKEFILE] [GCC FLAGS]\nNote: This assumes the gcc flags in the makefile are passed as a variable named CXXFLAGS.")
else:
    try:
        print("Cleaning filetree")
        os.system("make clean")
        print("Compiling program...")
        returnval = os.popen("make -j" + str(cpu_count))
        if returnval != 0:
            raise "ReturnError"
        else: # We managed to compile the program
            #Let's import the flags.
            if len(argv) > 2:
                # Let's take the flags from our parameters.
                flags = argv[2:]


    except "ReturnError":
        print("Something went wrong compiling program. Exiting...")
        