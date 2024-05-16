#############################################################################################################
# Copyright 2021 Bilgesu Çakmak
#
# This software is distributed under the terms of the GNU Public License
# version 3 (http://www.gnu.org/licenses/gpl.txt).
#
# A Matlab version of this code is available at
# https://github.com/tdietzen/LC-SRP.
#
# If you find it useful, please cite:
#
# [1] T. Dietzen, E. De Sena, and T. van Waterschoot, "Low-Complexity
# Steered Response Power Mapping based on Nyquist-Shannon Sampling," in
# Proc. 2021 IEEE Workshop Appl. Signal Process. Audio, Acoust. (WASPAA 2021), New Paltz, NY, USA, Oct. 2021.
#############################################################################################################



import numpy as np
import matplotlib.pyplot as plt
import time
### ACOUSTIC SETUP
from numpy import linalg as LA
import numpy as np


import scipy.io as spio

#speed of sound
c = 340;
#sample rate
fs = 16000;
#bandlimit
import math
pi=math.pi
w_0 = pi*fs;
#SNR in dB
SNR = 6;



## MICROPHONE ARRAY
# circular array, 10cm radius, six microphones
import scipy.io
#import matplotlib.pyplot as plt
tmp = scipy.io.loadmat('coord_mic_array.mat')
# array center
arrayCenterPos = tmp.get('arrayCenterPos')
# microphone positions
micPos = tmp.get('micPos');
# number of microphones
M = len(micPos)

### SOURCE LOCATIONS
# 8 different locations
tmp = scipy.io.loadmat('coord_loc_1_8.mat');
true_loc = tmp.get('true_loc');
# compute ground truth DOA vectors for source locations

L = 32;


# STFT PARAMETERS
# window size
N_STFT = 2048;
# shift
R_STFT = N_STFT/2;
# window
win = np.sqrt(np.hanning(N_STFT));
N_STFT_half = math.floor(N_STFT/2)+1;
# frequency vector
omega = 2*pi*np.transpose(np.linspace(0,fs/2,N_STFT_half));


# CANDIDATE LOCATIONS
# polar angles of candidate locations
ang_pol= [90] #np.arange(90, 181, 2).tolist();
# azimuth angles of candidate locations 
ang_az = np.arange(0,359,2).tolist();
# compute candidate DOA vectors and TDOAs
from gen_searchGrid import gen_searchGrid
DOAvec_i, Delta_t_i = gen_searchGrid(micPos, ang_pol, ang_az, 'spherical', c);

DOAvec_i_tmp= DOAvec_i.copy();
DOAvec_i_tmp2= DOAvec_i.copy();


# SRP APPROXIMATION PARAMETERS
# compute sampling period and number of samples within TDOA interval
from calc_sampleParam import calc_sampleParam
T, N_mm  =calc_sampleParam(micPos, w_0, c);
#number of auxilary samples (approximation will be computed for all values in vector)
N_aux = range(0,3);

## PROCESSING
import soundfile as sf

for true_loc_idx in range (1,len(true_loc)+1):
#for true_loc_idx in range (1,2):

    print(['PROCESSING SOURCE LOCATION'+str(true_loc_idx)])
    #GENERATE MICROPHONE SIGNALS
    #speech componentfor selected source
    x_TD,samplerate = sf.read('x_loc' +str(true_loc_idx)+ '.wav');

    # transform to STFT domain
    from calc_STFT import calc_STFT
    x_STFT,f_x = calc_STFT(x_TD, fs, win, N_STFT, R_STFT, 'onesided');

    ## PROCESSING
    from calc_FD_GCC import calc_FD_GCC
    psi_STFT = calc_FD_GCC(x_STFT); #sorun yok

    #conventional SRP

    print('* compute conventional SRP (stay tuned, this will take a few minutes)...')
    t = time.time();
    print (t)
    from calc_SRPconv import calc_SRPconv
    SRP_conv = calc_SRPconv(psi_STFT, omega, Delta_t_i);
    elapsed = time.time() - t;
    print(elapsed)
    print('_____________==')
    data_array = np.array(SRP_conv)
    #find max
    print(data_array.shape)
    print(data_array[1])

    from PeakPeaking import finde_max
    plt.figure(figsize=(8, 6))
    for i in range(1,len(SRP_conv)): #len(SRP_conv)
        angles_degrees = np.linspace(0, 360, len(data_array[i]))
        angles_radians = np.radians(angles_degrees)
        maxes = finde_max(data_array[i],10,angles_radians)

        x = data_array[i] * np.cos(angles_radians)
        y = data_array[i] * np.sin(angles_radians)

        # Debug information
        print(f"Time Frame {i + 1}")
        print(f"Max Point: ({maxes[0]}, {maxes[1]})")
        print(f"Second Max Point: ({maxes[2]}, {maxes[3]})")

        # Plot vectors
        plt.clf()
        #plt.plot(x, y)
        plt.plot(x, y, label=f'Time Frame {i + 1}')
        #plt.scatter(x, y, color='blue', label='all_points')
        plt.scatter(maxes[0], maxes[1], color='red', label='max1')
        plt.scatter(maxes[2], maxes[3], color='orange', label='max2')
        plt.scatter(0, 0, color='orange', label='center')
        plt.xlabel('X-coordinate')
        plt.ylabel('Y-coordinate')
        plt.title('Vectors at Different Angles')
        plt.grid(True)
        plt.pause(0.5)
    plt.show()
        
    print('done')
print('DONE.')

