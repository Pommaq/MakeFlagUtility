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
        if len(argv) > 2:
            flags = argv[2:]
        else:
            # Read flags from flags.db
            try:
                flagsdb = open(argv[1] + "/flags.db")
                flags = ()
                for line in flagsdb:
                    flags.append(line)
                flagsdb.close()
            except IOError:
                print("Could not open flags.db and no flags passed as parameters. Exiting...")
                flagsdb.close()
                sys.exit(1) # EXIT_FAILURE
        
        command = "make -j" + str(cpu_count()) + "CXXFLAGS = \""
        for flag in flags:
            command += flag + " "
        
        returnval = os.popen(command)
        
        if returnval:
            raise OSError
        else: # We managed to compile the program
            #Let's import the flags.
            if len(argv) > 2:
                # Let's take the flags from our parameters. That is everything after the makefile path
                flags = argv[2:]
                


    except OSError:
        print("Something went wrong compiling program. Exiting...")
        