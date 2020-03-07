
This is a utility designed to compile a C/C++ program with a large combination of compilerflags and then test the performance, finally logging the results to a logfile.
I needed this so I could easily test what combination of flags would optimise performance.

Usage:
Place a file named flags.db inside the folder you wish to compile, or pass the flags we should test as parameters after the .executable name. Each line in flags.db counts as one flag. Make sure there isnt a newline at the end of it or in the middle
Example of running it:

`[pommaq@localhost Makeutil]$ python main.py AV-PYTH/ AV -ofast -funroll-all-loops -Wunused-variable -Werror -fcombine-stack-adjustments  -fconserve-stack`

where AV-PYTH contains the src code and the makefile. AV is the .exe name found as .../AV-PYTH/bin/AV. This is what we run to try shit.
The program is currently hardcoded to run AV-PYTH as parameters.
