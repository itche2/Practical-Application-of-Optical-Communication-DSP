import sys
import numpy as np
import matplotlib.pylab as plt
from qampy import signals, io, filtering
import os
import pdb

def transmit_signal(fs, M, N, nmodes=1, fb=1, bitclass=signals.RandomBits, dtype=np.complex128, **kwargs):
    """
    Parameters
    ----------
        fs: float
            desired sampling frequency
        M : int
            QAM order
        N : int
            number of symbols per polarization
        nmodes : int, optional
            number of modes/polarizations
        fb  : float, optional
            symbol rate 
        bitclass : Bitclass object, optional
            class for initialising the bit arrays from which to generate the symbols, by default use
            RandomBits.
        dtype : numpy dtype, optional
            dtype of the array. Should be either np.complex128 (default) for double precision or np.complex64
        **kwargs 
            kword arguments to pass to bitclass
    """
    #Generating signal
    sig = signals.SignalQAMGrayCoded(M, N, nmodes, fb, bitclass, dtype, **kwargs)
    #Resampling signal at output AWG
    resampled_sig=sig.resample(fs, beta=0.1, renormalise=True)
    return resampled_sig

def export_signal(DACrate, sig, M, N, nmodes=1, fb=1, fs=1, bitclass=signals.RandomBits, dtype=np.complex128, **kwargs):
    #Saving signal to file in compressed form
    sig.save_to_file('saved_signal.txt')
    
    if not os.path.isdir('data_files'):
        os.makedirs('data_files')

    f_sig_p = "data_files/sig_prop.txt"
    f_sig_prop = open(f_sig_p, "w")
    f_sig_prop.writelines(str(DACrate) + '\n' + str(M) + '\n' + str(N) + '\n' + str(nmodes) + '\n' + str(fb) + '\n' + str(bitclass) + '\n' + str(dtype) + '\n' + str(**kwargs) + '\n')    
    f_sig_prop.close()
    
    fname = "data_files"
##    f = open(fname, "w")
##    for i in range(0, sig.shape[1]):
##        a = sig[0,i]
##        f.writelines(str(a) + '\n') 
##    f.close()


    with open(fname + "/tmp_real_X.txt", 'w') as RX:
##        for i in range(0, sig.shape[0]):
        for item in sig.real[0]:
            RX.write('%s\n' % item)
    with open(fname + "/tmp_imag_X.txt", 'w') as IX:
##        for i in range(0, sig.shape[0]):
        for item in sig.imag[0]:
            IX.write('%s\n' % item)                
    with open(fname + "/tmp_real_Y.txt", 'w') as RY:
##        for i in range(0, sig.shape[0]):
        for item in sig.real[1]:
            RY.write('%s\n' % item)
    with open(fname + "/tmp_imag_Y.txt", 'w') as IY:
##        for i in range(0, sig.shape[0]):
        for item in sig.imag[1]:
            IY.write('%s\n' % item)
                
## Original Data signal generated
    with open(fname + "/data_real_X.txt", 'w') as RX_D:
##        for i in range(0, sig.shape[0]):
        for item in sig.symbols.real[0]:
            RX_D.write('%s\n' % item)
    with open(fname + "/data_imag_X.txt", 'w') as IXD:
##        for i in range(0, sig.shape[0]):
        for item in sig.symbols.imag[0]:
            IXD.write('%s\n' % item)                
    with open(fname + "/data_real_Y.txt", 'w') as RYD:
##        for i in range(0, sig.shape[0]):
        for item in sig.symbols.real[1]:
            RYD.write('%s\n' % item)
    with open(fname + "/data_imag_Y.txt", 'w') as IYD:
##        for i in range(0, sig.shape[0]):
        for item in sig.symbols.imag[1]:
            IYD.write('%s\n' % item)


    
##fs = 92.e9          #Sampling frequency
##DACrate = fs
##M = 4               #M-QAM
##nmodes = 2           #Number of polarizations
##fb = 10*10**9       #Symbol rate (float)
##Baud = fb
##N = 2**18/(fs/fb)/2 #Number of symbols per polarization; This is set to be around 2^18 bits of data (0.5*2^18 symbols) after resampling.
##N = 2**18/(DACrate/Baud) #Number of symbols per polarization; This is set to be around 2^18 symbols (2*2^18 samples) after resampling.
##
##sig = transmit_signal(DACrate, M, N, nmodes, fb)
##
##sig_len_xtnd = 2**18-sig.shape[1] #length of extension of signal
###Extending signal to get exact size of 2^18
##sig_temp=sig
##for i in range(0, sig_len_xtnd):
##    sig_temp = np.hstack([sig_temp, [[0],[0]]])
##pdb.set_trace()
##sig_exp=sig.recreate_from_np_array(sig_temp)
##export_signal(DACrate, sig, M, N, nmodes, fb)
#pdb.set_trace()
##sys.stdout.write("Done")
