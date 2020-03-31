#!/usr/bin/python3
from sys import argv # argv[0] gives main.py
import subprocess # To replace os
from multiprocessing import cpu_count
import itertools
import timeit
import os
import copy
from Flag import Flag
# Dependencies: Make, gcc, Linux. python3.7

def readOptFlags(path=argv[1]):
    #Let's read our data from Flag-notes.txt
    o1 = o2 = o3 = oS = False
    flagClass = []

    try:
        optFlags = open(path + "/Flag-notes.txt") 
        try:
            for line in optFlags:
                text = line.strip() # Avoid calling .strip multiple times
                """ Sadly we do not have a switch() function implemented in python..."""
                if text == "-o1/-o2/-o3:":
                    o1 = o2 = o3 = True
                    oS = False
                    continue # To avoid so "-o1/-o2/-o3:" is treated as a compiler flag
                elif text == "-o2/-o3/-os:":
                    o2 = o3 = oS = True
                    o1 = False
                    continue
                elif text == "-o2/-o3:":
                    o2 = o3 = True
                    oS = o1 = False
                    continue
                elif text == "-o3:":
                    o3  = True
                    o1 = o2 = oS = False
                    continue

                flagClass.append(Flag.cFlag(text,o1,o2,o3,oS))
        finally:
            optFlags.close()
    except IOError:
        print("Something went wrong opening flag-notes.txt")
        exit(-1)
    return flagClass
        

def readFlags(optFlags):
    if len(argv) > 3:
        flags = []
        for entry in argv[3:]:
            for flag in optFlags:
                if entry == flag.a_flag:
                    flags.append(copy.copy(flag))
                    break
                else:
                    flags.append(Flag.cFlag(entry, False,False,False,False))
                    break 
    else:
        try:
            flagsdb = open(argv[1] + "/flags.db")
            flags = []
            try:
                for line in flagsdb:
                    for flag in optFlags:
                        if line.strip() == flag.a_flag:
                            flags.append(copy.copy(flag))
                    flags.append(Flag.cFlag(line[:len(line)-1], False, False, False, False))
            finally:
                flagsdb.close()
        except IOError:
                print("Could not open flags.db and no flags passed as parameters. Continuing with no flags")
                flags = [""]
    return flags


def randflags(rawflags, programname, optflags, path):
    """ Randomizes flags from rawflags and returns an array of variable-length combinations""" 
    print("Reading optimization flags")
    if len(rawflags) > 1:
        optLevels = ("-o1", "-o2", "-o3", "-os")
        for i in range (4):
            flagsToUse = []
            for flag in rawflags:
                stat = (flag.a_o1, flag.a_o2, flag.a_o3, flag.a_os)
                if not stat[i]:
                    flagsToUse.append(copy.copy(flag))
            
            #Create all combinations then inject our opt flag
            if len(flagsToUse) > 0:
                for l in range(0,len(flagsToUse)):
                    for x in itertools.combinations(flagsToUse,l):
                        TimeProgram(path, programname, x + (optLevels[i],))            
    else:
        flags = [rawflags]
    return flags


def log(path, programname, result, flaglist):
    """ Logs one result to a logfile. """
    try:
        resultLog = open(path + "/log.txt", "a")
        flags  = ""
        for flag in flaglist:
            flags += str(flag) + " "
        resultLog.write(path + "/" + programname + ": " + str(result) + " COMPILER_FLAGS:" + flags + "\n")
        return True
    except IOError:
        print("Could not open logfile")
        return False
    return False

def runProgram(path, programname):
    return subprocess.run([path + "/bin/" + programname, path + "/TestDir/"], shell=False).returncode # TODO: Take custom parameters
    




def TimeProgram(path, programname, rawflags):
    """ Assumes rawflags is a 1d array containing compiler flags """

    if rawflags:
        CppFlags = "CPPFLAGS="
        CppFlags += "%s" %rawflags[0]
        for flag in rawflags[1:]:
            CppFlags += " %s" %(flag)
            #CppFlags += " -pipe"
    else:
        CppFlags = "CPPFLAGS="
    try:
        FNULL = open(os.devnull, "w") # Consumes program output
        
        subprocess.run(["make", "-C", argv[1], "clean",], stdout=FNULL) #Note: stderr is still stderr.

        print("Compiling program")
        print(CppFlags)
        returnval = subprocess.run(["make", "-j", str(cpu_count()), "-C", path, CppFlags], stdout = FNULL, shell=False ).returncode # Compile code using make and our flags
        FNULL.close()

        if returnval != 0: 
            raise OSError
        else: 
            print("Testing with flags: " + CppFlags)
            m_times = []
            for _ in range(16):
                # Let's run the program X times and log the average time.
                # TODO: Consider program return values. End if non-zero return.
                arguments = """[
                    '%s',
                    '%s',
                    '%s'], stdout=FNULL
                    """ % ( path + "/bin/" + programname, path + "/TestDir/", "shell=False") 
                m_times.append(timeit.timeit(stmt="subprocess.run(%s)" % (arguments) + "; FNULL.close()", setup="import subprocess, os; FNULL=open(os.devnull,'w')", number=1))
            result = 0
            for time in m_times:
                result += time
            result = result/16
            print("Result was: " + str(result))
            logged = log(path, programname, result, rawflags)
            if not logged:
                raise OSError
                
    except OSError as error:
        flagsUsed = ""
        for flag in rawflags:
            flagsUsed += str(flag) + " "
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
        #ProgramName = argv[2] # Saving name of executable
        """ Let's store flags. """
        optflags = readOptFlags()
        flags = readFlags(optflags)
            
        RandomizedFlags = randflags(flags, argv[2] , optflags, argv[1])
        # We are now ready to compile and run the tests.
        TimeProgram(argv[1], argv[2], RandomizedFlags)

if __name__ == "__main__":
    main()
            

