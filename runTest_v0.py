import pdb
import sys
import numpy as np
from qampy.core import ber_functions, impairments
from qampy import impairments, signals
from signalGenerate_v2 import transmit_signal, export_signal
from signalReceive_v2 import signal_compare, receive_signal, receive_signal_import, import_signal


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
N = 2**18/(fs/fb)/2 #Number of symbols per polarization; This is set to be around 2^18 bits of data (0.5*2^18 Sa) after resampling.
N = 2**18/(fs/fb)

#Main code
##sig = transmit_signal(fs, M, N, nmodes, fb)
##sps = sig.Nbits #bits per symbol
##sig_len_xtnd = 2**18-sig.shape[1]
##DACrate = fs
##export_signal(DACrate, sig, M, N, nmodes, fb)
##sig = signals.SignalQAMGrayCoded(M, N, nmodes, fb)
#Receiver side
resampled_sig = receive_signal()
#E, ber= signal_compare(resampled_sig)

#sig2 = np.roll(resampled_sig, 1) #single polarization
shift = int(np.floor(2000/2))
shift = 1000
sig2 = np.roll(resampled_sig, shift, axis=1) #dual polarization
        ##sig2 = impairments.simulate_transmission(sig, modal_delay=[100])
        #TX, RX = sig2._sync_and_adjust(sig, sig2) #shifts tx to sync with rx
        ##TX, RX = resampled_sig._sync_and_adjust(resampled_sig.symbols, sig2) #shifts tx to sync with rx
        ##TX2, RX2,acm = sync_and_adjust(resampled_sig.symbols, sig2) #shifts tx to sync with rx
E1, ber = signal_compare(sig2)
pdb.set_trace()
##trimmed_sig = E1[:,int(shift/2):int(-shift/2)]
##ber, errs, tx_synced = E1.cal_ber(trimmed_sig,verbose = True)
ber, errs, tx_synced = sig2.cal_ber(sig2,verbose = True)
print(ber)
# recreating synced transmitter symbol
sig3 = sig2.from_bit_array(tx_synced, M, sig2._fb)
#sig3 = sig2._modulate(tx_synced,sig2._encoding,M)
#sig4 = sig2.recreate_from_np_array(sig3)
##sig4 = sig3.recreate_from_np_array(trimmed_sig)
sig4 = sig3.recreate_from_np_array(sig2)
ber_sig4 = sig4.cal_ber(sig4)

E1, ber = signal_compare(sig4)

##pdb.set_trace()
##syms_demod = sig2.make_decision(E1)
##(tX,rX),act = ber_functions.sync_and_adjust(sig2.symbols, syms_demod,"rx")
        #(tX,rX),act = ber_functions.sync_and_adjust(resampled_sig.symbols[0], sig2[0],"rx") #shift rx to sync with tx; don't know why you have to index the array to make it functional
        #E, ber= signal_compare(tX)
##ber = rX.cal_ber()#BER of processed signal
##print ("Processed signal BER =",ber)
##
##plt.figure()
##plt.title('Processed signal')
##plt.plot(E[0].real, E[0].imag,'r.')
##plt.show()
#E, ber= signal_compare(rX[:,3000:-3000])
        ##offset, tx, ii, acm = ber_functions.find_sequence_offset_complex(sig[0], sig2[0])
        ##realigned_sig = np.roll(tx,offset)

        ##sig2 = np.roll(resampled_sig,100)
        ##offset, tx, ii, acm = ber_functions.find_sequence_offset_complex(sig[0], sig2[0])
        ##realigned_sig = np.roll(tx,offset)

pdb.set_trace()
sys.stdout.write("Done")



