# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import pandas as pd
import numpy.fft as fft
import numpy as np
import matplotlib.pyplot as plt

#IFFT size in LTE
IFFT_SIZE = 2048
NUM_SUBCARRIERS_IN_RB = 12

#UL RB Allocation size 
rb_allocation_size = 20
rb_allocation_size_in_subcarriers = rb_allocation_size * NUM_SUBCARRIERS_IN_RB;

ul_rb_allocation = [0 for i in range(IFFT_SIZE)]
UlTransformPrecodeOut = [0 for i in range(IFFT_SIZE)]

# Generate random numbers
qpsk_mod_sym_array = [1+1.j, 1-1.j, -1-1.j, -1+1.j ]
#16qam_mod_sym_array = [1+3.j, 3+3.j, 1+1.j, 1+3.j, -1+3.j, -3+3.j, -1+1.j, -1+3.j, 1-3.j, 3-3.j, 1-1.j, 1-3.j, -1-3.j, -3-3.j, -1-1.j, -1-3.j ]
mod_sym_array_16qam = [1+3.j, 3+3.j, 1+1.j, 3+1.j, -1+3.j, -3+3.j, -1+1.j, -3+1.j, -1-3.j, -3-3.j, -1-1.j, -3-1.j, 1-3.j, 3-3.j, 1-1.j, 3-1.j,]
#64QAM
mod_sym_array_64qam = []
I = [1, 3, 5, 7]
Q = [1, 3, 5, 7]
for count in range (0, 4):        
    for i in range(0, 4):
        for q in range(0, 4):
            if count == 0:
                mod_sym_array_64qam.append(complex(I[i], Q[q]))
            elif count == 1:
                mod_sym_array_64qam.append(complex(I[i], (-1 * Q[q])))
            elif count == 2:
                mod_sym_array_64qam.append(complex((-1 * I[i]), (-1 * Q[q])))
            elif count == 3:
                mod_sym_array_64qam.append(complex((-1 * I[i]), Q[q]))
    
plt.scatter(np.real(mod_sym_array_64qam), np.imag(mod_sym_array_64qam))
plt.show()

for iter in range(0, 3):
        
    if iter == 0:
        mod_sym_array = qpsk_mod_sym_array
        print('QPSK')
    elif iter == 1:
        mod_sym_array = mod_sym_array_16qam
        print(' ')
        print('16QAM')    
    elif iter == 2:
        mod_sym_array = mod_sym_array_64qam
        print(' ')
        print('64QAM')
    
    plt.scatter(np.real(mod_sym_array), np.imag(mod_sym_array))
    plt.draw()
    
    for i in range(0, rb_allocation_size_in_subcarriers):
        #np.insert(ul_rb_allocation, i, np.random.choice(qpsk_mod_sym_array))
        ul_rb_allocation[i] = 10 * np.random.choice(mod_sym_array);
    
    #Plot the frequency domain output after mapping modulation symbols to the RB allocation 
    plt.plot(np.absolute(ul_rb_allocation))
    plt.draw()
    
    for i in range(2):
            
        if i == 0:
            #Now that we have the subcarriers mapped, take the DFT - Transform Precoding in LTE UL 
            print('With DFT precoding - SCFDMA')
            UlTransformPrecodeOut = fft.fft(ul_rb_allocation, rb_allocation_size_in_subcarriers)
            plt.plot(np.absolute(UlTransformPrecodeOut))
            plt.draw()
        else:
            print('Without DFT precoding - OFDMA')
            UlTransformPrecodeOut = ul_rb_allocation   
        
        #Take 2K IFFT 
        UlOutputTimeDomain = fft.ifft(UlTransformPrecodeOut, IFFT_SIZE)
        print('FFT Size: ', len(UlOutputTimeDomain))
        #Time domain absolute value 
        UlOutputTimeDomainAbs = np.absolute(UlOutputTimeDomain)
        plt.plot(np.absolute(UlOutputTimeDomainAbs))
        plt.draw()
        
        #Time domain PEAK
        UlTimeDomainPeak = max(UlOutputTimeDomainAbs)
        print('Peak: ', UlTimeDomainPeak )
        #Time domain AVG
        UlTimeDomainAvg = np.mean(UlOutputTimeDomainAbs)
        print('Avg: ', UlTimeDomainAvg )
        
        Peak2Avg = UlTimeDomainPeak/UlTimeDomainAvg
        print('Peak2Avg: ', Peak2Avg )
        
        Peak2AvgdB = 10 * np.log10(Peak2Avg)
        print('Peak2AvgdB: ', Peak2AvgdB )





    
    
    
    
        
        
