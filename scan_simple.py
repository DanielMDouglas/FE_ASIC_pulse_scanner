import numpy as np
import os

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
    output = os.system(cmdString)
    return output

def do_test(A = 0, B = 0, dt = 0):
    "Run the femb_python simple test routine to measure ASIC response"
    
    outfile = "data/scan/"+str(A)+"_"+str(B)+"_"+str(dt)
    args = ["-o", outfile,
            "-s"]
    cmdString = " ".join([TEST_EXE]+args)
    output = os.system(cmdString)
    return output

NA = NB = Ndt = 11

A_space = np.linspace(0, 10, NA)
B_space = np.linspace(0, 10, NB)
dt_space = np.linspace(0, 10, Ndt)

for A in A_space:
    for B in B_space:
        for dt in dt_space:
            set_pulser(A, B, dt)
            do_test(A, B, dt)
