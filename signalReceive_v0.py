import pdb
import sys
import numpy as np
import matplotlib.pylab as plt
from qampy import signals, equalisation, helpers, phaserec, io, filtering

def signal_compare(resampled_sig):
    SS = resampled_sig

    ber_SS = SS.cal_ber()
    print ("Receiver BER =",ber_SS)

    plt.figure()
    plt.title('Received signal')
    plt.plot(SS[0].real, SS[0].imag,'r.')
    
    mu = 3e-4 #equalizer step size
    ntaps = 13 # number of filter taps
    wxy, err = equalisation.equalise_signal(SS, mu, Ntaps=ntaps, method="mcma", adaptive_step=True, avoid_cma_sing=False)
    E = equalisation.apply_filter(SS,  wxy)
    E = helpers.normalise_and_center(E)
    #E, ph = phaserec.viterbiviterbi(E, 11)
    #E = helpers.dump_edges(E, 20)

    ber = E.cal_ber()
    print ("Processed signal BER =",ber)

    plt.figure()
    plt.title('Processed signal')
    plt.plot(E[0].real, E[0].imag,'r.')
    plt.show()
    
    return E, ber

def receive_signal():
    resampled_sig = io.load_signal('saved_signal.txt')
    fs=80.e9 
    resampled_sig = resampled_sig.resample(fs, beta=0.1, renormalise=True)# DSO resampling at 80 GSa/s
    fs=resampled_sig.fb*2
    resampled_sig = resampled_sig.resample(fs, beta=0.1, renormalise=True)# DSP resampling signal at 2Sa/symbol    
    return resampled_sig

resampled_sig = receive_signal()
E, ber= signal_compare(resampled_sig)

sys.stdout.write("Done")

