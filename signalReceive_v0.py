import pdb
import sys
import numpy as np
import matplotlib.pylab as plt
from qampy import signals, equalisation, helpers, phaserec, io



def import_signal(fname="signal.txt", f_sig_p="sig_prop.txt"):
    #get signal from file
    with open(fname, 'r') as f:
        count = 0
        for line in f:
            count += 1
    signal_r=np.empty((1,count),np.complex128)

    #get signal properties from file
    with open(fname, 'r') as f:
        for i in range (0, signal_r.shape[1]):
            signal_r[0,i] = f.readline()
    f.close()
    
    f_sigProp = open(f_sig_p, "r")
    M = int(f_sigProp.readline())
    N = int(f_sigProp.readline())
    nmodes = int(f_sigProp.readline())
    fb = float(f_sigProp.readline())
    bitclass = f_sigProp.readline()
    dtype = f_sigProp.readline()
    kwargs = f_sigProp.readline()

    return signal_r, M, N, nmodes, fb, bitclass, dtype, kwargs

def receive_signal(fs=80*10**9, signal_r = None, M = None, N = None, nmodes = None, fb = None, bitclass = None, dtype = None, **kwargs):
    if signal_r or M or N or nmodes or fb or bitclass or dtype is None:
        signal_r, M, N, nmodes, fb, bitclass, dtype, kwargs = import_signal()
    if bitclass [8:-3] == 'qampy.signals.RandomBits':
        bitclass = signals.RandomBits
    if dtype[8:-3]=='numpy.complex128':
        dtype = np.complex128
    else:
        dtype = np.complex64

    #reconstruction of original signal
    if kwargs[:-1]:
        orig_sig = signals.SignalQAMGrayCoded(M, N, nmodes, fb, bitclass, dtype, kwargs)
    else:
        orig_sig = signals.SignalQAMGrayCoded(M, N, nmodes, fb, bitclass, dtype)    
    received_sig = orig_sig.recreate_from_np_array(signal_r)
    # fs = 80*10**9
    # resampled original signal at fs
    resampled_sig=received_sig.resample(fs, beta=1, renormalise=True)
    pdb.set_trace()
    #resampled_sig._symbols = resampled_sig.copy()
    #r_sig = orig_sig.from_symbol_array(symbs=resampled_sig, M=4, fb = 10*10**9, dtype = np.complex128)
    return resampled_sig, orig_sig

def signal_compare(resampled_sig, orig_sig):
    SS = resampled_sig
    mu = 4e-4 #equalizer step size
    ntaps = 11 # number of filter taps
    wxy, err = equalisation.equalise_signal(SS, mu, Ntaps=ntaps, TrSyms=None, method="cma", adaptive_step=True)
    E = equalisation.apply_filter(SS,  wxy)
    E = helpers.normalise_and_center(E)
    E, ph = phaserec.viterbiviterbi(E, 11)
    E = helpers.dump_edges(E, 20)

    pdb.set_trace()
    ber = E.cal_ber()
    ber_o = orig_sig.cal_ber()
    print ("Receiver BER =",ber)
    print ("Original BER =",ber_o)

    plt.figure()
    plt.title('Received signal')
    plt.plot(E[0].real, E[0].imag,'r.')
    plt.figure()
    plt.title('Original signal')
    plt.plot(orig_sig[0].real, orig_sig[0].imag,'r.')
    plt.show()
    
    return E, orig_sig, ber, ber_o


resampled_sig, orig_sig = receive_signal()
resampled_sig2 = io.load_signal('saved_signal.txt')
fs=80*10**9
resampled_sig2 = resampled_sig2.resample(fs, beta=None, renormalise=True)
pdb.set_trace()
E, sig, ber, ber_o = signal_compare(resampled_sig2, orig_sig)
pdb.set_trace()
sys.stdout.write("Done")

