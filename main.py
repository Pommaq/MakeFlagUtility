#!/usr/bin/python3
from sys import argv # argv[0] gives main.py
import subprocess # To replace os
from multiprocessing import cpu_count
import itertools
import timeit
import os

# Dependencies: Make, gcc, Linux. python3.7

#sys.argv[1] is the location of the makefile.

def randflags(rawflags):
    """ Randomizes flags from rawflags and returns an array of variable-length combinations""" 
    print("Randomizing flags. ")
    flags = []
    if len(rawflags) > 1:
        for l in range(0,len(rawflags)):
            for x in itertools.combinations(rawflags,l):
                flags.append(x)
    else:
        flags = [rawflags]
    return flags # Should be safe even if rawflags was empty


def log(path, programname, result, flaglist):
    """ Logs one result to a logfile. """
    try:
        resultLog = open(path + "/log.txt", "a")
        flags  = ""
        for flag in flaglist:
            flags += flag + " "
        resultLog.write(path + "/" + programname + ": " + str(result) + " COMPILER_FLAGS:" + flags + "\n")
        return True
    except IOError:
        print("Could not open logfile")
        return False
    return False

def runProgram(path, programname):
    return subprocess.run([path + "/bin/" + programname, path + "/TestDir/"], shell=False).returncode # TODO: Take custom parameters
    




def TimeProgram(path, programname, rawflags):
    """ Assumes rawflags is a 2d array containing combinations of our flags """

    for flaglist in rawflags:
        if flaglist:
            CppFlags = "CPPFLAGS="
            CppFlags += flaglist[0]
            for flag in flaglist[1:]:
                CppFlags += " %s" %(flag)
        else:
            CppFlags = "CPPFLAGS="
        try:
            FNULL = open(os.devnull, "w") # Consumes program output
            
            subprocess.run(["make", "-C", argv[1], "clean",], stdout=FNULL) #Note: stderr is still stderr.

            print("Compiling program")
            print(CppFlags)
            returnval = subprocess.run(["make", "-j", str(cpu_count()), "-C", path, CppFlags], stdout = FNULL, shell=False ).returncode # Compile code using make and our flags
            if returnval != 0: 
                FNULL.close()
                raise OSError
            else: 
                # Let's benchmark the program.
                print("Testing with flags: " + CppFlags)
                m_times = []
                for i in range(16):
                    # Let's run the program X times and log the average time.
                    # TODO: Consider program return values. End if non-zero return.
                    arguments = """[
                        '%s',
                        '%s',
                        '%s'], stdout=FNULL
                        """ % ( path + "/bin/" + programname, path + "/TestDir/", "shell=False") 
                    m_times.append(timeit.timeit(stmt="subprocess.run(%s)" % (arguments) + "; FNULL.close()", setup="import subprocess, os; FNULL=open(os.devnull,'w')", number=1))
                FNULL.close()
                #Calculating and logging results
                result = 0
                for time in m_times:
                    result += time
                result = result/16
                print("Result was: " + str(result))
                logged = log(path, programname, result, flaglist)
                if not logged:
                    raise OSError
                    
        except OSError as error:
            flagsUsed = ""
            for flag in flaglist:
                flagsUsed += flag + " "
            print("Something went wrong testing the program.\nFlags were: " + flagsUsed)
            print(error)
            print("Exiting...")
            return False

    return True # We tried all combinations without a hitch.


def main():

    if len(argv) < 3:
        print("Usage:\nCall: python3 main.py [PATH TO DIRECTORY CONTAINING MAKEFILE] [EXECUTABLE NAME] [GCC FLAGS]\nNote: This assumes the gcc flags in the makefile are passed as a variable named " \
                + "CPPFLAGS inside the makefile\nand that the executable is found in PATH/bin\nIf there are no [GCC FLAGS] then the flag will be taken from a flag.db file inside the directory")
        return False
    else:

        print("Cleaning filetree")
        subprocess.run(["make", "-C", argv[1], "clean",])
        ProgramName = argv[2] # Saving name of executable
        """ Let's store flags. """
        if len(argv) > 3:
            flags = argv[3:]
        else:
            try:
                flagsdb = open(argv[1] + "/flags.db")
                flags = []
                for line in flagsdb:
                    flags.append(line)
                flagsdb.close()
            except IOError:
                    print("Could not open flags.db and no flags passed as parameters. Continuing with no flags")
                    flagsdb.close()
                    flags = [""]
            
            return True
            
        RandomizedFlags = randflags(flags)
        # We are now ready to compile and run the tests.
        TimeProgram(argv[1], ProgramName, RandomizedFlags)

if __name__ == "__main__":
    main()
            

