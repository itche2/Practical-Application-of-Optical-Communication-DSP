from signalGenerate_v2 import transmit_signal
from signalReceive_v2 import signal_compare, receive_signal
import pdb
import sys
from qampy import impairments, signals
import numpy as np
from qampy.core import ber_functions#, impairments

##for tx_fs in [62*10**9, 92*10**9]:
##    for sym_r in [60*10**9, 32*10**9, 28*10**9, 12*10**9, 12.5*10**9, 11*10**9, 10*10**9]:
##        transmit_signal(tx_fs, 4, 2**18/(tx_fs/sym_r)/2, 1, sym_r)
##        resampled_sig = receive_signal()
##        signal_compare(resampled_sig)
##        print(tx_fs, sym_r)
##        #pdb.set_trace()

def sync_and_adjust(tx, rx, synced=False):
##    tx_out = []
##    rx_out = []
##    txmodes = tx.shape[0]
##    rxmodes = rx.shape[0]
##    idxx = list(range(max(txmodes, rxmodes)))
    # TODO: check if it's possible to do this in a faster way. One option: only shift once.
##    for j in range(rx.shape[0]):
    for j in [0]:
##        acm = -100.
##        for i in idxx:
        for i in [0]:
            (t, r), act = ber_functions.sync_and_adjust(tx[i], rx[j])
            print(i)
            print(j)
##            if act > acm:
##                itmp = i
##                acm = act
##                t_tmp = t
##                r_tmp = r
##        idxx.remove(itmp)
##        tx_out.append(t_tmp)
##        rx_out.append(r_tmp)
##    return np.array(tx_out), np.array(rx_out)
    return t, r

#Transmitter side
fs = 92.e9          #Sampling frequency
M = 4               #M-QAM
nmodes =1           #Number of polarizations
fb = 10*10**9       #Symbol rate (float)
N = 2**18/(fs/fb)/2 #Number of symbols per polarization; This is set to be around 2^18 bits of data (0.5*2^18 Sa) after resampling.

##sig = transmit_signal(fs, M, N, nmodes, fb)
sig = signals.SignalQAMGrayCoded(M, N, nmodes, fb)
#Receiver side
resampled_sig = receive_signal()
E, ber= signal_compare(resampled_sig)

sig2=np.roll(sig,100)
##pdb.set_trace()
##TX, RX = sig2._sync_and_adjust(sig, sig2)
#pdb.set_trace()
#TX2, RX2 = sync_and_adjust(sig, sig2)
offset, tx, ii, acm = ber_functions.find_sequence_offset_complex(sig[0], sig2[0])
realigned_sig = np.roll(tx,offset)
#(tX,rX),act = ber_functions.sync_and_adjust(sig[0], sig2[0],"rx") #shift rx to sync with tx; don't know why you have to index the array to make it functional
##ttx = np.roll(tx, offset)
##rrt = sig2.symbols
impairments.simulate_transmission(sig, modal_delay=[1])
#offset = ber_functions.find_sequence_offset_complex(sig, sig2)

pdb.set_trace()
sys.stdout.write("Done")



