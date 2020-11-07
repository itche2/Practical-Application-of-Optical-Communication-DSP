import sys
import numpy as np
import matplotlib.pylab as plt
from qampy import signals, io, filtering
import os
import pdb
from scipy.interpolate import interp1d
from qampy import signals, equalisation, helpers, phaserec, io, filtering
from qampy.core import ber_functions, impairments

def interpolate_signal(sig):
    #Generate a interpolated signal
    x = np.linspace(0, len(sig[0])-1, len(sig[0]), endpoint=True)
    f1 = interp1d(x, sig[0], kind='cubic')
    f2 = interp1d(x, sig[1], kind='cubic')
    sig_n=[[],[]]

    x_n=np.linspace(0.5, len(sig[0])-1-0.5, len(sig[0])-1, endpoint=True)
    sig_n = np.asarray([f1(x_n), f2(x_n)])
    sig_n = sig.recreate_from_np_array(sig_n)
    return sig_n

def extend_signal(sig,xtnd_w_zero=1):        
    #Extend the signal to 2^18 number of symbols
    sig_len_xtnd = 2**18-sig.shape[1] #length of extension of signal
    sig_temp=sig

    #Extend the signal to 2^18 number of symbols with zeros
    if xtnd_w_zero == 1:    
        xtnd_arr=np.zeros((2,sig_len_xtnd))
        sig_temp = np.hstack([sig_temp, xtnd_arr])
        sig_xtnd=sig.recreate_from_np_array(sig_temp)

    #Extend the signal to 2^18 number of symbols with the signal itself
    else: 
        sig_temp = np.hstack([sig_temp, sig[:,:sig_len_xtnd]])
        sig_xtnd=sig.recreate_from_np_array(sig_temp)
    return sig_xtnd

def delay(sig, shift, nmodes):
    if nmodes == 1:
        sig = np.roll(sig, shift, axis=0) #single polarization desynchronization
    if nmodes == 2:
        sig = np.roll(sig, shift, axis=1) #dual polarization desynchronization
    return sig
