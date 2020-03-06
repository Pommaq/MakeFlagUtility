#!/usr/bin/python3
from sys import argv # argv[0] gives main.py
import os  # print os.popen("echo Hello, World!").read()
from multiprocessing import cpu_count
import datetime
import itertools
# Dependencies: Make, gcc, Linux. python3.7

#sys.argv[1] is the location of the makefile.

def randflags(rawflags):
    """ Randomizes flags from rawflags and returns an array of variable-length combinations""" 
    flags = []
    for l in range(len(rawflags)):
        for x in itertools.combinations(rawflags,l):
            flags.append(x)

    return flags # Should be safe even if rawflags was empty


def log(path, programname, result, flaglist):
    """ Logs one result to a logfile. """
    try:
        resultLog = open(path + "/log.txt", "w")
        flags  = ""
        for flag in flaglist:
            flags += flag + " "
        resultLog.write(path + "/" + programname + ": " + str(result) + " " + flags)
    except IOError:
        print("Could not open logfile")
        return False
    return False


def TimeProgram(path, programname, rawflags):
    """ Assumes rawflags is a 2d array containing combinations of our flags """
    
    for flaglist in rawflags:
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

                    os.system(path + "/bin/" + programname)
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


def main():

    if len(argv) < 3:
        print("Usage:\nCall: python3 main.py [PATH TO DIRECTORY CONTAINING MAKEFILE] [EXECUTABLE NAME] [GCC FLAGS]\nNote: This assumes the gcc flags in the makefile are passed as a variable named CXXFLAGS\
            \nand that the executable is found in PATH/bin")
        return False
    else:

        print("Cleaning filetree")
        os.system("make clean")
        print("Compiling program...")
        ProgramName = argv[2] # Saving programname
        if len(argv) > 3:
            flags = argv[3:]
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
                    return False
            
            RandomizedFlags = randflags(flags)
            # We are now ready to compile and run the tests.
            TimeProgram(argv[1], ProgramName, RandomizedFlags)

if __name__ == "__main__":
    main()
            

