import sys
import numpy as np
import matplotlib.pylab as plt
from qampy import signals, io, filtering
import pdb

def transmit_signal(fs, M, N, nmodes=1, fb=1, bitclass=signals.RandomBits, dtype=np.complex128, **kwargs):
    sig = signals.SignalQAMGrayCoded(M, N, nmodes, fb, bitclass, dtype, **kwargs)
    #sig = filtering.rrcos_pulseshaping(sig, 0.1)
    pdb.set_trace()
    resampled_sig=sig.resample(fs, beta=0.1, renormalise=True)
    #resampled_sig=sig.resample(fb*2)
    #, beta=0.1, renormalise=True)
    pdb.set_trace()
    resampled_sig.save_to_file('saved_signal.txt')
    return resampled_sig

fs = 92.e9 #Sampling frequency
M = 4 #M-QAM
N = 2**16 #Number of symbols per polarization
N = 30000
nmodes =1 #Number of polarizations
fb = 10*10**9 #Symbol rate (float)
N = 2**18/(fs/fb)/2 #Number of symbols per polarization; This is set tobe around 2^18 bits of data after resampling.
#N = 2**18/(fs/fb)
#fs = 62*10**9
#pdb.set_trace()
sig = transmit_signal(fs, M, N, nmodes, fb)

sys.stdout.write("Done")
