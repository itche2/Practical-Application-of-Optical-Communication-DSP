import pdb
import sys
import numpy as np
import math
import statistics
import random
import matplotlib.pylab as plt
from scipy.interpolate import interp1d
from qampy import signals, equalisation, helpers, phaserec, io, filtering
from qampy.core import ber_functions, impairments

def signal_Constellation(sig):
    #Plot the signal constellation diagram of sig
    plt.figure()
    plt.title('Signal constellation diagram')
    plt.plot(sig[0].real, sig[0].imag,'r.')

    plt.figure()
    plt.title('Signal constellation diagram')
    plt.plot(sig[1].real, sig[1].imag,'b.')
    plt.show()
        
def signal_compare(resampled_sig):
    SS = resampled_sig

    ber_SS = SS.cal_ber()#BER of received signal
    print ("Receiver BER =",ber_SS)

    plt.figure()
    plt.title('Received signal')
    plt.plot(SS[0].real, SS[0].imag,'r.')

    #mu = 3e-4 #equalizer step size
    #ntaps = 13 # number of filter taps
    mu = 2e-3 #equalizer step size; e.x.: 3e-4
    ntaps = 21 # number of filter taps e.x.: 13
    sps = 2 #samples per symbol
    nmodes=1
    wxy, err = equalisation.equalise_signal(SS, mu, Ntaps=ntaps, method="cma", adaptive_step=True, avoid_cma_sing=False)
    E = equalisation.apply_filter(SS,  wxy)
    if nmodes == 2:
        muCMA = 1e-3
        muRDE = 1.e-3
        E , wx, (err, err_rde) = equalisation.dual_mode_equalisation(SS, (muCMA, muRDE), ntaps, methods=("mcma", "sbd"), adaptive=(True, True))
        #wxy, err = equalisation.equalise_signal(SS, mu, Ntaps=ntaps, method="mcma", adaptive_step=True, avoid_cma_sing=False)
    E = helpers.normalise_and_center(E)

    SS = E
    signal_rx = SS._signal_present(SS)
    nmodes = signal_rx.shape[0]
    syms_demod = SS.make_decision(signal_rx)
    symbols_tx, syms_demod = SS._sync_and_adjust(SS.symbols, syms_demod, synced= False)
    #(symbols_tx,syms_demod),act = ber_functions.sync_and_adjust(SS.symbols, syms_demod,"rx")
    bits_demod = SS.demodulate(syms_demod)
    tx_synced = SS.demodulate(symbols_tx)
    errs = tx_synced ^ bits_demod 
    SS = SS.recreate_from_np_array(syms_demod[:,3000:-3000])
    E = SS
    
    ber = E.cal_ber()#BER of processed signal
    print ("Processed signal BER =",ber)

    plt.figure()
    plt.title('Processed signal')
    plt.plot(E[0].real, E[0].imag,'r.')
    plt.show()
    return E, ber

def receiver_resample_signal(received_sig):
    #Resample signal
    # DSO resampling at 80 GSa/s
    ADCrate = 80.e9
    resampled_sig = received_sig.resample(ADCrate, beta=0.1, renormalise=True)

    # DSP resampling signal at 2 times the baud rate (2Sa/symbol)
    fs_dsp=resampled_sig.fb*2
    resampled_sig = resampled_sig.resample(fs_dsp, beta=0.1, renormalise=True)

    return resampled_sig

def receive_signal_compressed():
    #Receives signal by resampling
    #Reading signal from compressed text file
    received_sig = io.load_signal('saved_signal.txt')
    #Sampling the transmitted signal at the receiver
    resampled_sig = receiver_resample_signal(received_sig)
    return resampled_sig

def receive_signal(ADCrate=80.e9, signal_r = None, signal_rd=None, DACrate = None, M = None, N = None, nmodes = None, fb = None, bitclass = None, dtype = None, **kwargs):
    #Receives signal by resampling
    #Importing signal
    if signal_r or signal_rd or DACrate or M or N or nmodes or fb or bitclass or dtype is None:
        signal_r, signal_rd, DACrate, M, N, nmodes, fb, bitclass, dtype, kwargs = import_signal()
    if bitclass [8:-3] == 'qampy.signals.RandomBits':
        bitclass = signals.RandomBits
    if dtype[8:-3]=='numpy.complex128':
        dtype = np.complex128
    else:
        dtype = np.complex64

    #Reconstruction of transmitted signal
    if kwargs[:-1]:
        orig_sig = signals.SignalQAMGrayCoded(M, N, nmodes, fb, bitclass, dtype, kwargs)
    else:
        orig_sig = signals.SignalQAMGrayCoded(M, N, nmodes, fb, bitclass, dtype)    
    orig_sig = orig_sig.resample(DACrate, beta=0.1, renormalise=True)
    orig_sig = orig_sig.recreate_from_np_array(signal_rd)
    orig_sig._symbols = orig_sig
    received_sig = orig_sig.recreate_from_np_array(signal_r)
    
    #Sampling the transmitted signal at the receiver
    resampled_sig = receiver_resample_signal(received_sig)
    return resampled_sig

def import_signal(fname="data_files", f_sig_p="data_files/sig_prop.txt"):
    #Imports and reads signal from text file
    #Reading signal transmitted generated
    with open(fname + "/tmp_real_X.txt", 'r') as RX:
        rx = RX.read().splitlines()
    with open(fname + "/tmp_imag_X.txt", 'r') as IX:
        ix = IX.read().splitlines()                
    with open(fname + "/tmp_real_Y.txt", 'r') as RY:
        ry = RY.read().splitlines()        
    with open(fname + "/tmp_imag_Y.txt", 'r') as IY:
        iy = IY.read().splitlines()        


    #Reading original data generated
    with open(fname + "/data_real_X.txt", 'r') as RX_D:
        rxd = RX_D.read().splitlines()
    with open(fname + "/data_imag_X.txt", 'r') as IXD:
        ixd = IXD.read().splitlines()               
    with open(fname + "/data_real_Y.txt", 'r') as RYD:
        ryd = RYD.read().splitlines()
    with open(fname + "/data_imag_Y.txt", 'r') as IYD:
        iyd = IYD.read().splitlines()

    #Rebuilding signal transmitted
    x_temp = np.complex128(ix)
    x_temp = x_temp*1j
    x_temp = x_temp + np.complex128(rx)
    y_temp = np.complex128(iy)
    y_temp = y_temp*1j
    y_temp = y_temp + np.complex128(ry)
    signal_r = [x_temp, y_temp]
    signal_r = np.complex128(signal_r)

    #Getting signal properties from file
    f_sigProp = open(f_sig_p, "r")
    DACrate = float(f_sigProp.readline())
    M = int(f_sigProp.readline())
    N = float(f_sigProp.readline())
    nmodes = int(f_sigProp.readline())
    fb = float(f_sigProp.readline())
    bitclass = f_sigProp.readline()
    dtype = f_sigProp.readline()
    kwargs = f_sigProp.readline()

    #Rebuilding original data
    xd_temp = np.complex128(ixd)
    xd_temp = xd_temp*1j
    xd_temp = xd_temp + np.complex128(rxd)
    yd_temp = np.complex128(iyd)
    yd_temp = yd_temp*1j
    yd_temp = yd_temp + np.complex128(ryd)
    signal_rd = [xd_temp, yd_temp]
    signal_rd = np.complex128(signal_rd)
    
    
    return signal_r, signal_rd, DACrate, M, N, nmodes, fb, bitclass, dtype, kwargs


def equalize_synchronize_signal(resampled_sig, mu=None, ntaps=None, method=None, adaptive_step=None, avoid_cma_sing=None ):
    #Equalize and synchronize the signal and calculate the bit error rate
    if mu is None:
        mu = 2e-3
    if ntaps is None:
        ntaps = 21
    if method is None:
        method="cma"
    if adaptive_step is None:
        adaptive_step=True
    if avoid_cma_sing is None:
        avoid_cma_sing=False
    wxy, err = equalisation.equalise_signal(resampled_sig, mu, Ntaps=ntaps, method=method, adaptive_step=adaptive_step, avoid_cma_sing=avoid_cma_sing)
    E = equalisation.apply_filter(resampled_sig,  wxy)
    E = helpers.normalise_and_center(E)
    ber, errs, tx_synced = E.cal_ber(E,verbose = True) #Synchronize the signal with the data and calculates the bit error rate
    return E, ber, errs ,tx_synced

def recreate_signal_with_synced_transmitter_symbols(sig, M, tx_synced): 
    #recreating signal with synced transmitter symbol
    sig_temp = sig.from_bit_array(tx_synced, M, sig._fb)
    synced_sig = sig_temp.recreate_from_np_array(sig)
    ber_synced_sig = synced_sig.cal_ber(synced_sig)
    return synced_sig, ber_synced_sig

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





    
