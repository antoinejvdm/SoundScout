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
import math
import time
import pandas as pd
import matplotlib.pyplot as plt
import soundfile as sf
from Visualization.visualization_of_angle_speakerPos import visualization_of_angle_speakerPos
from Functions.calc_deltaT import calc_deltaT
from Functions.calc_deltaTime import calc_deltaTime
from Functions.calc_STFT_frames import calc_STFT_frames
from Functions.calc_FD_GCC_frames import calc_FD_GCC_frames
from Functions.calc_SRPconv_frames import calc_SRPconv_frames
from Functions.PeakPeaking import finde_max

# VISUALIZATION OF ANGLE FOR THE BIGGEST PEAK
plt.ion()  # animation mode
f1 = plt.figure()
f2 = plt.figure()
axis_visualization = f1.add_subplot(projection='3d')
ax2 = f2.add_subplot(111)
plt.show()
plt.pause(0.3)


# Load the audio file to get its length in samples
file_path = 'Audio_simulations/output_moving_sound_4ch.wav'
with sf.SoundFile(file_path, 'r') as f:
    total_samples = f.frames

# Calculate the total duration of the audio in seconds
total_duration_seconds = total_samples / f.samplerate

# CONSTANTS
c = 340 #speed of sound
fs = f.samplerate #sample rate
pi=math.pi
w_0 = pi*fs

## MICROPHONE ARRAY
mic_positions_df = pd.read_csv('CSV_files/mic_positions_4ch.csv')
micPos = mic_positions_df[['X','Y','Z']].to_numpy()

# CANDIDATE LOCATIONS
# polar angles of candidate locations
ang_pol= [90] # we only use the horizontal plane inside the sphere
ang_az = np.arange(0,359,2).tolist() # azimuth angles of candidate locations
# compute candidate DOA vectors
DOAvec_i, Delta_t_i = calc_deltaTime(micPos, ang_pol, ang_az,'polar',c)

# STFT PARAMETERS
N_STFT = fs # window size We set N_STFT to the sampling rate fs to have a window size of one second.
R_STFT = N_STFT/2 # shift
win = np.sqrt(np.hanning(N_STFT)) # window
N_STFT_half = math.floor(N_STFT/2)+1
omega = 2*pi*np.transpose(np.linspace(0,fs/2,N_STFT_half)) # frequency vector

start_frame = 0
frames_per_iteration = N_STFT

# Open the audio file
with sf.SoundFile(file_path, 'r') as f:
    for iteration in range(f.frames // frames_per_iteration):
        t_iter = time.time();
        start_pos = start_frame + (iteration * frames_per_iteration)
        x_TD, samplerate = sf.read(file_path, start=start_pos, frames=frames_per_iteration)

        # transform to STFT domain
        x_STFT,f_x = calc_STFT_frames(x_TD, fs, win, N_STFT,'onesided')

        # PROCESSING
        psi_STFT = calc_FD_GCC_frames(x_STFT)

        #conventional SRP
        t = time.time();
        SRP_conv = calc_SRPconv_frames(psi_STFT, omega, Delta_t_i)
        elapsed = time.time() - t
        print('Time of SRPconv computation = ',elapsed)

        data_array = np.array(SRP_conv)
        angles_degrees = np.linspace(0, 360, len(data_array))
        angles_radians = np.radians(angles_degrees)
        x = data_array * np.cos(angles_radians)
        y = data_array * np.sin(angles_radians)

        maxes = finde_max(data_array,10,angles_radians)

        ax2.clear()
        ax2.set_xlabel('X-coordinate')
        ax2.set_ylabel('Y-coordinate')
        ax2.set_title("iteration: " + str(iteration))
        ax2.grid(True)
        ax2.plot(x, y, marker='+', linestyle='-')
        ax2.set_xlim(-70000, 70000)
        ax2.set_ylim(-70000, 70000)
        ax2.set_aspect('equal')
        ax2.quiver(0, 0, x[maxes[0]], y[maxes[0]],scale=1, scale_units='xy',color='red')

        visualization_of_angle_speakerPos(axis_visualization, angles_radians[maxes[0]])
        plt.draw()
        plt.pause(0.01)

        elapsed_iter = time.time() - t_iter
        print('Time of iteration = ', elapsed_iter)

