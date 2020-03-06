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
        \nAnd that the executable is found in PATH/bin/program.exe")
else:

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


def randflags(rawflags):
    """ Randomizes flags from rawflags and returns an array of variable-length combinations""" 
    flags = []
    for l in range(len(rawflags)):
        for x in itertools.combinations(rawflags,l):
            flags.append(x)

    return flags # Should be safe even if rawflags was empty


def log(path, result, flaglist):
    """ Logs one result to a logfile. """
    try:
        resultLog = open(path + "/log.txt", "w")
        flags  = ""
        for flag in flaglist:
            flags += flag + " "
        resultLog.write(path + "/Program.exe: " + str(result) + " " + flags)
    except IOError:
        print("Could not open logfile")
        return False
    return False


def TimeProgram(path, rawflags):
    """ Assumes rawflags is a 2d array containing combinations of our flags """
    
    for flaglist in flags:
        command = "make -j" + str(cpu_count()) + "CXXFLAGS = \""
        for flag in flaglist:
            command += flag + " "
        command += "\""
        try:
            returnval = os.popen(command) # Compiling code using make.
            
            if returnval != 0: # Something went wrong when compiling
                raise OSError

            else: # We managed to compile the program
                # Let's benchmark the program.
                times = []
                for i in range(5):
                    # Let's run the program 5 times and log the average time.
                    t_start = datetime.now()

                    os.system(path + "/bin/Program.exe") # TODO: Implement custom program name
                    # TODO: Consider program return values. End if non-zero return.

                    t_end = datetime.now()
                    times.append(t_start - t_end)
                #Calculating and logging results
                result = 0
                for time in times:
                    result += time
                result = result/5
                logged = log(result, flaglist)
                if not logged:
                    raise OSError
        except OSError:
            flagsUsed = ""
            for flag in flaglist:
                flagsUsed += flag + " "
            print("Something went wrong testing the program.\nFlags were: " + flagsUsed + "\nExiting...")
            return False
    return True # We tried all combinations without a hitch.
            