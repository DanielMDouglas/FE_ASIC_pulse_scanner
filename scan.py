import curses as crs
import numpy as np
from time import sleep
import os
import subprocess

stdscr = crs.initscr()
crs.noecho()
crs.cbreak()
stdscr.keypad(1)
stdscr.nodelay(1)
crs.curs_set(0)

maxHeight, maxWidth = stdscr.getmaxyx()

# edit these!
# they should point to the executable itself,
# not including arguments
# right now they just make noise and take time...
PULSER_EXE = "sleep 1; cat /proc/cpuinfo; echo"
TEST_EXE = "sleep 1; echo"

def set_pulser(A = 0, B = 0, dt = 0):
    """Set the argibrary wave generator to produce two pulses of height A and B, 
    seperated by time interval dt"""

    args = ["-A", str(A),
            "-B", str(B),
            "-dt", str(dt)]
    cmdString = " ".join([PULSER_EXE]+args)
    output = subprocess.check_output(cmdString, shell = True)
    return output
    
def do_test(A = 0, B = 0, dt = 0):
    "Run the femb_python simple test routine to measure ASIC response"

    outfile = "data/scan/"+str(A)+"_"+str(B)+"_"+str(dt)
    args = ["-o", outfile,
            "-s"]
    cmdString = " ".join([TEST_EXE]+args)
    output = subprocess.check_output(cmdString, shell = True)
    return output

def frac_bar(title, n, N):
    "Returns a string of a progress bar depending on the fraction given"
    f = float(n)/N
    bar_size = maxWidth - 20
    full = int(bar_size*f)
    empty = bar_size - full

    bar = " " + title + (3 - len(title))*" "
    bar += "  "
    bar += str(n) + " "*(5 - len(str(n)))
    bar += "["
    bar += full*"#"
    bar += empty*"-"
    bar += "]"
    bar += " "*(5 - len(str(N))) + str(N)
    bar += "  "
    
    return bar
    
NA = NB = Ndt = 11

A_space = np.linspace(0, 10, NA)
B_space = np.linspace(0, 10, NB)
dt_space = np.linspace(0, 10, Ndt)

stdscr.addstr(maxHeight-6, 0, maxWidth*"-")
for i, Ai in enumerate(A_space):
    stdscr.addstr(maxHeight-4, 0, frac_bar("A:", i, NA))
    for j, Bj in enumerate(B_space):
        stdscr.addstr(maxHeight-3, 0, frac_bar("B:", j, NB))
        for k, dtk in enumerate(dt_space):
            stdscr.addstr(maxHeight-2, 0, frac_bar("dt:", k, Ndt))

            output = set_pulser(Ai, Bj, dtk)
            for row, line in zip(range(0, maxHeight-7), output.split('\n')):
                stdscr.addstr(row, 0, line[:maxWidth])

            output = do_test(Ai, Bj, dtk)
            for row, line in zip(range(0, maxHeight-7), output.split('\n')):
                stdscr.addstr(row, 0, line[:maxWidth])

            stdscr.refresh()
