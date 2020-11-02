import sys
import numpy as np
import matplotlib.pylab as plt
from qampy import equalisation, signals, impairments, helpers, phaserec, io
import pdb
import sys

def transmit_signal(fs, M, N, nmodes=1, fb=1, bitclass=signals.RandomBits, dtype=np.complex128, **kwargs):
    sig = signals.SignalQAMGrayCoded(M, N, nmodes, fb, bitclass, dtype, **kwargs)
    resampled_sig=sig.resample(fs, beta=1, renormalise=True)
    return resampled_sig

def export_signal(sig, M, N, nmodes=1, fb=1, bitclass=signals.RandomBits, dtype=np.complex128, **kwargs):
    f_sig_p = "sig_prop.txt"
    f_sig_prop = open(f_sig_p, "w")
    f_sig_prop.writelines(str(M) + '\n' + str(N) + '\n' + str(nmodes) + '\n' + str(fb) + '\n' + str(bitclass) + '\n' + str(dtype) + '\n' + str(**kwargs) + '\n')    
    f_sig_prop.close()

    fname = "signal.txt"
    f = open(fname, "w")
    for i in range(0, sig.shape[1]):
        a = sig[0,i]
        f.writelines(str(a) + '\n')    
    f.close()
    

fs = 92.e9 #Sampling frequency
M = 4 #M-QAM
N = 4000 #Number of symbols per polarization
nmodes =1 #Number of polarizations
fb = 10*10**9 #Symbol rate (float)

#pdb.set_trace()
sig = transmit_signal(fs, M, N, nmodes, fb)
sig.save_to_file('saved_signal.txt')
export_signal(sig, M, N, nmodes, fb)

sys.stdout.write("Done")
