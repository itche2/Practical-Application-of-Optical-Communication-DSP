import numpy as np
from qampy.core import ber_functions, impairments
from qampy import impairments, signals,equalisation, helpers, phaserec, theory
from signalGenerate import transmit_signal, export_signal
from signalReceive import receiver_resample_signal, equalize_synchronize_signal, import_signal
from signal_Impairments import interpolate_signal, extend_signal, delay
import matplotlib.pylab as plt
from scipy import special
from plotSetup import plot_setup_SNR, plot_setup_linewidth
import pdb

#Signal properties
DACrate = 92.e9         #DAC Sampling frequency (fs) at AWG output
M = 4                   #M-QAM
nmodes =2               #Number of polarizations
fb = 10*10**9           #Baud rate or Symbol rate (float)
N = 2**18/(DACrate/fb)  #Number of symbols per polarization; This is set to be 2^18 symbols of data (2^18 Sa) after resampling.
Nsc=1
os=DACrate/(fb/Nsc)


#Transmitter side
sig = signals.SignalQAMGrayCoded(M, N, nmodes, fb)              #Generating data
Tx=sig.resample(DACrate, beta=0.1, renormalise=True)            #DAC resampling
shift = np.random.randint(-N/2, N/2, 1)
Tx = delay(Tx, shift=0, nmodes=nmodes)                          #Shifting signal to simulate delay
Tx=interpolate_signal(Tx)                                       #Interpolating signal
Tx = extend_signal(Tx,xtnd_w_zero=0)                            #Extending signal to fit 2^18 symbols    
export_signal(DACrate, Tx, M, N, nmodes, fb, compress=False)     #Exporting transmitted signal into files


#Receiver side
Rx = import_signal(M,fb,Nsc,DACrate)                            #Importing signal
resampled_sig = receiver_resample_signal(Rx)    #Resampling signal

#############################################
## Setting up signal quality metrics
snr = np.linspace(5, 16, 12)
snrf = np.linspace(5, 16, 500)
evmf = np.linspace(-30, 0, 500)
lwdth=[0] #Setting up array from 10kHz to 10GHz linewidth with 5 points every decade
l_temp = np.linspace(10*10**3, 10*10**4,5)
for lw in range(3,9):
    lwdth = np.delete(lwdth,-1)
    lwdth = np.append(lwdth,l_temp*(10**(lw-3)))

#############################################################################################
##Signal with SNR impairment
ser = np.zeros(snr.shape)
ber = np.zeros(snr.shape)
evm1 = np.zeros(snr.shape)
evm_known = np.zeros(snr.shape)
gmi = np.zeros([snr.shape[0],2])
i=0
for sr in snr:
    print("SNR = %2f dB"%sr)
    signal_s = impairments.change_snr(resampled_sig, sr)
    #signalx = np.atleast_2d(filtering.rrcos_pulseshaping(signal_s, beta))
    E, BER, errs ,tx_synced = equalize_synchronize_signal(resampled_sig = signal_s)  #Equalizing and synchronizing signal
    evm1[i] = sig.cal_evm()[0]
    evm_known[i] = E.cal_evm()[0]
    ser[i] = E.cal_ser()[0]
    ber[i] = E.cal_ber()[0]
    gmi[i] = E.cal_gmi()[0]
    i += 1

Q_fc = 20*np.log10(special.erfcinv(ber*2)*np.sqrt(2)) #Calculating Q-factor
plot_setup_SNR(M,N,snrf,snr,ber,ser,evmf,evm1,evm_known,gmi,Q_fc)

##############################################################################################
## Signal with linewidth
## Resseting the signal quality metrics to zero
ser = np.zeros(lwdth.shape)
ber = np.zeros(lwdth.shape)
evm1 = np.zeros(lwdth.shape)
evm_known = np.zeros(lwdth.shape)
gmi = np.zeros([lwdth.shape[0],2])

i=0
for L in lwdth:
    print("Linewidth = %2f Hz"%L)
    sig2 = impairments.apply_phase_noise(resampled_sig, L)
    E, BER, errs ,tx_synced = equalize_synchronize_signal(resampled_sig = sig2)  #Equalizing and synchronizing signal
    E, BER, errs ,tx_synced = equalize_synchronize_signal(resampled_sig = E, mu=2e-3, ntaps=21)
    E, ph = phaserec.viterbiviterbi(E, 11)
    E = helpers.dump_edges(E, 20)
    evm1[i] = sig.cal_evm()[0]
    evm_known[i] = E.cal_evm()[0]
    ser[i] = E.cal_ser()[0]
    ber[i] = E.cal_ber()[0]
    gmi[i] = E.cal_gmi()[0]
    i += 1
##Q_fc = special.erfcinv(ber*2)*np.sqrt(2)
pdb.set_trace()
Q_fc = special.erfcinv(ber*2)*np.sqrt(2)    #Calculating Q-factor
plot_setup_linewidth(M,lwdth,ber,ser,evmf,evm1,evm_known,gmi,Q_fc)

##############################################################################################

plt.show()    







