#############################################################################################################
# Our project is based on the work and research of:
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
from Visualization.visualization_of_angles_speakerPos import visualization_of_angles_speakerPos
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
file_path = 'Audio_simulations/Our_speech_two_sources/output_our_speech_audio.wav'
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
mic_positions_df = pd.read_csv('CSV_files/Our_speech_two_sources/microphone_coordinates.csv')
micPos = mic_positions_df[['X','Y','Z']].to_numpy()

## SPEAKERS POSITION
speaker_positions_df = pd.read_csv('CSV_files/Our_speech_two_sources/source_coordinates.csv')
speakerPos = speaker_positions_df[['X','Y','Z']].to_numpy()


# CANDIDATE LOCATIONS
# polar angles of candidate locations
ang_pol= [90] # we only use the horizontal plane inside the sphere
ang_az = np.arange(0,359,2).tolist() # azimuth angles of candidate locations
DOAvec_i, Delta_t_i = calc_deltaTime(micPos, ang_pol, ang_az,'polar',c) # compute candidate DOA vectors

# STFT PARAMETERS
#N_STFT = fs # set N_STFT to the sampling rate fs to have a window size of one second.
N_STFT = 2048
win = np.sqrt(np.hanning(N_STFT)) # window
N_STFT_half = math.floor(N_STFT/2)+1
omega = 2*pi*np.transpose(np.linspace(0,fs/2,N_STFT_half)) # frequency vector

start_frame = 0
frames_per_iteration = N_STFT

#Amount of time for computation
amount_time_STFT = 0
amount_time_FD_GCC = 0
amount_time_SRP = 0
amount_time_iter = 0
with sf.SoundFile(file_path, 'r') as f:
    for iteration in range(f.frames // frames_per_iteration):
        t_iter = time.time();
        start_pos = start_frame + (iteration * frames_per_iteration)
        x_TD, samplerate = sf.read(file_path, start=start_pos, frames=frames_per_iteration)

        # transform to STFT domain
        t_STFT = time.time()
        x_STFT,f_x = calc_STFT_frames(x_TD, fs, win, N_STFT,'onesided')
        amount_time_STFT = amount_time_STFT + (time.time() - t_STFT)

        # PROCESSING
        t_FD_GCC = time.time()
        psi_STFT = calc_FD_GCC_frames(x_STFT)
        amount_time_FD_GCC = amount_time_FD_GCC + (time.time() - t_FD_GCC)

        #conventional SRP
        t_SRP = time.time()
        SRP_conv = calc_SRPconv_frames(psi_STFT, omega, Delta_t_i)
        amount_time_SRP = amount_time_SRP + (time.time() - t_SRP)

        amount_time_iter = amount_time_iter + (time.time() - t_iter)
        print('Time of iteration = ', time.time() - t_iter)

        data_array = np.array(SRP_conv)
        #angles_degrees = np.linspace(0, 360, len(data_array))
        angles_radians = np.radians(ang_az)
        x = data_array * np.cos(angles_radians)
        y = data_array * np.sin(angles_radians)

        maxes = finde_max(data_array,10, angles_radians)

        if(data_array[maxes[1]] > data_array[maxes[0]]*0.5):
            two_sources = True
        else:
            two_sources = False

        if (iteration % 10 == 0):
            ax2.clear()
            ax2.set_xlabel('X-coordinate')
            ax2.set_ylabel('Y-coordinate')
            ax2.set_title("Iteration: " + str(iteration+1))
            ax2.grid(True)
            ax2.plot(x, y,linestyle='-',alpha=0.5)
            #ax2.set_xlim(-data_array[maxes[0]]*1.2, data_array[maxes[0]]*1.2)
            #ax2.set_ylim(-data_array[maxes[0]]*1.2, data_array[maxes[0]]*1.2)
            ax2.set_xlim(-6000, 6000) # to see real size of peaks
            ax2.set_ylim(-6000, 6000)
            ax2.set_aspect('equal')
            ax2.quiver(0, 0, x[maxes[0]], y[maxes[0]],scale=1, scale_units='xy',color='red')
            if(two_sources):
                ax2.quiver(0, 0, x[maxes[1]], y[maxes[1]], scale=1, scale_units='xy', color='green')
            if (two_sources):
                visualization_of_angles_speakerPos(axis_visualization, angles_radians[maxes[0]], angles_radians[maxes[1]], micPos, speakerPos)
            else:
                visualization_of_angle_speakerPos(axis_visualization, angles_radians[maxes[0]],micPos, speakerPos)
            plt.draw()
            plt.pause(0.005)

print('Mean time for STFT = ', amount_time_STFT/(iteration+1))
print('Mean time for FD_GCC = ', amount_time_FD_GCC/(iteration+1))
print('Mean time for SRP = ', amount_time_SRP/(iteration+1))
print('Mean time for iteration = ', (amount_time_iter/(iteration+1))*(fs/N_STFT))
plt.pause(10)