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

################################################################################################
import numpy as np
import matplotlib.pyplot as plt
import time
### ACOUSTIC SETUP
from numpy import linalg as LA
import pandas as pd
import random

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
mic_positions_df = pd.read_csv('mic_positions_4ch.csv')
micPos = mic_positions_df[['X', 'Y', 'Z']].to_numpy()  # Ensure columns match your CSV's column names

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

# SRP APPROXIMATION PARAMETERS
# compute sampling period and number of samples within TDOA interval
from calc_sampleParam import calc_sampleParam
T, N_mm  =calc_sampleParam(micPos, w_0, c);
#number of auxilary samples (approximation will be computed for all values in vector)
N_aux = range(0,3);


## VISUALIZATION OF ANGLE FOR THE BIGGEST PEAK
from visualization_of_angles import update_visualization
plt.ion()  # animation mode
f1 = plt.figure()
f2 = plt.figure()
axis_visualization = f1.add_subplot(projection='3d')
ax2 = f2.add_subplot(111)
plt.show()
plt.pause(0.3) #before starting computing the angle there must be longer pause to show plots



import soundfile as sf

file_path = 'simulation_20sources.wav'

# Define parameters
start_frame = 0
frames_per_iteration = N_STFT

# Open the audio file
with sf.SoundFile(file_path, 'r') as f:
    # Loop through the file in chunks of 64 frames
    for iteration in range(f.frames // frames_per_iteration):
        start_pos = start_frame + (iteration * frames_per_iteration)
        x_TD, samplerate = sf.read(file_path, start=start_pos, frames=frames_per_iteration)

        #x_TD, samplerate = sf.read('x_loc1.wav', start=1024, frames=64)
        print('x_TD',x_TD.shape)
        print('samplerate:',samplerate)

        # transform to STFT domain
        from calc_STFT_frames import calc_STFT_frames
        x_STFT,f_x = calc_STFT_frames(x_TD, fs, win, N_STFT,'onesided');
        print('x_STFT',x_STFT.shape)

        ## PROCESSING
        from calc_FD_GCC_frames import calc_FD_GCC_frames
        psi_STFT = calc_FD_GCC_frames(x_STFT)
        print('psi_STFT',psi_STFT.shape)

        #conventional SRP
        print('* compute conventional SRP (stay tuned, this will take a few minutes)...')
        t = time.time();
        print(t)
        print('delta:',Delta_t_i.shape)
        from calc_SRPconv_frames import calc_SRPconv_frames
        SRP_conv = calc_SRPconv_frames(psi_STFT, omega, Delta_t_i);
        elapsed = time.time() - t;
        print(elapsed)
        print('_____________==')

        data_array = np.array(SRP_conv)
        print(data_array.shape)

        angles_degrees = np.linspace(0, 360, len(data_array))
        # Convert angles to radians
        angles_radians = np.radians(angles_degrees)
        # Convert lengths to x and y coordinates
        x = data_array * np.cos(angles_radians)
        y = data_array * np.sin(angles_radians)

        from PeakPeaking import finde_max
        maxes = finde_max(data_array,10,angles_radians)
        # Plot vectors
        ax2.clear()
        ax2.set_xlabel('X-coordinate')
        ax2.set_ylabel('Y-coordinate')
        ax2.set_title("frame: " + str(iteration))
        ax2.grid(True)
        ax2.plot(x, y, marker='+', linestyle='-')
        ax2.set_xlim(-2500, 2500)
        ax2.set_ylim(-2500, 2500)
        ax2.quiver(0, 0, x[maxes[0]], y[maxes[0]],scale=1, scale_units='xy',color='red')
        ax2.quiver(0, 0, x[maxes[1]], y[maxes[1]],scale=1, scale_units='xy',color='blue')


        update_visualization(axis_visualization,angles_radians[maxes[0]], angles_radians[maxes[1]])
        plt.draw()  # Update the plot
        plt.pause(0.05) # this delay must be there for actualization of graph

        print('done')

