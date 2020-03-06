#!/usr/bin/python3
from sys import argv # argv[0] gives main.py
import os  # print os.popen("echo Hello, World!").read()
from multiprocessing import cpu_count
import datetime
import itertools
# Dependencies: Make, gcc, Linux. python3.7

#sys.argv[1] is the location of the makefile.
if len(argv) < 2:
    print("Usage:\nCall: python3 main.py [PATH TO DIRECTORY CONTAINING MAKEFILE] [GCC FLAGS]\nNote: This assumes the gcc flags in the makefile are passed as a variable named CXXFLAGS.\
        \nAnd that the filestructure of your source code is as following:\nbin/Executable\nbuild/[.o FILES]\nsrc/[.cpp FILES]\ninclude/[.hpp FILES]")
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
                flags = []
                for line in flagsdb:
                    flags.append(line)
                flagsdb.close()
            except IOError:
                print("Could not open flags.db and no flags passed as parameters. Exiting...")
                flagsdb.close()
                sys.exit(1) # EXIT_FAILURE
        
        command = "make -j" + str(cpu_count()) + "CXXFLAGS = \""

def TimeProgram(path, rawflags):
        for i in range(len(rawflags)):
            flags = itertools.permutations(rawflags[:i])
            for flag in flags:
                command += flag + " "
            command += "\""

            returnval = os.popen(command) # Compiling code using make.
            
            if returnval != 0: # Something went wrong when compiling
                raise OSError

            else: # We managed to compile the program
                # Let's benchmark the program.
                for i in range(5):
                    # Let's run the program 5 times and log the average time.
                    t_start = datetime.now()
                    # RUN PROGRAM
                    

                    t_end = datetime.now()
                    result = t_start - t_end
        except OSError:
            print("Something went wrong compiling program. Exiting...")
            