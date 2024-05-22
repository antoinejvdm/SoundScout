import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import windows
from scipy.fft import fft

# Read a multi-channel audio file
x, fs = sf.read('simulation_20sources.wav')

# Create a time array that matches the length of the audio signal
t = np.linspace(0, len(x) / fs, num=len(x), endpoint=False)

def calc_STFT_frames(x, fs, win, N_STFT, sides):
    N_STFT_half = N_STFT / 2 + 1

    # Frequency vector
    f = np.linspace(0, fs / 2, int(N_STFT_half))
    if sides == 'twosided':
        f = np.concatenate([f, -f[1:-1][::-1]])

    # Initialize
    num_frames = len(x) // N_STFT
    if sides == 'onesided':
        X = np.zeros((int(N_STFT_half), num_frames, x.shape[1]), dtype=np.complex128)
    if sides == 'twosided':
        X = np.zeros((N_STFT, num_frames, x.shape[1]), dtype=np.complex128)

    for m in range(x.shape[1]):  # Iterate over channels
        for i in range(num_frames):
            x_frame = x[i * N_STFT: (i + 1) * N_STFT, m]
            X_frame = fft(np.multiply(win, x_frame))
            if sides == 'onesided':
                X[:, i, m] = X_frame[:int(N_STFT_half)]
            if sides == 'twosided':
                X[:, i, m] = X_frame
    return X, f

# STFT parameters
N_STFT = 1024  # Window size
win = windows.hann(N_STFT)  # Hanning window

# Apply STFT
X, f = calc_STFT_frames(x, fs, win, N_STFT, 'onesided')

# Plot time-domain signal for the first channel
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(t, x[:, 0])  # Plot only the first channel
plt.title("Time-Domain Signal")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# Plot frequency-domain representation (magnitude spectrum) for the first frame of the first channel
plt.subplot(1, 2, 2)
plt.plot(f, np.abs(X[:, 0, 0]))  # Plot only the first frame of the first channel
plt.title("Frequency-Domain Representation")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude")

plt.tight_layout()
plt.show()

