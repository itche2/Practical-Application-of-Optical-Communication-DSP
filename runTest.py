import pdb
import sys
import numpy as np
from qampy.core import ber_functions, impairments
from qampy import impairments, signals,equalisation, helpers
from signalGenerate_v3 import transmit_signal, export_signal
from signalReceive_v6 import signal_compare, receive_signal, receive_signal_compressed, import_signal, equalize_synchronize_signal, recreate_signal_with_synced_transmitter_symbols, interpolate_signal

#Testing for different sampling rates at the transmitter and symbol rates
##for tx_fs in [62*10**9, 92*10**9]:
##    for sym_r in [60*10**9, 32*10**9, 28*10**9, 12*10**9, 12.5*10**9, 11*10**9, 10*10**9]:
##        transmit_signal(tx_fs, 4, 2**18/(tx_fs/sym_r)/2, 1, sym_r)
##        resampled_sig = receive_signal()
##        signal_compare(resampled_sig)
##        print(tx_fs, sym_r)
##        #pdb.set_trace()

#Transmitter side
fs = 92.e9          #Sampling frequency
M = 4               #M-QAM
nmodes =2           #Number of polarizations
fb = 10*10**9       #Symbol rate (float)
#N = 2**18/(fs/fb)/2 #Number of symbols per polarization; This is set to be around 2^18 bits of data (0.5*2^18 Sa) after resampling.
N = 2**18/(fs/fb)
#N = 2**18/(fs/fb)-1

#Main code
sigS = signals.SignalQAMGrayCoded(M, N, nmodes, fb)
sps = sigS.Nbits #bits per symbol
DACrate = fs
sig = transmit_signal(fs, M, N, nmodes, fb, shift=-20000)

#Extending signal to get exact size of 2^18
sig_len_xtnd = 2**18-sig.shape[1] #length of extension of signal
sig_temp=sig
xtnd_arr=np.zeros((2,sig_len_xtnd))
sig_temp = np.hstack([sig_temp, xtnd_arr])
sig_exp=sig.recreate_from_np_array(sig_temp)
export_signal(DACrate, sig_exp, M, N, nmodes, fb)

#Receiver side
resampled_sig = receive_signal_compressed()
##resampled_sig_2 = receive_signal()

sig_intrplt=interpolate_signal(resampled_sig)

E, ber, errs ,tx_synced = synchronize_equalize_signal(resampled_sig = resampled_sig)


pdb.set_trace()

sys.stdout.write("Done")



