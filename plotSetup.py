import pdb
import sys
import numpy as np
from qampy import theory
import matplotlib.pylab as plt
import qampy.helpers
from scipy import special
from scipy.optimize import curve_fit


def plot_setup_SNR(M, N,snrf,snr,ber,ser,evmf,evm1,evm_known,gmi,Q_fc,t_ory=True):
    fig = plt.figure()
    ax1 = fig.add_subplot(231)
    ax2 = fig.add_subplot(232)
    ax3 = fig.add_subplot(233)
    ax4 = fig.add_subplot(234)
    ax5 = fig.add_subplot(235)
    ax6 = fig.add_subplot(236)    

    ax1.set_title("BER vs SNR")
    ax2.set_title("SER vs SNR")
    ax3.set_title("BER vs EVM")
    ax4.set_title("EVM vs SNR")
    ax5.set_title("Q-factor vs SNR")
    ax6.set_title("GMI vs SNR")
    ax1.set_xlabel('SNR [dB]')
    ax1.set_ylabel('BER [dB]')
    ax1.set_yscale('log')
##    ax1.set_xlim(0,20)
##    ax1.set_ylim(1e-5,1)
    ax2.set_xlabel('SNR [dB]')
    ax2.set_ylabel('SER [dB]')
    ax2.set_yscale('log')
##    ax2.set_xlim(0,20)
##    ax2.set_ylim(1e-5,1)
    ax3.set_xlabel('EVM [dB]')
    ax3.set_ylabel('BER [dB]')
    ax3.set_yscale('log')
##    ax3.set_xlim(-15,0)
##    ax3.set_ylim(1e-6,1)
    ax4.set_xlabel('SNR [dB]')
    ax4.set_ylabel('EVM [dB]')
##    ax4.set_xlim(0, 30)
##    ax4.set_ylim(-30, 0)
    ax5.set_xlabel('SNR [dB]')
    ax5.set_ylabel('Q-factor [dB]')
    ax5.set_yscale('log',base=10)
    ax5.set_xscale('log',base=10)
    ax6.set_xlabel('SNR [dB]')
    ax6.set_ylabel('GMI')

    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    ax4.grid(True)
    ax5.grid(True)
    ax6.grid(True)

    c = ['b', 'r', 'g', 'c', 'k']
    s = ['o', '<', 's', '+', 'd']

    j=0
    if t_ory==True:
        ax1.plot(snrf, theory.ber_vs_es_over_n0_qam(10 ** (snrf / 10), M), color=c[j+1], label="%d-QAM theory" % M)
        ax2.plot(snrf, theory.ser_vs_es_over_n0_qam(10 ** (snrf / 10), M), color=c[j+1], label="%d-QAM theory" % M)
        ax5.plot(snrf, 20*np.log10(special.erfcinv(theory.ber_vs_es_over_n0_qam(10 ** (snrf / 10), M)*2)*np.sqrt(2)), color=c[j+1], label="%d-QAM theory" % M)
        ax6.plot(snrf, theory.cal_gmi(M, snrf, N=N), color=c[j], label="GMI theory")
    ax1.plot(snr, ber, color=c[j], marker=s[j], lw=0, label="%d-QAM"%M)
    ax2.plot(snr, ser, color=c[j], marker=s[j], lw=0, label="%d-QAM"%M)
    ax3.plot(evmf, theory.ber_vs_evm_qam(evmf, M), color=c[j], label="%d-QAM theory" % M)
##    ax3.plot(qampy.helpers.lin2dB(evm1 ** 2), ber, color=c[j+1], marker=s[j], lw=0, label="%d-QAM" % M)
    # illustrate the difference between a blind and non-blind EVM
    ax3.plot(qampy.helpers.lin2dB(evm_known ** 2), ber, color=c[j+2], marker='*', lw=0, label="%d-QAM"% M) # non-blind" % M)
##    ax4.plot(snr, qampy.helpers.lin2dB(evm1 ** 2), color=c[j], marker=s[j], lw=0, label="%d-QAM" % M)
    ax4.plot(snr, qampy.helpers.lin2dB(evm_known ** 2), color=c[j+1], marker='*', lw=0, label="%d-QAM"% M)# non-blind" % M)
    #ax4.plot(snr, utils.lin2dB(evm2), color=c[j], marker='*', lw=0, label="%d-QAM signalq"%M)
    ax5.plot(snr, Q_fc, color=c[j], marker=s[j], lw=0, label="Q-factor")
    ax6.plot(snr, gmi[:,0], color=c[j], marker=s[j], lw=0, label="GMI")

    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    ax5.legend()
    ax6.legend()


def plot_setup_linewidth(M,lwdth,ber,ser,evmf,evm1,evm_known,gmi,Q_fc):
    ##x = lwdth
    ##y = ber
##    minimum=np.amin(lwdth)
##    maximum=np.amax(lwdth)
##    z_1 = np.polyfit(np.log(lwdth), ber, 3, w=-np.log(ber))
##    p_1 = np.poly1d(z_1)
##    xp_1 = np.linspace(minimum, maximum, 100)
    ##z_1 = curve_fit(lambda t,a,b: a+b*np.log10(t),  x,  y)
    ##a=z_1[0][0]
    ##b=z_1[0][1]

    fig = plt.figure()
    ax1 = fig.add_subplot(231)
    ax2 = fig.add_subplot(232)
    ax3 = fig.add_subplot(233)
    ax4 = fig.add_subplot(234)
    ax5 = fig.add_subplot(235)
    ax6 = fig.add_subplot(236) 

    ax1.set_title("BER vs Linewidth [Hz]")
    ax2.set_title("SER vs Linewidth [Hz]")
    ax3.set_title("BER vs EVM")
    ax4.set_title("EVM vs Linewidth [Hz]")
    ax5.set_title("Q-factor vs Linewidth [Hz]")
    ax6.set_title("GMI vs Linewidth [Hz]")
    ax1.set_xlabel('Linewidth [Hz]')
    ax1.set_ylabel('BER [dB]')
    ax1.set_yscale('log')
    ax1.set_xscale('log',base=10)
    ##ax1.set_xlim(0,30)
    ##ax1.set_ylim(1e-5,1)
    ax2.set_xlabel('Linewidth [Hz]')
    ax2.set_ylabel('SER [dB]')
    ax2.set_xscale('log',base=10)
    ax2.set_yscale('log')
    ##ax2.set_xlim(0,30)
    ##ax2.set_ylim(1e-5,1)
    ax3.set_xlabel('EVM [dB]')
    ax3.set_ylabel('BER [dB]')
    ax3.set_yscale('log')
    ##ax3.set_xlim(-30,0)
    ##ax3.set_ylim(1e-6,1)
    ax4.set_xlabel('Linewidth [Hz]')
    ax4.set_ylabel('EVM [dB]')
    ax4.set_xscale('log',base=10)
    ##ax4.set_xlim(0, 30)
    ##ax4.set_ylim(-30, 0)
    ax5.set_xlabel('Linewidth [Hz]')
    ax5.set_ylabel('Q-factor [dB]')
    ax5.set_yscale('log',base=10)
    ax5.set_xscale('log',base=10)
    ax6.set_xlabel('Linewidth [Hz]')
    ax6.set_ylabel('GMI')
    ax6.set_xscale('log',base=10)

    ax1.grid(True)
    ax2.grid(True)
    ax3.grid(True)
    ax4.grid(True)
    ax5.grid(True)
    ax6.grid(True)

    c = ['b', 'r', 'g', 'c', 'k']
    s = ['o', '<', 's', '+', 'd']

    j=0
    ax1.plot(lwdth, ber, color=c[j], marker=s[j], lw=0, label="%d-QAM"%M)
    ##ax1.plot(xp_1, p_1(np.log(xp_1)), color=c[j+1], label='Best fit line')
    ax2.plot(lwdth, ser, color=c[j], marker=s[j], lw=0, label="%d-QAM"%M)
    ax3.plot(evmf, theory.ber_vs_evm_qam(evmf, M), color=c[j], label="%d-QAM theory" % M)
##    ax3.plot(qampy.helpers.lin2dB(evm1 ** 2), ber, color=c[j+1], marker=s[j], lw=0, label="%d-QAM" % M)
    # illustrate the difference between a blind and non-blind EVM
    ax3.plot(qampy.helpers.lin2dB(evm_known ** 2), ber, color=c[j+2], marker='*', lw=0, label="%d-QAM"% M)# non-blind" % M)
##    ax4.plot(lwdth, qampy.helpers.lin2dB(evm1 ** 2), color=c[j], marker=s[j], lw=0, label="%d-QAM" % M)
    ax4.plot(lwdth, qampy.helpers.lin2dB(evm_known ** 2), color=c[j+1], marker='*', lw=0, label="%d-QAM"% M)# non-blind" % M)
    #ax4.plot(snr, utils.lin2dB(evm2), color=c[j], marker='*', lw=0, label="%d-QAM signalq"%M)
    ax5.plot(lwdth, Q_fc, color=c[j], marker=s[j], lw=0, label="Q-factor")
    ax6.plot(lwdth, gmi[:,0], color=c[j], marker=s[j], lw=0, label="GMI")

    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax4.legend()
    ax5.legend()
    ax6.legend()

    ##z_1 = np.polyfit(np.log(lwdth[2:]), ber[2:], 3, w=-np.log(ber[2:]))
    ##p_1 = np.poly1d(z_1)
    ##plt.figure()
    ####plt.xscale('log')
    ####plt.yscale('log')
    ##plt.plot(xp_1, p_1(np.log(xp_1)), color=c[j+1], label='Best fit line')

    ##plt.figure()
    ####plt.xscale('log')
    ####plt.yscale('log')
    ##plt.plot(xp_1, p_1(xp_1), color=c[j+1], label='Best fit line')    

