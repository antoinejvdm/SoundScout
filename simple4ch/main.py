import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import soundfile as sf
from gen_searchGrid import gen_searchGrid
from calc_sampleParam import calc_sampleParam
from calc_STFT import calc_STFT
from calc_FD_GCC import calc_FD_GCC
from calc_SRPconv import calc_SRPconv

# Constants
c = 340  # Speed of sound in m/s
fs = 16000  # Sample rate in Hz
pi = np.pi
w_0 = pi * fs
SNR = 6

# Load microphone positions from CSV
mic_positions_df = pd.read_csv('mic_positions_4ch.csv')
micPos = mic_positions_df[['X', 'Y', 'Z']].to_numpy()  # Ensure columns match your CSV's column names

# Load the audio file
audio_data, samplerate = sf.read('audio_outputEcho0p99_merged.wav')

# STFT parameters
N_STFT = 2048
R_STFT = N_STFT // 2
win = np.sqrt(np.hanning(N_STFT))
omega = 2 * pi * np.linspace(0, fs / 2, N_STFT // 2 + 1)

# Candidate locations
ang_pol = [90]  # Polar angles
ang_az = np.arange(0, 359, 2)  # Azimuth angles
DOAvec_i, Delta_t_i = gen_searchGrid(micPos, ang_pol, ang_az, 'spherical', c)

# Calculate TDOAs and sampling parameters
T, N_mm = calc_sampleParam(micPos, w_0, c)

# Transform to STFT domain
x_STFT, f_x = calc_STFT(audio_data, fs, win, N_STFT, R_STFT, 'onesided')

# Calculate cross-spectral density matrix
psi_STFT = calc_FD_GCC(x_STFT)

# Compute conventional SRP
SRP_conv = calc_SRPconv(psi_STFT, omega, Delta_t_i)
data_array = np.array(SRP_conv)

# Define angles from 0 to 360 degrees and plot
angles_degrees = np.linspace(0, 360, len(data_array[1]))
angles_radians = np.radians(angles_degrees)
x = data_array[1] * np.cos(angles_radians)
y = data_array[1] * np.sin(angles_radians)

plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.title('Vectors at Different Angles')
plt.grid(True)
plt.show()
